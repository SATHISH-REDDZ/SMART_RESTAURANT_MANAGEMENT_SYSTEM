# Smart Restaurant Management System 🍽️

> **AI-Powered Smart Restaurant Management and Food Recommendation System**

A modern full-stack web application designed to digitize restaurant operations, automate bill & tax receipt generation, provide real-time admin sales analytics, and recommend dishes to customers using machine learning TF-IDF cosine similarity.

---

## 🚀 Key Features

### 👤 Customer Features
- **User Authentication**: Secure registration, login, and profile management with password hashing.
- **Interactive Menu**: Search dishes by keyword, filter by Category, Price tier (Under ₹100, ₹100-₹200, ₹200-₹500, Above ₹500), and Diet type (Veg / Non-Veg).
- **Food Item Details**: View high-resolution images, descriptions, ratings, and customer reviews.
- **Smart Shopping Cart**: Real-time quantity adjustment, subtotal & tax calculation, and AJAX updates.
- **Checkout & Payment Simulation**: Options for Demo Payment, UPI, Credit/Debit Card, and Cash on Delivery.
- **Digital Tax Receipts**: Instant printable digital tax invoice receipts with itemized pricing, tax breakdowns, and mock transaction IDs.
- **Order Tracking & History**: Track order status (`Pending` → `Confirmed` → `Preparing` → `Ready` → `Completed`).
- **AI Food Recommendations**: Personalized food suggestions calculated using Scikit-Learn TF-IDF similarity vectors.

### 🛡️ Admin Panel Features
- **Executive Dashboard**: Key metrics (Total Customers, Total Orders, Total Revenue, Today's Sales).
- **Sales Analytics Charts**: Interactive trend charts powered by Chart.js & Pandas data synthesis.
- **Menu Management**: Add, edit, delete, and toggle stock availability for food dishes.
- **Category Management**: Create and manage food categories.
- **Order Workflow Control**: Update preparation statuses in real-time.
- **Customer Management**: View registered customer base, order counts, and lifetime spend.
- **Financial Reports**: Exportable transaction logs and tax summaries.

---

## 🛠️ Technology Stack

| Layer | Technology |
|---|---|
| **Frontend** | HTML5, Vanilla CSS3 (Custom Dark Theme & Glassmorphism), JavaScript |
| **Backend** | Python 3, Flask Framework |
| **Database** | SQLite3 |
| **Machine Learning** | Scikit-Learn (TF-IDF Vectorizer, Cosine Similarity), Pandas, NumPy, Joblib |
| **Visualization** | Chart.js, FontAwesome |
| **Testing** | Python `unittest` framework |

---

## 📁 Project Folder Structure

```
SMART-RESTAURANT-MANAGEMENT-SYSTEM/
│
├── app.py                     # Main Flask application entry point
├── config.py                  # Application configurations
├── requirements.txt           # Python dependencies
├── README.md                  # Project documentation
├── LICENSE                    # MIT License
├── .gitignore                 # Git ignore rules
├── .env                       # Environment variables
├── .env.example               # Environment variables example template
│
├── database/
│   ├── restaurant.db          # SQLite Database
│   ├── create_db.py           # Database table creation script
│   ├── seed_data.py           # Database seeding script with sample data
│   └── schema.sql             # SQL Schema definition
│
├── models/
│   ├── user.py                # User model & password hashing
│   ├── food.py                # Food item & search filter model
│   ├── category.py            # Category management model
│   ├── order.py               # Order & order items model
│   ├── payment.py             # Payment transaction model
│   └── review.py              # Food reviews & ratings model
│
├── routes/
│   ├── auth.py                # Login, Register, Logout routes
│   ├── customer.py            # Home, Profile, Contact routes
│   ├── admin.py               # Admin Dashboard & management routes
│   ├── food.py                # Menu, Food Details, Search routes
│   ├── cart.py                # Cart operations routes
│   ├── order.py               # Checkout & Order history routes
│   ├── payment.py             # Payment simulation routes
│   └── recommendation.py      # AI Recommendation routes
│
├── services/
│   ├── auth_service.py        # Auth decorators & session security
│   ├── order_service.py       # Cart & Tax calculation logic
│   ├── payment_service.py     # Payment processing service
│   └── recommendation_service.py # AI Recommendation wrapper
│
├── ml/
│   ├── recommender.py         # TF-IDF Cosine Similarity recommendation engine
│   ├── train_model.py         # Model training & cache script
│   └── model.pkl              # Saved ML recommendation model
│
├── analytics/
│   ├── sales_analysis.py      # Pandas sales metric algorithms
│   ├── order_analysis.py      # Status breakdown analysis
│   └── reports.py             # Admin analytics reports
│
├── templates/                 # Jinja2 HTML templates
│   ├── base.html
│   ├── 404.html
│   ├── 500.html
│   ├── auth/ (login, register)
│   ├── customer/ (home, menu, food_details, cart, checkout, orders, receipt, profile, recommendations)
│   └── admin/ (dashboard, foods, add_food, edit_food, categories, orders, customers, analytics, reports)
│
├── static/                    # Static CSS & JS assets
│   ├── css/ (style.css, auth.css, customer.css, admin.css)
│   └── js/ (main.js, cart.js, menu.js, admin.js)
│
├── tests/                     # Automated unit test suite
│   ├── test_auth.py
│   ├── test_food.py
│   ├── test_cart.py
│   └── test_orders.py
│
└── docs/                      # Documentation reports
    ├── project_report.md
    ├── system_design.md
    └── database_design.md
```

---

## 🔑 Demo Login Credentials

For quick evaluation and testing:

| Account Type | Email | Password | Access |
|---|---|---|---|
| **Admin** | `admin@smartrestaurant.com` | `Admin@123` | Full Admin Dashboard & Management |
| **Customer** | `customer@example.com` | `Customer@123` | Customer Ordering & Receipts |

---

## ⚡ Quick Start & Installation

### 1. Clone Repository
```bash
git clone https://github.com/YOUR_USERNAME/SMART-RESTAURANT-MANAGEMENT-SYSTEM.git
cd SMART-RESTAURANT-MANAGEMENT-SYSTEM
```

### 2. Create Virtual Environment & Install Dependencies
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux / Mac
source venv/bin/activate

pip install -r requirements.txt
```

### 3. Initialize & Seed Database
```bash
python database/seed_data.py
```

### 4. Train Recommendation Model
```bash
python ml/train_model.py
```

### 5. Run Application
```bash
python app.py
```

Open **`http://127.0.0.1:5000`** in your browser.

---

## 🧪 Running Automated Tests

To execute the unit test suite:
```bash
python -m unittest discover -s tests
```

---

## 📄 License
This project is open source and available under the [MIT License](LICENSE).
