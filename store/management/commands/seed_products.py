from django.core.management.base import BaseCommand
from store.models import Category, Product


class Command(BaseCommand):
    help = "Create StanMatt demo categories and products."

    def handle(self, *args, **kwargs):
        data = {
            "fruits-vegetables": ("Fruits & Vegetables", "🥦"),
            "dairy-eggs": ("Dairy & Eggs", "🥛"),
            "meat-fish": ("Meat & Fish", "🥩"),
            "bakery": ("Bakery", "🍞"),
            "beverages": ("Beverages", "🥤"),
            "household": ("Household", "🧴"),
            "snacks-sweets": ("Snacks & Sweets", "🍫"),
            "cleaning": ("Cleaning Essentials", "🧼"),
            "personal-care": ("Personal Care", "🧴"),
            "baby-care": ("Baby Care", "🍼"),
        }

        categories = {}
        for slug, (name, icon) in data.items():
            category, _ = Category.objects.get_or_create(
                slug=slug,
                defaults={"name": name, "icon": icon},
            )
            categories[slug] = category

        products = [
            ("Fresh Tomatoes 1kg", "fresh-tomatoes-1kg", "fruits-vegetables", 120, 150, "🍅", True),
            ("Sukuma Wiki 1 Bunch", "sukuma-wiki", "fruits-vegetables", 45, 55, "🥬", False),
            ("Brookeside Milk 500ml", "brookside-milk-500ml", "dairy-eggs", 65, 75, "🥛", True),
            ("Fresh Eggs 6 Pack", "fresh-eggs-6-pack", "dairy-eggs", 180, 210, "🥚", False),
            ("Chicken Breast 1kg", "chicken-breast-1kg", "meat-fish", 520, 620, "🍗", True),
            ("Tilapia Fish 1kg", "tilapia-fish-1kg", "meat-fish", 480, 550, "🐟", False),
            ("Brown Bread Loaf", "brown-bread-loaf", "bakery", 75, 90, "🍞", True),
            ("Chocolate Muffins", "chocolate-muffins", "bakery", 220, 260, "🧁", False),
            ("Coca Cola 1L", "coca-cola-1l", "beverages", 120, 140, "🥤", True),
            ("Fresh Orange Juice", "orange-juice", "beverages", 250, 300, "🧃", False),
            ("Dish Washing Liquid 1L", "dish-washing-liquid", "household", 228, 280, "🧴", True),
            ("Sunlight Washing Bar", "sunlight-washing-bar", "cleaning", 65, 80, "🧼", False),
            ("Maize Flour 2kg", "maize-flour-2kg", "snacks-sweets", 100, 120, "🌽", True),
            ("Chocolate Bar", "chocolate-bar", "snacks-sweets", 150, 180, "🍫", False),
        ]

        for name, slug, cat, price, old, emoji, featured in products:
            Product.objects.update_or_create(
                slug=slug,
                defaults={
                    "category": categories[cat],
                    "name": name,
                    "description": f"Quality {name.lower()} from StanMatt.",
                    "price": price,
                    "old_price": old,
                    "emoji": emoji,
                    "stock": 50,
                    "featured": featured,
                    "active": True,
                },
            )

        self.stdout.write(self.style.SUCCESS("StanMatt demo data is ready."))
