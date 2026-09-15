# StanMatt Supermarket E-commerce

A modern red-and-white supermarket e-commerce starter built with Django, HTML, CSS and JavaScript.

## Features
- Modern StanMatt homepage
- Rotating offers/discount ticker below the main navbar
- Product categories
- Product search
- Discount badges and sale prices
- Add to cart
- Cart quantity controls
- Checkout page
- Card and M-Pesa payment method selection (demo checkout flow)
- Login, logout and account creation
- Django admin for products, categories and orders
- SQLite database for development

## 1. Create and activate a virtual environment

Windows PowerShell:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, use:

```powershell
venv\Scripts\activate
```

## 2. Install packages

```powershell
pip install -r requirements.txt
```

## 3. Create the database

```powershell
python manage.py makemigrations
python manage.py migrate
```

## 4. Create an admin account

```powershell
python manage.py createsuperuser
```

## 5. Add demo products automatically

```powershell
python manage.py seed_products
```

## 6. Start the website

```powershell
python manage.py runserver
```

Open:

http://127.0.0.1:8000/

Admin:

http://127.0.0.1:8000/admin/

## Payments

The checkout currently records the selected payment method and creates an order. It does NOT collect real card numbers or send real M-Pesa payments.

For production payments, connect the checkout to an approved payment provider/Daraja integration and keep all payment credentials in environment variables. Never store card numbers in your Django database.

## Project structure

stanmatt/
├── manage.py
├── requirements.txt
├── stanmatt/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
└── store/
    ├── admin.py
    ├── apps.py
    ├── models.py
    ├── urls.py
    ├── views.py
    ├── migrations/
    ├── management/commands/seed_products.py
    ├── templates/store/
    ├── templates/registration/
    └── static/store/
