from locust import HttpUser, SequentialTaskSet, task, between

class MyTaskSet(SequentialTaskSet):
    wait_time = between(1, 3)  # Wait time between consecutive tasks
    username = "damian"
    password = "test"

    @task
    def login(self):
        # Send form-encoded POST request to /login endpoint with the corresponding username and password
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        form_data = {"username": self.username, "password": self.password}
        response = self.client.post("/token", data=form_data, headers=headers)
        if response.status_code == 200:
            # Successful login
            token = response.json().get("access_token")
            # Use the token for authenticated requests in subsequent tasks
            self.client.headers.update({"Authorization": f"Bearer {token}"})

    @task
    def get_user(self):
        self.client.get("/users/me/")

    @task
    def get_hmds(self):
        self.client.get("/symbols/hmds", params={"symbol": "AAPL"})

    @task
    def get_symbols(self):
        self.client.get("/symbols")

class MyLoadTest(HttpUser):
    tasks = [MyTaskSet]
    wait_time = between(1, 3)  # Wait time between consecutive tasks
