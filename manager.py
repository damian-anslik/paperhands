import tinydb
import time
import dotenv
import os
from app import models
from cpapi import session


class OrderManager:
    """
    The order manager is responsible for processing orders submitted by the user. There are two types of orders:

    - Market orders: orders that are executed immediately at the current market price.
    - Limit orders: orders that are executed only when the market price reaches a specified price.

    The order manager needs to keep track of all of the symbols. It then gets regular snapshots of the market prices. It uses this information to determine whether or not to execute limit orders.
    """

    def __init__(
        self,
        orders_db: tinydb.TinyDB,
        portfolios_db: tinydb.TinyDB,
        symbols_db: tinydb.TinyDB,
    ):
        self.__orders_db = orders_db
        self.__portfolios_db = portfolios_db
        self.__contracts_db = symbols_db.table("contracts")
        self.__api_session = session.GatewaySession()
        self.__orders = []
        self.__symbol_conid_map = {}
        self.__symbol_price_map = {}

    def __update_orders(self):
        """
        Update the list of orders from the orders database.
        """
        orders = self.__orders_db.all()
        self.__orders = map(lambda order: models.Order.parse_obj(order), orders)
        self.__orders = list(self.__orders)

    def __map_orders_to_conids(self):
        """
        Map the symbols in the orders to their conids so that we can get market data snapshots for them.
        """
        self.__symbol_conid_map = {}
        self.__symbol_price_map = {}
        for order in self.__orders:
            conid = self.__contracts_db.get(tinydb.where("ticker") == order.symbol).get(
                "contract_id"
            )
            self.__symbol_conid_map[order.symbol] = conid

    def __get_market_data_snapshots(self):
        """
        Get market data snapshots for all of the symbols in the orders.
        """
        FIELDS = ["84", "86"]
        conids = list(self.__symbol_conid_map.values())
        if not conids:
            return
        snapshots = self.__api_session.market_data_snapshot(conids, FIELDS)
        for snapshot in snapshots:
            symbol = self.__contracts_db.get(
                tinydb.where("contract_id") == snapshot["conidEx"]
            ).get("ticker")
            has_fields = all(field in snapshot for field in FIELDS)
            if not has_fields:
                continue
            self.__symbol_price_map[symbol] = {
                "bid": snapshot["84"],
                "ask": snapshot["86"],
            }

    def __process_orders(self):
        """
        Process a list of orders.
        """
        for order in self.__orders:
            if order.symbol not in self.__symbol_price_map:
                # Skip orders for which we don't have market data.
                continue
            self.__process_order_single(order)

    def __process_order_single(self, order: models.Order):
        """
        Process a single order. A different method is used for each order type.
        """
        ask_price = float(self.__symbol_price_map[order.symbol]["ask"])
        bid_price = float(self.__symbol_price_map[order.symbol]["bid"])
        match order.order_type:
            case "MKT":
                self.__process_market_order(order, ask_price, bid_price)
            case "LMT":
                self.__process_limit_order(order, ask_price, bid_price)
            case _:
                raise ValueError(f"Invalid order type: {order.order_type}")

    def __create_position(
        self, order: models.Order, fill_price: float
    ) -> models.Position:
        """
        Create a new position and update the user's portfolio.
        """
        position = models.Position(
            symbol=order.symbol,
            quantity=order.quantity,
            side=order.side,
            value=order.quantity * fill_price * (-1 if order.side == "SELL" else 1),
        )
        return position

    def __process_market_order(
        self, order: models.Order, ask_price: float, bid_price: float
    ):
        """
        Process a market order.
        """
        fill_price = ask_price if order.side == "BUY" else bid_price
        position = self.__create_position(order, fill_price)
        self.__update_positions(position, order)

    def __process_limit_order(
        self, order: models.Order, ask_price: float, bid_price: float
    ):
        """
        Process a limit order.
        """
        order_limit_price = order.limit_price
        if order.side == "BUY" and ask_price > order_limit_price:
            return
        if order.side == "SELL" and bid_price < order_limit_price:
            return
        fill_price = ask_price if order.side == "BUY" else bid_price
        position = self.__create_position(order, fill_price)
        self.__update_positions(position, order)

    def __update_positions(self, new_position: models.Position, order: models.Order):
        """
        Update the positions database with the new position and remove the order from the orders database.
        If the user already has a position in the same symbol, then the position is updated.
        If the order side is SELL, then the position is reduced, otherwise it is increased.
        """
        portfolio = self.__portfolios_db.get(tinydb.where("id") == order.portfolio_id)
        portfolio = models.Portfolio.parse_obj(portfolio)
        existing_position = next(
            (
                position
                for position in portfolio.positions
                if position.symbol == new_position.symbol
            ),
            None,
        )
        if existing_position:
            existing_position = models.Position.parse_obj(existing_position)
            updated_position = self.__update_existing_position(
                existing_position, new_position
            )
            portfolio.positions = [
                updated_position.dict()
                if position.symbol == updated_position.symbol
                else position
                for position in portfolio.positions
            ]
        else:
            portfolio = self.__add_new_position(new_position, portfolio)
        portfolio = self.__remove_order(order, portfolio)
        self.__portfolios_db.update(
            portfolio.dict(), tinydb.where("id") == portfolio.id
        )

    def __update_existing_position(
        self, existing_position: models.Position, new_position: models.Position
    ):
        """
        Update an existing position with a new position.
        If the new position is a SELL, then the existing position is reduced, otherwise it is increased.
        Change the side of the existing position to SELL if the quantity after the order is negative.
        Change the side of the existing position to BUY if the quantity after the order is positive.
        If sell order reduce the value of the existing position by the value of the new position.
        If buy order increase the value of the existing position by the value of the new position.
        """
        current_position_quantity = existing_position.quantity * (
            1 if existing_position.side == "BUY" else -1
        )
        new_position_quantity = new_position.quantity * (
            1 if new_position.side == "BUY" else -1
        )
        existing_position.quantity = current_position_quantity + new_position_quantity
        if existing_position.quantity < 0:
            existing_position.side = "SELL"
        elif existing_position.quantity > 0:
            existing_position.side = "BUY"
        else:
            return None
        existing_position.value += new_position.value
        existing_position.quantity = abs(existing_position.quantity) # Always show positive quantity
        return existing_position

    def __add_new_position(
        self, new_position: models.Position, portfolio: models.Portfolio
    ) -> dict:
        portfolio.positions.append(new_position.dict())
        return portfolio

    def __remove_order(
        self, order: models.Order, portfolio: models.Portfolio
    ) -> models.Portfolio:
        """
        Remove an order from the orders database and the user's portfolio.
        """
        self.__orders_db.remove(tinydb.where("id") == order.id)
        portfolio.orders = list(filter(lambda o: o.id != order.id, portfolio.orders))
        return portfolio

    def __manage_brokerage_session(self):
        """
        Manage the broker session and clear dangling market data subscriptions.
        """
        self.__api_session.validate_session()
        self.__api_session.tickle()
        self.__api_session.cancel_market_data_all()

    def run(self):
        """
        Run the order manager loop.
        """
        TIMEOUT_BETWEEN_REQUESTS = 5
        num_iterations_before_tickle = 5
        self.__manage_brokerage_session()
        while True:
            self.__update_orders()
            self.__map_orders_to_conids()
            self.__get_market_data_snapshots()
            self.__process_orders()
            num_iterations_before_tickle -= 1
            if num_iterations_before_tickle == 0:
                self.__manage_brokerage_session()
                num_iterations_before_tickle = 10
            time.sleep(TIMEOUT_BETWEEN_REQUESTS)


if __name__ == "__main__":
    dotenv.load_dotenv()
    ORDERS_DB = os.getenv("ORDERS_DB")
    PORTFOLIOS_DB = os.getenv("PORTFOLIOS_DB")
    SYMBOLS_DB = os.getenv("SYMBOLS_DB")
    INDENT = 4
    orders_db = tinydb.TinyDB(ORDERS_DB, indent=INDENT)
    portfolios_db = tinydb.TinyDB(PORTFOLIOS_DB, indent=INDENT)
    symbols_db = tinydb.TinyDB(SYMBOLS_DB, indent=INDENT)
    order_manager = OrderManager(orders_db, portfolios_db, symbols_db)
    order_manager.run()
