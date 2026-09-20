from locust import HttpUser, task, between


class StanMattUser(HttpUser):
    wait_time = between(1, 3)

    @task(5)
    def homepage(self):
        self.client.get("/")

    @task(4)
    def products(self):
        self.client.get("/products/")

    @task(3)
    def product_detail(self):
        self.client.get("/products/chocolate-bar/")

    @task(2)
    def login_page(self):
        self.client.get("/login/")

    @task(2)
    def cart(self):
        self.client.get("/cart/")

    @task(2)
    def deals(self):
        self.client.get("/deals/")

    @task(1)
    def new_arrivals(self):
        self.client.get("/new-arrivals/")

    @task(1)
    def best_sellers(self):
        self.client.get("/best-sellers/")

    @task(1)
    def flash_sales(self):
        self.client.get("/flash-sales/")

    @task(1)
    def help_center(self):
        self.client.get("/help/")

    @task(1)
    def store_locator(self):
        self.client.get("/store-locator/")