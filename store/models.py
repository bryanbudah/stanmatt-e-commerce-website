from django.conf import settings
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    icon = models.CharField(max_length=20, default="")

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="products",
    )

    name = models.CharField(max_length=180)

    slug = models.SlugField(unique=True)

    description = models.TextField(blank=True)

    # Current selling price
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )

    # Original price used when the product is discounted
    old_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
    )

    # Uploaded product image
    image = models.ImageField(
        upload_to="products/",
        blank=True,
        null=True,
    )

    # Optional external image URL
    image_url = models.URLField(
        blank=True,
    )

    # Emoji fallback when no image exists
    emoji = models.CharField(
        max_length=10,
        default="🛒",
    )

    # Inventory
    stock = models.PositiveIntegerField(
        default=50,
    )

    # Store display controls
    featured = models.BooleanField(
        default=False,
    )

    active = models.BooleanField(
        default=True,
    )

    # Promotions
    is_deal = models.BooleanField(
        default=False,
    )

    is_flash_sale = models.BooleanField(
        default=False,
    )

    is_best_seller = models.BooleanField(
        default=False,
    )

    is_new_arrival = models.BooleanField(
        default=False,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        ordering = ["-featured", "-created_at"]

        indexes = [
            models.Index(fields=["active", "category"]),
            models.Index(fields=["active", "featured"]),
            models.Index(fields=["active", "is_deal"]),
            models.Index(fields=["active", "is_flash_sale"]),
            models.Index(fields=["active", "is_best_seller"]),
            models.Index(fields=["active", "is_new_arrival"]),
            models.Index(fields=["created_at"]),
            models.Index(fields=["price"]),
        ]

    def __str__(self):
        return self.name

    @property
    def discount_percent(self):
        if self.old_price and self.old_price > self.price:
            return round(
                (1 - (self.price / self.old_price)) * 100
            )

        return 0

    @property
    def display_image(self):
        """
        Image priority:
        1. Uploaded image
        2. External image URL
        3. Empty string so the template can show the emoji
        """
        if self.image:
            return self.image.url

        if self.image_url:
            return self.image_url

        return ""


class Order(models.Model):
    PAYMENT_CHOICES = [
        ("mpesa", "M-Pesa"),
        ("card", "Card"),
    ]

    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("paid", "Paid"),
        ("processing", "Processing"),
        ("delivered", "Delivered"),
        ("cancelled", "Cancelled"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="orders",
    )

    full_name = models.CharField(
        max_length=180,
    )

    phone = models.CharField(
        max_length=30,
    )

    address = models.TextField()

    city = models.CharField(
        max_length=100,
        default="Nairobi",
    )

    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_CHOICES,
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending",
    )

    subtotal = models.DecimalField(
        max_digits=12,
        decimal_places=2,
    )

    delivery_fee = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
    )

    discount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
    )

    total = models.DecimalField(
        max_digits=12,
        decimal_places=2,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        ordering = ["-created_at"]

        indexes = [
            models.Index(fields=["status", "created_at"]),
            models.Index(fields=["user", "created_at"]),
        ]

    def __str__(self):
        return f"Order #{self.id} — {self.full_name}"


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="items",
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT,
    )

    quantity = models.PositiveIntegerField()

    unit_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )

    @property
    def line_total(self):
        return self.quantity * self.unit_price

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"