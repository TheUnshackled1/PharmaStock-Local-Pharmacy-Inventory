# PharmaStock - Pharmacy Inventory Management System

PharmaStock is a comprehensive inventory management system designed specifically for pharmacies. It helps manage product stock, track expiry dates, handle sales, and manage suppliers efficiently. This web-based application is built with Django and provides a user-friendly interface for both pharmacy staff and customers.

## Key Features

*   **Product Management:** Add, edit, and delete products with details like category, quantity, expiry date, and price.
*   **Stock Tracking:** Automatically monitors stock levels and identifies products that are running low.
*   **Expiry Date Management:** Keeps track of product expiry dates and provides alerts for expired and soon-to-expire products.
*   **Supplier Management:** Maintain a database of suppliers with their contact information.
*   **Sales and Checkout:** A simple and efficient checkout process for customers to purchase products.
*   **Income Reporting:** Generate reports to track total income from sales.
*   **Sales Forecasting:** Provides a basic sales forecast based on historical data.
*   **Product Returns:** Allows customers to request returns and admins to manage them.
*   **Barcode Generation:** Automatically generates EAN-13 barcodes for each product.
*   **User Authentication:** Separate views for authenticated users (customers) and staff (admins).

## Real-World Application

In a real-world pharmacy, PharmaStock can be an invaluable tool to streamline daily operations. Here’s how it can help:

*   **Reduce Waste:** By tracking expiry dates, the pharmacy can prioritize selling products that are nearing their expiry, thus reducing waste and financial loss.
*   **Prevent Stockouts:** The low-stock alerts ensure that popular and essential medicines are always available, improving customer satisfaction and preventing lost sales.
*   **Improve Efficiency:** Automating inventory tracking saves significant time for pharmacy staff, allowing them to focus on customer service and other critical tasks.
*   **Data-Driven Decisions:** The income reports and sales forecasts provide valuable insights for making informed business decisions, such as which products to stock more of.
*   **Enhanced Customer Experience:** A smooth checkout process and the ability to view available products online enhance the overall customer experience.

## Technologies Used

*   **Backend:** Django, Python
*   **Frontend:** HTML, CSS, JavaScript
*   **Database:** SQLite (default, can be configured for other databases)
*   **Libraries:**
    *   `pandas` for data analysis (sales forecasting)
    *   `python-barcode` for generating barcodes
    *   `Pillow` for image processing

## Setup and Installation

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd stock
    ```

2.  **Create a virtual environment and activate it:**
    ```bash
    python -m venv env
    source env/bin/activate  # On Windows, use `env\Scripts\activate`
    ```

3.  **Install the dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
    *(Note: A `requirements.txt` file would need to be created for this step)*

4.  **Apply migrations:**
    ```bash
    python manage.py migrate
    ```

5.  **Create a superuser:**
    ```bash
    python manage.py createsuperuser
    ```

6.  **Run the development server:**
    ```bash
    python manage.py runserver
    ```

The application will be available at `http://127.0.0.1:8000`.

## Project Structure

```
stock/
├── inventory/         # Main application
│   ├── migrations/    # Database migrations
│   ├── templates/     # HTML templates
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py      # Database models
│   ├── tests.py
│   ├── urls.py        # URL routing for the app
│   └── views.py       # Application logic
├── stocktime/         # Django project configuration
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py    # Project settings
│   ├── urls.py        # Root URL configuration
│   └── wsgi.py
├── static/            # Static files (CSS, JS, images)
├── media/             # User-uploaded files (product images, barcodes)
├── manage.py          # Django's command-line utility
└── db.sqlite3         # SQLite database
```