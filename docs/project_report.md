# Project Report: Smart Restaurant Management System

## 1. Executive Summary
The **Smart Restaurant Management System** is a modern full-stack web application developed using Python, Flask, and SQLite. The primary goal is to digitize and automate restaurant operations ranging from online customer ordering, table management, payment processing, itemized tax receipt generation, and real-time administrative analytics to AI-based personalized food recommendations.

## 2. Key Modules & Functional Architecture
1. **Authentication & Role Management**:
   - Werkzeug password hashing (`scrypt`)
   - Protected session management (`customer` vs `admin`)
2. **Customer Portal**:
   - Interactive Menu browsing with multi-parameter filtering (Category, Price range, Diet type)
   - Real-time search query matching
   - Food details and customer review system
   - Shopping cart session manager
   - Payment simulation (Demo Payment, UPI, Card, Cash on Delivery)
   - Digital tax receipt generator
3. **Smart ML Recommendation Engine**:
   - Content-Based filtering using Scikit-Learn `TfidfVectorizer` and `cosine_similarity`.
   - Feature vector extraction across Food Name, Category, Description, and Veg/Non-Veg attributes.
   - User purchase history similarity calculation with popularity fallback.
4. **Admin Dashboard & Analytics**:
   - Executive metric cards (Total Customers, Total Orders, Revenue, Today's Sales).
   - Sales analytics charts powered by Chart.js.
   - Menu item CRUD operations & availability status toggle.
   - Order lifecycle workflow management (Pending → Confirmed → Preparing → Ready → Completed → Cancelled).

## 3. Technology Stack
- **Backend Framework**: Python 3.14, Flask
- **Database**: SQLite3
- **Data Processing & ML**: Pandas, NumPy, Scikit-Learn, Joblib
- **Frontend**: HTML5, Vanilla CSS3 (Custom Dark Mode System), JavaScript, Chart.js, FontAwesome

## 4. Verification & Quality Assurance
- Automated Unit Tests covering authentication, food search, cart operations, order placement, and ML recommendation model.
- 100% test pass rate across all suites (`tests/`).
