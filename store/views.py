from decimal import Decimal

from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .models import Category, Product, Order, OrderItem


# ============================================================
# CART HELPERS
# ============================================================

def _cart_items(request):
    cart = request.session.get("cart", {})

    if not isinstance(cart, dict):
        cart = {}

    product_ids = []

    for product_id in cart.keys():
        try:
            product_ids.append(int(product_id))
        except (TypeError, ValueError):
            continue

    products = (
        Product.objects
        .filter(id__in=product_ids, active=True)
        .select_related("category")
    )

    items = []
    subtotal = Decimal("0")

    for product in products:
        try:
            quantity = int(cart.get(str(product.id), 0))
        except (TypeError, ValueError):
            continue

        if quantity <= 0:
            continue

        quantity = min(quantity, product.stock)

        if quantity <= 0:
            continue

        line_total = product.price * quantity
        subtotal += line_total

        items.append({
            "product": product,
            "quantity": quantity,
            "line_total": line_total,
        })

    delivery = Decimal("0")
    discount = Decimal("0")
    total = subtotal - discount

    return items, subtotal, delivery, discount, total


# ============================================================
# HOME
# ============================================================

def home(request):
    categories = Category.objects.all()

    deals = (
        Product.objects
        .filter(
            active=True,
            is_deal=True,
        )
        .select_related("category")
        .order_by("-featured", "-created_at")[:8]
    )

    featured = (
        Product.objects
        .filter(
            active=True,
            featured=True,
        )
        .select_related("category")
        .order_by("-created_at")[:8]
    )

    # If there are no featured products,
    # show recent active products instead.
    if not featured:
        featured = (
            Product.objects
            .filter(active=True)
            .select_related("category")
            .order_by("-created_at")[:8]
        )

    return render(request, "store/home.html", {
        "categories": categories,
        "deals": deals,
        "featured": featured,
    })


# ============================================================
# ALL PRODUCTS
# ============================================================

def products(request):
    query = request.GET.get("q", "").strip()
    category = request.GET.get("category", "")

    products_qs = (
        Product.objects
        .filter(active=True)
        .select_related("category")
        .order_by("-featured", "-created_at")
    )

    if query:
        products_qs = products_qs.filter(
            name__icontains=query
        )

    if category:
        products_qs = products_qs.filter(
            category__slug=category
        )

    return render(request, "store/products.html", {
        "products": products_qs,
        "categories": Category.objects.all(),
        "query": query,
        "selected_category": category,
        "page_title": "Shop All Products",
        "page_description": (
            "Shop quality products at StanMatt. "
            "Browse our full range of products and enjoy convenient shopping."
        ),
        "collection_page": False,
    })


# ============================================================
# DEALS
# ============================================================

def deals(request):
    products_qs = (
        Product.objects
        .filter(
            active=True,
            is_deal=True,
        )
        .select_related("category")
        .order_by("-featured", "-created_at")
    )

    return render(request, "store/products.html", {
        "products": products_qs,
        "categories": Category.objects.all(),
        "query": "",
        "selected_category": "",
        "page_title": "Deals",
        "page_description": (
            "Shop great deals at StanMatt. "
            "Discover quality products at competitive prices."
        ),
        "collection_page": True,
    })


# ============================================================
# NEW ARRIVALS
# ============================================================

def new_arrivals(request):
    products_qs = (
        Product.objects
        .filter(
            active=True,
            is_new_arrival=True,
        )
        .select_related("category")
        .order_by("-created_at")
    )

    return render(request, "store/products.html", {
        "products": products_qs,
        "categories": Category.objects.all(),
        "query": "",
        "selected_category": "",
        "page_title": "New Arrivals",
        "page_description": (
            "Discover the latest products and new arrivals "
            "at StanMatt."
        ),
        "collection_page": True,
    })


# ============================================================
# BEST SELLERS
# ============================================================

def best_sellers(request):
    products_qs = (
        Product.objects
        .filter(
            active=True,
            is_best_seller=True,
        )
        .select_related("category")
        .order_by("-featured", "-created_at")
    )

    return render(request, "store/products.html", {
        "products": products_qs,
        "categories": Category.objects.all(),
        "query": "",
        "selected_category": "",
        "page_title": "Best Sellers",
        "page_description": (
            "Shop popular best-selling products at StanMatt."
        ),
        "collection_page": True,
    })


# ============================================================
# FLASH SALES
# ============================================================

def flash_sales(request):
    products_qs = (
        Product.objects
        .filter(
            active=True,
            is_flash_sale=True,
        )
        .select_related("category")
        .order_by("-featured", "-created_at")
    )

    return render(request, "store/products.html", {
        "products": products_qs,
        "categories": Category.objects.all(),
        "query": "",
        "selected_category": "",
        "page_title": "Flash Sales",
        "page_description": (
            "Shop limited-time flash sale offers at StanMatt "
            "while stocks last."
        ),
        "collection_page": True,
    })


# ============================================================
# CATEGORY PRODUCTS
# ============================================================

def category_products(request, slug):
    category = get_object_or_404(
        Category,
        slug=slug,
    )

    products_qs = (
        Product.objects
        .filter(
            active=True,
            category=category,
        )
        .select_related("category")
        .order_by("-featured", "-created_at")
    )

    return render(request, "store/products.html", {
        "products": products_qs,
        "categories": Category.objects.all(),
        "query": "",
        "selected_category": category.slug,
        "page_title": category.name,
        "page_description": (
            f"Shop {category.name} products at StanMatt."
        ),
        "collection_page": True,
        "category": category,
    })


# ============================================================
# PRODUCT DETAIL
# ============================================================

def product_detail(request, slug):
    product = get_object_or_404(
        Product.objects.select_related("category"),
        slug=slug,
        active=True,
    )

    related = (
        Product.objects
        .filter(
            active=True,
            category=product.category,
        )
        .exclude(pk=product.pk)
        .select_related("category")
        .order_by("-featured", "-created_at")[:4]
    )

    return render(request, "store/product_detail.html", {
        "product": product,
        "related": related,
    })


# ============================================================
# ADD TO CART
# ============================================================

@require_POST
def add_to_cart(request, product_id):
    product = get_object_or_404(
        Product,
        pk=product_id,
        active=True,
    )

    if product.stock <= 0:
        messages.error(
            request,
            "This product is currently out of stock."
        )
        return redirect(
            request.POST.get("next") or "cart"
        )

    cart = request.session.get("cart", {})

    if not isinstance(cart, dict):
        cart = {}

    key = str(product_id)

    try:
        current = int(cart.get(key, 0))
    except (TypeError, ValueError):
        current = 0

    cart[key] = min(
        current + 1,
        product.stock
    )

    request.session["cart"] = cart
    request.session.modified = True

    messages.success(
        request,
        f"{product.name} added to your cart."
    )

    return redirect(
        request.POST.get("next") or "cart"
    )


# ============================================================
# UPDATE CART
# ============================================================

@require_POST
def update_cart(request, product_id):
    product = get_object_or_404(
        Product,
        pk=product_id,
        active=True,
    )

    try:
        quantity = int(
            request.POST.get("quantity", 1)
        )
    except (TypeError, ValueError):
        quantity = 1

    quantity = max(0, quantity)

    cart = request.session.get("cart", {})

    if not isinstance(cart, dict):
        cart = {}

    key = str(product_id)

    if quantity == 0:
        cart.pop(key, None)
    else:
        cart[key] = min(
            quantity,
            product.stock
        )

    request.session["cart"] = cart
    request.session.modified = True

    return redirect("cart")


# ============================================================
# REMOVE FROM CART
# ============================================================

@require_POST
def remove_from_cart(request, product_id):
    cart = request.session.get("cart", {})

    if not isinstance(cart, dict):
        cart = {}

    cart.pop(str(product_id), None)

    request.session["cart"] = cart
    request.session.modified = True

    return redirect("cart")


# ============================================================
# CART
# ============================================================

def cart(request):
    items, subtotal, delivery, discount, total = (
        _cart_items(request)
    )

    return render(request, "store/cart.html", {
        "items": items,
        "subtotal": subtotal,
        "delivery": delivery,
        "discount": discount,
        "total": total,
    })


# ============================================================
# CHECKOUT
# ============================================================

@login_required
def checkout(request):
    items, subtotal, delivery, discount, total = (
        _cart_items(request)
    )

    if not items:
        messages.warning(
            request,
            "Your cart is empty."
        )
        return redirect("products")

    if request.method == "POST":
        full_name = request.POST.get(
            "full_name",
            ""
        ).strip()

        phone = request.POST.get(
            "phone",
            ""
        ).strip()

        address = request.POST.get(
            "address",
            ""
        ).strip()

        city = request.POST.get(
            "city",
            "Nairobi"
        ).strip()

        payment_method = request.POST.get(
            "payment_method",
            ""
        )

        # ----------------------------------------------------
        # Validate delivery information
        # ----------------------------------------------------

        if not all([
            full_name,
            phone,
            address,
        ]):
            messages.error(
                request,
                "Please complete the delivery details."
            )

            return render(
                request,
                "store/checkout.html",
                {
                    "items": items,
                    "subtotal": subtotal,
                    "delivery": delivery,
                    "discount": discount,
                    "total": total,
                },
            )

        # ----------------------------------------------------
        # Validate payment method
        # ----------------------------------------------------

        if payment_method not in {
            "mpesa",
            "card",
        }:
            messages.error(
                request,
                "Please select a valid payment method."
            )

            return render(
                request,
                "store/checkout.html",
                {
                    "items": items,
                    "subtotal": subtotal,
                    "delivery": delivery,
                    "discount": discount,
                    "total": total,
                },
            )

        # ----------------------------------------------------
        # Create order safely
        # ----------------------------------------------------

        with transaction.atomic():

            product_ids = [
                item["product"].id
                for item in items
            ]

            locked_products = {
                product.id: product
                for product in (
                    Product.objects
                    .select_for_update()
                    .filter(
                        id__in=product_ids,
                        active=True,
                    )
                )
            }

            # Check stock again before creating order
            for item in items:
                product = locked_products.get(
                    item["product"].id
                )

                if not product:
                    messages.error(
                        request,
                        (
                            "One of the products in your "
                            "cart is no longer available."
                        ),
                    )
                    return redirect("cart")

                if item["quantity"] > product.stock:
                    messages.error(
                        request,
                        (
                            f"Not enough stock available "
                            f"for {product.name}."
                        ),
                    )
                    return redirect("cart")

            # ------------------------------------------------
            # Create order
            # ------------------------------------------------

            order = Order.objects.create(
                user=request.user,
                full_name=full_name,
                phone=phone,
                address=address,
                city=city,
                payment_method=payment_method,
                subtotal=subtotal,
                delivery_fee=delivery,
                discount=discount,
                total=total,
            )

            # ------------------------------------------------
            # Create order items and reduce stock
            # ------------------------------------------------

            for item in items:
                product = locked_products[
                    item["product"].id
                ]

                OrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=item["quantity"],
                    unit_price=product.price,
                )

                product.stock -= item["quantity"]

                product.save(
                    update_fields=["stock"]
                )

        # ----------------------------------------------------
        # Empty cart after successful order
        # ----------------------------------------------------

        request.session["cart"] = {}
        request.session.modified = True

        return redirect(
            "order_success",
            order_id=order.id,
        )

    return render(
        request,
        "store/checkout.html",
        {
            "items": items,
            "subtotal": subtotal,
            "delivery": delivery,
            "discount": discount,
            "total": total,
        },
    )


# ============================================================
# ORDER SUCCESS
# ============================================================

@login_required
def order_success(request, order_id):
    order = get_object_or_404(
        Order,
        id=order_id,
        user=request.user,
    )

    return render(
        request,
        "store/order_success.html",
        {
            "order": order,
        },
    )


# ============================================================
# SIGN UP
# ============================================================

def signup(request):
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        form = UserCreationForm(
            request.POST
        )

        if form.is_valid():
            user = form.save()

            login(
                request,
                user
            )

            messages.success(
                request,
                "Welcome to StanMatt!"
            )

            return redirect("home")

    else:
        form = UserCreationForm()

    return render(
        request,
        "registration/signup.html",
        {
            "form": form,
        },
    )


# ============================================================
# HELP CENTER
# ============================================================

def help_center(request):
    return render(
        request,
        "store/help_center.html"
    )


# ============================================================
# STORE LOCATOR
# ============================================================

def store_locator(request):
    return render(
        request,
        "store/store_locator.html"
    )


# ============================================================
# TRACK ORDER
# ============================================================

def track_order(request):
    return render(
        request,
        "store/track_order.html"
    )


# ============================================================
# RETURNS POLICY
# ============================================================

def returns_policy(request):
    return render(
        request,
        "store/returns_policy.html"
    )


# ============================================================
# TERMS & CONDITIONS
# ============================================================

def terms_conditions(request):
    return render(
        request,
        "store/terms_conditions.html"
    )


# ============================================================
# APP PAGE
# ============================================================

def app_page(request):
    return render(
        request,
        "store/app_page.html"
    )