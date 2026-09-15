from django.contrib import admin

from .models import Category, Product, Order, OrderItem


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "slug",
        "icon",
    )

    prepopulated_fields = {
        "slug": ("name",)
    }

    search_fields = (
        "name",
    )


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "category",
        "price",
        "old_price",
        "stock",
        "discount_percent",
        "featured",
        "is_deal",
        "is_flash_sale",
        "is_best_seller",
        "is_new_arrival",
        "active",
    )

    list_filter = (
        "category",
        "featured",
        "is_deal",
        "is_flash_sale",
        "is_best_seller",
        "is_new_arrival",
        "active",
    )

    search_fields = (
        "name",
        "description",
    )

    prepopulated_fields = {
        "slug": ("name",)
    }

    fieldsets = (
        (
            "Basic Information",
            {
                "fields": (
                    "name",
                    "slug",
                    "category",
                    "description",
                )
            },
        ),
        (
            "Pricing",
            {
                "fields": (
                    "price",
                    "old_price",
                )
            },
        ),
        (
            "Product Image",
            {
                "fields": (
                    "image",
                    "image_url",
                    
                )
            },
        ),
        (
            "Inventory",
            {
                "fields": (
                    "stock",
                )
            },
        ),
        (
            "Store Display",
            {
                "fields": (
                    "featured",
                    "active",
                )
            },
        ),
        (
            "Promotions",
            {
                "fields": (
                    "is_deal",
                    "is_flash_sale",
                    "is_best_seller",
                    "is_new_arrival",
                )
            },
        ),
    )


class OrderItemInline(admin.TabularInline):

    model = OrderItem

    extra = 0

    readonly_fields = (
        "unit_price",
    )


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "full_name",
        "phone",
        "total",
        "payment_method",
        "status",
        "created_at",
    )

    list_filter = (
        "payment_method",
        "status",
        "created_at",
    )

    search_fields = (
        "full_name",
        "phone",
        "address",
    )

    inlines = [
        OrderItemInline
    ]