# Database Design Document

## Entity Relationship Summary
The database utilizes SQLite storage located at `database/restaurant.db`.

### 1. `users` Table
- `id` (INTEGER, PK, AUTOINCREMENT)
- `name` (TEXT)
- `email` (TEXT, UNIQUE)
- `password` (TEXT, Hashed)
- `phone` (TEXT)
- `address` (TEXT)
- `role` (TEXT, 'customer' or 'admin')
- `created_at` (TIMESTAMP)

### 2. `categories` Table
- `id` (INTEGER, PK)
- `name` (TEXT, UNIQUE)
- `description` (TEXT)
- `created_at` (TIMESTAMP)

### 3. `foods` Table
- `id` (INTEGER, PK)
- `name` (TEXT)
- `category_id` (INTEGER, FK -> categories.id)
- `description` (TEXT)
- `price` (REAL)
- `image` (TEXT)
- `is_available` (INTEGER, 1/0)
- `rating` (REAL)
- `is_veg` (INTEGER, 1/0)

### 4. `orders` Table
- `id` (INTEGER, PK)
- `user_id` (INTEGER, FK -> users.id)
- `customer_name` (TEXT)
- `total_amount` (REAL)
- `tax_amount` (REAL)
- `grand_total` (REAL)
- `status` (TEXT: Pending, Confirmed, Preparing, Ready, Completed, Cancelled)
- `payment_status` (TEXT: UNPAID, PAID)
- `order_date` (TIMESTAMP)
- `delivery_address` (TEXT)

### 5. `order_items` Table
- `id` (INTEGER, PK)
- `order_id` (INTEGER, FK -> orders.id)
- `food_id` (INTEGER, FK -> foods.id)
- `food_name` (TEXT)
- `quantity` (INTEGER)
- `price` (REAL)
- `subtotal` (REAL)

### 6. `payments` Table
- `id` (INTEGER, PK)
- `order_id` (INTEGER, FK -> orders.id)
- `payment_method` (TEXT)
- `transaction_id` (TEXT, UNIQUE)
- `amount` (REAL)
- `status` (TEXT)
- `payment_date` (TIMESTAMP)
