from django.urls import path
from . import views


urlpatterns = [
    # Home
    path("", views.home, name="home"),

    # --------------------------------------------------------
    # Product pages
    # --------------------------------------------------------
    path("products/", views.products, name="products"),
    path(
        "products/<slug:slug>/",
        views.product_detail,
        name="product_detail",
    ),
    path(
        "category/<slug:slug>/",
        views.category_products,
        name="category_products",
    ),

    # --------------------------------------------------------
    # Product collections
    # --------------------------------------------------------
    path(
        "deals/",
        views.deals,
        name="deals",
    ),
    path(
        "new-arrivals/",
        views.new_arrivals,
        name="new_arrivals",
    ),
    path(
        "best-sellers/",
        views.best_sellers,
        name="best_sellers",
    ),
    path(
        "flash-sales/",
        views.flash_sales,
        name="flash_sales",
    ),

    # --------------------------------------------------------
    # Shopping
    # --------------------------------------------------------
    path(
        "cart/",
        views.cart,
        name="cart",
    ),
    path(
        "cart/add/<int:product_id>/",
        views.add_to_cart,
        name="add_to_cart",
    ),
    path(
        "cart/update/<int:product_id>/",
        views.update_cart,
        name="update_cart",
    ),
    path(
        "cart/remove/<int:product_id>/",
        views.remove_from_cart,
        name="remove_from_cart",
    ),
    path(
        "checkout/",
        views.checkout,
        name="checkout",
    ),
    path(
        "order/<int:order_id>/success/",
        views.order_success,
        name="order_success",
    ),

    # --------------------------------------------------------
    # Account
    # --------------------------------------------------------
    path(
        "signup/",
        views.signup,
        name="signup",
    ),

    # --------------------------------------------------------
    # Customer support
    # --------------------------------------------------------
    path(
        "help/",
        views.help_center,
        name="help_center",
    ),
    path(
        "track-order/",
        views.track_order,
        name="track_order",
    ),
    path(
        "returns/",
        views.returns_policy,
        name="returns_policy",
    ),
    path(
        "terms/",
        views.terms_conditions,
        name="terms_conditions",
    ),

    # --------------------------------------------------------
    # Other pages
    # --------------------------------------------------------
    path(
        "store-locator/",
        views.store_locator,
        name="store_locator",
    ),
    path(
        "app/",
        views.app_page,
        name="app_page",
    ),
]