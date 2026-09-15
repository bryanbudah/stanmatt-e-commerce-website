from decimal import Decimal
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .models import Category, Product, Order, OrderItem


def _cart_items(request):
    cart = request.session.get("cart", {})
    products = Product.objects.filter(
        id__in=cart.keys(),
        active=True
    )

    items = []
    subtotal = Decimal("0")

    for product in products:

        quantity = int(
            cart.get(str(product.id), 0)
        )

        if quantity <= 0:
            continue

        line_total = product.price * quantity
        subtotal += line_total

        items.append({
            "product": product,
            "quantity": quantity,
            "line_total": line_total,
        })

    # No delivery fee
    delivery = Decimal("0")

    # No discount for now
    discount = Decimal("0")

    # Total = subtotal
    total = subtotal - discount

    return items, subtotal, delivery, discount, total


def home(request):
    categories = Category.objects.all()
    deals = Product.objects.filter(active=True, old_price__isnull=False).order_by("-featured", "-created_at")[:8]
    featured = Product.objects.filter(active=True, featured=True)[:8]
    if not featured:
        featured = Product.objects.filter(active=True)[:8]
    return render(request, "store/home.html", {
        "categories": categories,
        "deals": deals,
        "featured": featured,
    })


def products(request):
    query = request.GET.get("q", "").strip()
    category = request.GET.get("category", "")
    products_qs = Product.objects.filter(active=True)
    if query:
        products_qs = products_qs.filter(name__icontains=query)
    if category:
        products_qs = products_qs.filter(category__slug=category)

    return render(request, "store/products.html", {
        "products": products_qs,
        "categories": Category.objects.all(),
        "query": query,
        "selected_category": category,
    })


def category_products(request, slug):
    category = get_object_or_404(Category, slug=slug)
    return render(request, "store/products.html", {
        "products": Product.objects.filter(active=True, category=category),
        "categories": Category.objects.all(),
        "query": "",
        "selected_category": category.slug,
    })


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, active=True)
    related = Product.objects.filter(active=True, category=product.category).exclude(pk=product.pk)[:4]
    return render(request, "store/product_detail.html", {"product": product, "related": related})


@require_POST
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, pk=product_id, active=True)
    cart = request.session.get("cart", {})
    key = str(product_id)
    current = int(cart.get(key, 0))
    cart[key] = min(current + 1, product.stock)
    request.session["cart"] = cart
    messages.success(request, f"{product.name} added to your cart.")
    return redirect(request.POST.get("next") or "cart")


@require_POST
def update_cart(request, product_id):
    product = get_object_or_404(Product, pk=product_id, active=True)
    quantity = max(0, int(request.POST.get("quantity", 1)))
    cart = request.session.get("cart", {})
    if quantity == 0:
        cart.pop(str(product_id), None)
    else:
        cart[str(product_id)] = min(quantity, product.stock)
    request.session["cart"] = cart
    return redirect("cart")


@require_POST
def remove_from_cart(request, product_id):
    cart = request.session.get("cart", {})
    cart.pop(str(product_id), None)
    request.session["cart"] = cart
    return redirect("cart")


def cart(request):
    items, subtotal, delivery, discount, total = _cart_items(request)
    return render(request, "store/cart.html", {
        "items": items,
        "subtotal": subtotal,
        "delivery": delivery,
        "discount": discount,
        "total": total,
    })


@login_required
def checkout(request):
    items, subtotal, delivery, discount, total = _cart_items(request)

    if not items:
        messages.warning(request, "Your cart is empty.")
        return redirect("products")

    if request.method == "POST":
        full_name = request.POST.get("full_name", "").strip()
        phone = request.POST.get("phone", "").strip()
        address = request.POST.get("address", "").strip()
        city = request.POST.get("city", "Nairobi").strip()
        payment_method = request.POST.get("payment_method", "")

        if not all([full_name, phone, address]) or payment_method not in {"mpesa", "card"}:
            messages.error(request, "Please complete the delivery and payment details.")
            return render(request, "store/checkout.html", locals())

        with transaction.atomic():
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

            for item in items:
                OrderItem.objects.create(
                    order=order,
                    product=item["product"],
                    quantity=item["quantity"],
                    unit_price=item["product"].price,
                )

        request.session["cart"] = {}
        return redirect("order_success", order_id=order.id)

    return render(request, "store/checkout.html", {
        "items": items,
        "subtotal": subtotal,
        "delivery": delivery,
        "discount": discount,
        "total": total,
    })


@login_required
def order_success(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, "store/order_success.html", {"order": order})


def signup(request):
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Welcome to StanMatt!")
            return redirect("home")
    else:
        form = UserCreationForm()

    return render(request, "registration/signup.html", {"form": form})
