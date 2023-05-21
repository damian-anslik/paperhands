import datetime
import tinydb
import fastapi
import dotenv
import os
import numpy
from cpapi import session
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext

from app import models

dotenv.load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
PORTFOLIOS_DB = os.getenv("PORTFOLIOS_DB")
USERS_DB = os.getenv("USERS_DB")
SYMBOLS_DB = os.getenv("SYMBOLS_DB")
ORDERS_DB = os.getenv("ORDERS_DB")
HMDS_DB = os.getenv("HMDS_DB")
PASSWORD_RESET_DB = os.getenv("PASSWORD_RESET_DB")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

user_router = fastapi.APIRouter(tags=["user"])
portfolio_router = fastapi.APIRouter(tags=["portfolio"])
orders_router = fastapi.APIRouter(tags=["order"])
symbols_router = fastapi.APIRouter(tags=["symbol"])

DB_INDENT = 4
orders_db = tinydb.TinyDB(ORDERS_DB, indent=DB_INDENT)
users_db = tinydb.TinyDB(USERS_DB, indent=DB_INDENT)
portfolio_db = tinydb.TinyDB(PORTFOLIOS_DB, indent=DB_INDENT)
password_reset_requests_db = tinydb.TinyDB(PASSWORD_RESET_DB, indent=DB_INDENT)
symbols_db = tinydb.TinyDB(SYMBOLS_DB, indent=DB_INDENT)
hmds_db = tinydb.TinyDB(HMDS_DB, indent=DB_INDENT)

# Client Portal API
cpapi_client = session.GatewaySession()


def send_password_reset_email(email_to: str, username: str, token: str):
    # TODO Implement this
    pass


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def get_user(db: tinydb.TinyDB, username: str):
    user = db.get(tinydb.Query().username == username)
    if user:
        return models.UserInDB(**user)


def authenticate_user(db, username: str, password: str) -> models.UserInDB | None:
    user = get_user(db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(
    data: dict, expires_delta: datetime.timedelta | None = None
) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.datetime.utcnow() + expires_delta
    else:
        expire = datetime.datetime.utcnow() + datetime.timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(
    token: str = fastapi.Depends(oauth2_scheme),
) -> models.UserInDB | None:
    """
    Get the current user from the database. If the user is not found in the database, or if the user is disabled,
    """
    credentials_exception = fastapi.HTTPException(
        status_code=fastapi.status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = models.TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(users_db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(
    current_user: models.User = fastapi.Depends(get_current_user),
) -> models.UserInDB | None:
    """
    Get the current active user from the database. If the user is not found in the database, or if the user is disabled,
    then raise an exception.
    """
    if current_user.disabled:
        raise fastapi.HTTPException(status_code=400, detail="Inactive user")
    return current_user


async def get_user_portfolio(
    id: str, user: models.User = fastapi.Depends(get_current_active_user)
) -> models.Portfolio:
    """
    Get the current user's portfolio from the database. If the user is not found in the database, or if the user is disabled,
    then raise an exception.
    """
    portfolio = portfolio_db.get(tinydb.where("id") == id)
    if portfolio is None:
        raise fastapi.HTTPException(status_code=404, detail="Portfolio not found")
    # Check if the user is the owner of the portfolio
    if portfolio.get("owner_id") != user.id:
        raise fastapi.HTTPException(
            status_code=403, detail="You don't have access to this portfolio"
        )
    return portfolio


@user_router.post("/token", response_model=models.Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = fastapi.Depends(),
):
    """
    Get an access token for a user. If the user is not found in the database, or if the user is disabled,
    then raise an exception.
    """
    user = authenticate_user(users_db, form_data.username, form_data.password)
    if not user:
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = datetime.timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token_expires_timestamp = (
        datetime.datetime.utcnow() + access_token_expires
    ).timestamp()
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {
        "access_token": access_token,
        "access_token_expires": access_token_expires_timestamp,
        "token_type": "bearer",
    }


@user_router.post("/token/refresh", response_model=models.Token)
async def refresh_access_token(
    user: models.User = fastapi.Depends(get_current_user),
):
    """
    Refresh the access token for a user.
    """
    access_token_expires = datetime.timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token_expires_timestamp = (
        datetime.datetime.utcnow() + access_token_expires
    ).timestamp()
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {
        "access_token": access_token,
        "access_token_expires": access_token_expires_timestamp,
        "token_type": "bearer",
    }


@user_router.post("/signup", status_code=fastapi.status.HTTP_201_CREATED)
async def create_user(
    email: str = fastapi.Form(...),
    username: str = fastapi.Form(...),
    password: str = fastapi.Form(...),
):
    """
    Create a new user in the database. If the user already exists, then raise an exception.
    """
    user_in_db = get_user(users_db, username)
    if user_in_db:
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_400_BAD_REQUEST,
            detail="Username already exists",
        )
    hashed_password = get_password_hash(password)
    user_in_db = models.UserInDB(
        username=username,
        email=email,
        disabled=False,
        hashed_password=hashed_password,
    )
    users_db.insert(user_in_db.dict())


@user_router.post(
    "/request-password-reset", status_code=fastapi.status.HTTP_202_ACCEPTED
)
async def request_password_reset(
    username: str = fastapi.Form(...),
):
    """
    Reset the password for a user. If the user is not found in the database, then raise an exception.
    """
    RESET_TOKEN_EXPIRE_MINUTES = 2 * 24 * 60
    user_in_db = get_user(users_db, username)
    if not user_in_db:
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_400_BAD_REQUEST,
            detail="User not found",
        )
    # Generate a reset token
    reset_request_expires = datetime.timedelta(minutes=RESET_TOKEN_EXPIRE_MINUTES)
    reset_token = create_access_token(
        data={"sub": user_in_db.username}, expires_delta=reset_request_expires
    )
    # Store the reset token in the database
    password_reset_requests_db.insert(
        {"token": reset_token, "username": user_in_db.username}
    )
    # Send the email
    send_password_reset_email(
        email_to=user_in_db.email, username=user_in_db.username, token=reset_token
    )
    return fastapi.Response(status_code=fastapi.status.HTTP_202_ACCEPTED)


@user_router.post("/reset-password", status_code=fastapi.status.HTTP_202_ACCEPTED)
async def reset_password(
    token: str = fastapi.Form(...),
    password: str = fastapi.Form(...),
):
    """
    Reset the password for a user. If the user is not found in the database, then raise an exception.
    """
    # Check if the token is valid
    reset_request = password_reset_requests_db.get(tinydb.where("token") == token)
    if reset_request is None:
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_400_BAD_REQUEST,
            detail="Invalid token",
        )
    # Decode the token and get the username and expiration date
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        expiration: int = payload.get("exp")
    except jwt.PyJWTError:
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_400_BAD_REQUEST,
            detail="Invalid token",
        )
    # Check if the token has expired
    if expiration < datetime.datetime.utcnow().timestamp():
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_400_BAD_REQUEST,
            detail="Token expired",
        )
    # Check if the user exists
    user_in_db = get_user(users_db, username)
    if not user_in_db:
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_400_BAD_REQUEST,
            detail="User not found",
        )
    # Update the user's password
    hashed_password = get_password_hash(password)
    users_db.update(
        {"hashed_password": hashed_password},
        tinydb.where("username") == username,
    )
    # Remove the token from the database
    password_reset_requests_db.remove(tinydb.where("token") == token)
    return fastapi.Response(status_code=fastapi.status.HTTP_202_ACCEPTED)


@user_router.get("/users/me/", response_model=models.User)
async def read_users_me(
    current_user: models.User = fastapi.Depends(get_current_active_user),
):
    """
    Get the current active user from the database. If the user is not found in the database, or if the user is disabled,
    then raise an exception.
    """
    return current_user


@portfolio_router.get("/portfolio", response_model=models.Portfolio)
def get_portfolio(portfolio: models.Portfolio = fastapi.Depends(get_user_portfolio)):
    return portfolio


@portfolio_router.post("/portfolio", response_model=models.Portfolio)
def create_portfolio(
    portfolio_name: str = fastapi.Form(...),
    is_public: bool = fastapi.Form(False),
    user: models.User = fastapi.Depends(get_current_active_user),
):
    portfolio = models.Portfolio(
        name=portfolio_name, owner_id=user.id, is_public=is_public
    )
    portfolio_db.insert(portfolio.dict())
    users_db.update(
        {
            "portfolios": user.portfolios
            + [
                {
                    "id": portfolio.id,
                    "name": portfolio.name,
                }
            ]
        },
        tinydb.where("id") == user.id,
    )
    return portfolio


@portfolio_router.put("/portfolio", response_model=models.Portfolio)
def update_portfolio(
    portfolio_name: str = fastapi.Form(...),
    is_public: bool = fastapi.Form(False),
    portfolio: models.Portfolio = fastapi.Depends(get_user_portfolio),
):
    portfolio_id = portfolio["id"]
    updated_portfolio = models.Portfolio(
        id=portfolio_id,
        name=portfolio_name,
        owner_id=portfolio["owner_id"],
        is_public=is_public,
    )
    portfolio_db.update(
        updated_portfolio.dict(),
        tinydb.where("id") == portfolio_id,
    )
    # Update the name of the portfolio in the user's list of portfolios
    user_portfolios = users_db.get(tinydb.where("id") == portfolio["owner_id"])
    # User portfolios have two fields: id and name
    user_portfolios = [
        p if p["id"] != portfolio_id else {"id": portfolio_id, "name": portfolio_name}
        for p in user_portfolios["portfolios"]
    ]
    users_db.update(
        {"portfolios": user_portfolios},
        tinydb.where("id") == portfolio["owner_id"],
    )
    return updated_portfolio


@portfolio_router.delete("/portfolio")
def delete_portfolio(portfolio: models.Portfolio = fastapi.Depends(get_user_portfolio)):
    """
    Delete a portfolio. If the portfolio is not found, then raise an exception.
    """
    portfolio_id = portfolio["id"]
    portfolio_db.remove(tinydb.where("id") == portfolio_id)
    # Remove the portfolio from the user's list of portfolios
    user_portfolios = users_db.get(tinydb.where("id") == portfolio["owner_id"])
    user_portfolios = [
        p for p in user_portfolios["portfolios"] if p["id"] != portfolio_id
    ]
    users_db.update(
        {"portfolios": user_portfolios},
        tinydb.where("id") == portfolio["owner_id"],
    )
    # Remove all orders associated with the portfolio
    orders_db.remove(tinydb.where("portfolio_id") == portfolio_id)
    return fastapi.Response(status_code=204)


@orders_router.get("/order", response_model=models.Order)
def get_order(id: str, user: models.User = fastapi.Depends(get_current_active_user)):
    """
    Retrieve details about a specific order. If the order is not found, then raise an exception.
    """
    order = orders_db.get(tinydb.where("id") == id)
    if order is None:
        raise fastapi.HTTPException(status_code=404)
    user_portfolio_ids = [p.get("id") for p in user.portfolios]
    order_portfolio_id = order.get("portfolio_id")
    if order_portfolio_id in user_portfolio_ids:
        return order
    raise fastapi.HTTPException(status_code=403)


@orders_router.post("/order", response_model=models.Order)
def create_order(
    symbol: str = fastapi.Form(...),
    quantity: float = fastapi.Form(...),
    side: str = fastapi.Form(...),
    order_type: str = fastapi.Form(...),
    limit_price: float = fastapi.Form(None),
    portfolio: models.Portfolio = fastapi.Depends(get_user_portfolio),
):
    portfolio_id = portfolio["id"]
    # Create the order object
    order = models.Order(
        symbol=symbol,
        quantity=quantity,
        side=side,
        order_type=order_type,
        limit_price=limit_price,
        portfolio_id=portfolio_id,
    )
    orders_db.insert(order.dict())
    # Add the order to the portfolio orders
    portfolio["orders"] = portfolio["orders"] + [order.dict()]
    portfolio_db.update(portfolio, tinydb.where("id") == portfolio_id)
    return order


@orders_router.delete("/order")
def cancel_order(
    id: str,
    user: models.User = fastapi.Depends(get_current_active_user),
):
    # Get the order from the database
    order = orders_db.get(tinydb.where("id") == id)
    if order is None:
        raise fastapi.HTTPException(status_code=404)
    # Check that the user has access to the order
    user_portfolio_ids = [p.get("id") for p in user.portfolios]
    order_portfolio_id = order.get("portfolio_id")
    if order_portfolio_id not in user_portfolio_ids:
        raise fastapi.HTTPException(status_code=403)
    # Delete the order from the database
    orders_db.remove(tinydb.where("id") == id)
    # Delete the order from the portfolio
    portfolio = portfolio_db.get(tinydb.where("id") == order_portfolio_id)
    portfolio["orders"] = [o for o in portfolio["orders"] if o["id"] != id]
    portfolio_db.update(portfolio, tinydb.where("id") == order_portfolio_id)
    return fastapi.Response(status_code=204)


@symbols_router.get("/symbols", response_model=list[models.Symbol])
async def get_available_symbol():
    """
    Retrieve a list of all available symbols.
    """
    return symbols_db.table("symbols").all()


def filter_bars(bars: list[dict]) -> list[dict]:
    """
    Filter out bars that are above a moving average threshold.
    """
    MOVING_AVERAGE_WINDOW = 3
    MOVING_AVERAGE_FILTER_THRESHOLD = 2
    open_prices = [bar["o"] for bar in bars]
    open_price_ma = (
        numpy.convolve(open_prices, numpy.ones(MOVING_AVERAGE_WINDOW), "valid")
        / MOVING_AVERAGE_WINDOW
    )
    open_prices_ma = numpy.concatenate(
        (numpy.full(10, numpy.nan), open_price_ma), axis=None
    )
    filtered_bars = [
        bar
        for bar, open_ma in zip(bars, open_prices_ma)
        if bar["o"] < MOVING_AVERAGE_FILTER_THRESHOLD * open_ma
    ]
    return filtered_bars


def request_historical_data(
    conid: str, period: str, bar: str, start: datetime = None
) -> list[dict]:
    """
    Retrieve historical data for a contract.
    """
    response = cpapi_client.historical_market_data(
        conid=conid,
        period=period,
        bar=bar,
        start_time=start,
        outside_rth=True,
    )
    bars = response["data"]
    filtered_bars = filter_bars(bars)
    return filtered_bars


@symbols_router.get("/symbols/hmds")
async def get_historical_market_data(
    symbol: str, _: models.User = fastapi.Depends(get_current_active_user)
):
    """
    Get historical market data for a symbol. If the symbol is not found, then raise an exception.
    If the symbol is found in the database, then return the historical market data from the database,
    otherwise, retrieve the historical market data from the API and store it in the database.
    """
    symbol_upper = symbol.upper()
    market_data = hmds_db.get(tinydb.where("symbol") == symbol_upper)
    if market_data:
        market_data_last_updated = datetime.datetime.fromisoformat(
            market_data["last_updated"]
        )
        is_stale_data = datetime.datetime.now() - market_data_last_updated > datetime.timedelta(days=1)
        if not is_stale_data:
            return market_data
    contract = symbols_db.table("contracts").get(tinydb.where("ticker") == symbol_upper)
    if not contract:
        raise fastapi.HTTPException(status_code=404, detail="Symbol not found")
    conid = contract["contract_id"]
    historical_data = request_historical_data(conid, "1y", "1d")
    market_data = {
        "symbol": symbol.upper(),
        "last_updated": datetime.datetime.now().isoformat(),
        "bars": historical_data,
    }
    hmds_db.upsert(market_data, tinydb.where("symbol") == symbol_upper)
    return market_data
