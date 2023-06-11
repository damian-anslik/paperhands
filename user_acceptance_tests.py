import time
import random
from string import ascii_letters, digits
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By


class UserAcceptanceTests:
    def __init__(self, base_url: str):
        self.driver = webdriver.Chrome()
        self.base_url = base_url

    def create_user(self, email: str, username: str, password: str):
        self.driver.get(self.base_url + "/signup")
        form_inputs = self.driver.find_elements(By.TAG_NAME, "input")
        email_input = form_inputs[0]
        username_input = form_inputs[1]
        password_input = form_inputs[2]
        confirm_password_input = form_inputs[3]
        email_input.send_keys(email)
        username_input.send_keys(username)
        password_input.send_keys(password)
        confirm_password_input.send_keys(password)
        # Submit the form, and wait for a few seconds
        confirm_password_input.send_keys(Keys.RETURN)
        time.sleep(10)
        # Check that the success message is displayed
        success_message = self.driver.find_element(By.CLASS_NAME, "success")
        assert success_message.is_displayed()
        print("User created successfully!")

    def login(self, username: str, password: str):
        self.driver.get(self.base_url + "/login")
        form_inputs = self.driver.find_elements(By.TAG_NAME, "input")
        username_input = form_inputs[0]
        password_input = form_inputs[1]
        username_input.send_keys(username)
        password_input.send_keys(password)
        # Submit the form, and wait for a few seconds
        password_input.send_keys(Keys.RETURN)
        time.sleep(10)
        # Check that the user is redirected to the dashboard
        assert self.driver.current_url == self.base_url + "/dashboard"
        print("Login successful! User is redirected to the dashboard")

    def check_user_redirects_to_dashboard(self):
        # Check that the user is redirected to the dashboard when they visit the root URL, login page, or signup page
        self.driver.get(self.base_url)
        assert self.driver.current_url == self.base_url + "/dashboard"
        self.driver.get(self.base_url + "/login")
        assert self.driver.current_url == self.base_url + "/dashboard"
        self.driver.get(self.base_url + "/signup")
        assert self.driver.current_url == self.base_url + "/dashboard"

    def create_new_portfolio(self, portfolio_name: str):
        # Click on the "Create Portfolio" link in the navbar
        create_portfolio_link = self.driver.find_element(By.LINK_TEXT, "Create Portfolio")
        create_portfolio_link.click()
        time.sleep(5)
        form_inputs = self.driver.find_elements(By.TAG_NAME, "input")
        portfolio_name_input = form_inputs[0]
        portfolio_name_input.send_keys(portfolio_name)
        portfolio_name_input.send_keys(Keys.RETURN)
        time.sleep(10)
        assert self.driver.current_url == self.base_url + "/dashboard"
        print("Portfolio created successfully!")

    def check_portfolio_exists(self, portfolio_name: str):
        # Check that the portfolio exists in the portfolio selector
        portfolio_selector = self.driver.find_element(By.CLASS_NAME, "portfolio-selector")
        portfolio_options = portfolio_selector.find_elements(By.TAG_NAME, "option")
        assert portfolio_name in [option.text for option in portfolio_options]
        print("Portfolio exists in the portfolio selector!")

    def toggle_between_positions_and_orders(self):
        # Click on the "Orders" tab
        tab_selector = self.driver.find_element(By.CLASS_NAME, "tab-selector")
        tab_selector.find_elements(By.TAG_NAME, "div")[1].click()
        time.sleep(5)
        assert tab_selector.find_elements(By.TAG_NAME, "div")[1].get_attribute("class") == "active"
        print("Orders tab is now active!")

    def place_order(self, order_details: dict):
        # Place an order
        symbol_input = self.driver.find_element(By.ID, "symbol")
        quantity_input = self.driver.find_element(By.ID, "quantity")
        order_type_input = self.driver.find_element(By.ID, "order-type")
        if order_details["side"] == "BUY":
            submit_button = self.driver.find_element(By.ID, "buy-order")
        else:
            submit_button = self.driver.find_element(By.ID, "sell-order")
        symbol_input.send_keys(order_details["symbol"])
        quantity_input.send_keys(order_details["quantity"])
        order_type_input.send_keys(order_details["order-type"])
        submit_button.click()
        time.sleep(10)
        orders_table = self.driver.find_element(By.TAG_NAME, "table")
        assert order_details["symbol"] in orders_table.text
        print("Order placed successfully!")

    def rename_portfolio(self, new_portfolio_name: str):
        self.driver.get(self.base_url + "/settings")
        time.sleep(5)
        portfolio_form = self.driver.find_element(By.TAG_NAME, "form")
        portfolio_name_input = portfolio_form.find_element(By.TAG_NAME, "input")
        portfolio_name_input.clear()
        portfolio_name_input.send_keys(new_portfolio_name)
        portfolio_actions = self.driver.find_element(By.CLASS_NAME, "portfolio-actions")
        portfolio_actions.find_element(By.TAG_NAME, "button").click()
        time.sleep(3)
        success_message = self.driver.find_element(By.CLASS_NAME, "success")
        assert success_message.is_displayed()
        print("Portfolio renamed successfully!")
        # Check if the portfolio name is updated in the navbar
        portfolio_selector = self.driver.find_element(By.CLASS_NAME, "portfolio-selector")
        portfolio_options = portfolio_selector.find_elements(By.TAG_NAME, "option")
        assert new_portfolio_name in [option.text for option in portfolio_options]
        print("Portfolio name updated in the navbar!")

    def delete_portfolio(self):
        # Click on the delete button in the portfolio settings page
        self.driver.get(self.base_url + "/settings")
        time.sleep(5)
        portfolio_actions = self.driver.find_element(By.CLASS_NAME, "portfolio-actions")
        portfolio_actions.find_elements(By.TAG_NAME, "button")[1].click()
        time.sleep(5)
        # Check that the user is redirected to the dashboard and the portfolio is deleted
        assert self.driver.current_url == self.base_url + "/dashboard"
        empty_portfolios = self.driver.find_element(By.CLASS_NAME, "empty-portfolios")
        assert empty_portfolios.is_displayed()
        print("Portfolio deleted successfully!")

    def logout(self):
        # Click on the logout button in the navbar and check if the user is redirected to the root page
        navbar = self.driver.find_element(By.TAG_NAME, "nav")
        navbar.find_elements(By.TAG_NAME, "button")[0].click()
        time.sleep(5)
        assert self.driver.current_url == self.base_url + "/"
        print("User logged out successfully!")

    def check_user_redirect_to_login(self):
        # Check if the user is redirected to the login page when trying to access the dashboard without logging in
        self.driver.get(self.base_url + "/dashboard")
        time.sleep(5)
        assert self.driver.current_url == self.base_url + "/login"
        print("User redirected to login page when trying to access dashboard without logging in!")

    def run(self):
        NUM_CHARS_IN_USERNAME = 10
        test_username = "".join(
            random.choice(ascii_letters + digits) for _ in range(NUM_CHARS_IN_USERNAME)
        )
        test_password = "test_password"
        test_email = "example@example.com"
        default_portfolio_name = "Default Portfolio"
        renamed_portfolio = "Renamed Portfolio"
        order_details = {
            "symbol": "AAPL",
            "quantity": "10",
            "order-type": "MKT",
            "side": "BUY"
        }
        self.create_user(test_email, test_username, test_password)
        self.login(test_username, test_password)
        self.check_user_redirects_to_dashboard()
        self.create_new_portfolio(default_portfolio_name)
        self.check_portfolio_exists(default_portfolio_name)
        self.toggle_between_positions_and_orders()
        self.place_order(order_details)
        self.rename_portfolio(renamed_portfolio)
        self.delete_portfolio()
        self.logout()
        self.check_user_redirect_to_login()


if __name__ == "__main__":
    acceptance_tests = UserAcceptanceTests("https://paperhands-fdc46.web.app")
    acceptance_tests.run()