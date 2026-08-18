import sqlite3
import os
import sys
from werkzeug.security import generate_password_hash
from datetime import datetime, timedelta
import random

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config import Config
from database.create_db import init_db

def seed_database():
    init_db()
    conn = sqlite3.connect(Config.DB_PATH)
    cursor = conn.cursor()

    # Clear existing data
    cursor.execute("DELETE FROM recommendations")
    cursor.execute("DELETE FROM reviews")
    cursor.execute("DELETE FROM payments")
    cursor.execute("DELETE FROM order_items")
    cursor.execute("DELETE FROM orders")
    cursor.execute("DELETE FROM cart")
    cursor.execute("DELETE FROM foods")
    cursor.execute("DELETE FROM categories")
    cursor.execute("DELETE FROM users")
    cursor.execute("DELETE FROM sqlite_sequence")

    print("Seeding Users...")
    admin_pass = generate_password_hash("Admin@123")
    cust_pass = generate_password_hash("Customer@123")

    users = [
        ('Administrator', 'admin@smartrestaurant.com', admin_pass, '9876543210', 'Restaurant HQ, City Center', 'admin'),
        ('Sathish Customer', 'customer@example.com', cust_pass, '9123456789', '123 Tech Park Avenue, Flat 4B', 'customer'),
        ('Priya Sharma', 'priya@example.com', generate_password_hash("Priya@123"), '9811122233', '45 Green Park, Metro View', 'customer'),
        ('Rahul Verma', 'rahul@example.com', generate_password_hash("Rahul@123"), '9722233344', '89 Royal Residency', 'customer')
    ]
    cursor.executemany("""
        INSERT INTO users (name, email, password, phone, address, role)
        VALUES (?, ?, ?, ?, ?, ?)
    """, users)

    print("Seeding 8 Categories...")
    categories = [
        ('Biryani', 'Aromatic dum rice cooked with rich Indian spices and marinated meats or veggies'),
        ('Starters', 'Crispy, savory appetizers and kebabs to ignite your taste buds'),
        ('Main Course', 'Hearty traditional Indian curries, gravies, and fresh tandoori breads'),
        ('Fast Food', 'Delicious burgers, pizzas, French fries, and crispy snacks'),
        ('Chinese', 'Authentic wok-tossed noodles, fried rice, and Indo-Chinese manchurian gravies'),
        ('South Indian', 'Traditional dosas, idlis, vadas, sambar, and Malabar parottas'),
        ('Desserts', 'Sweet cakes, ice cream sundaes, waffles, and traditional Indian sweets'),
        ('Beverages', 'Refreshing cold drinks, fresh lime sodas, thick milkshakes, and cold coffee')
    ]
    cursor.executemany("""
        INSERT INTO categories (name, description) VALUES (?, ?)
    """, categories)

    cursor.execute("SELECT name, id FROM categories")
    cat = {row[0]: row[1] for row in cursor.fetchall()}

    print("Seeding 60 Food Items...")
    foods = [
        # BIRYANI (7)
        ('Hyderabadi Chicken Dum Biryani', cat['Biryani'], 'Traditional Hyderabadi chicken biryani cooked in dum style with basmati rice and saffron spices', 240.0, 'https://images.unsplash.com/photo-1563379091339-03b21ab4a4f8?w=500', 1, 4.8, 0),
        ('Special Mutton Dum Biryani', cat['Biryani'], 'Tender mutton pieces layered with saffron basmati rice and rich aromatic spices', 350.0, 'https://images.unsplash.com/photo-1633945274405-b6c8069047b0?w=500', 1, 4.9, 0),
        ('Royal Veg Dum Biryani', cat['Biryani'], 'Fragrant basmati rice layered with garden fresh vegetables, paneer, and dum masala', 190.0, 'https://images.unsplash.com/photo-1543339308-43e59d6b73a6?w=500', 1, 4.5, 1),
        ('Spicy Egg Dum Biryani', cat['Biryani'], 'Spicy roasted boiled egg gravy layered with fragrant spiced biryani rice', 200.0, 'https://images.unsplash.com/photo-1563379091339-03b21ab4a4f8?w=500', 1, 4.4, 0),
        ('Prawns Dum Biryani', cat['Biryani'], 'Juicy prawns marinated in coastal spices layered with fragrant biryani rice', 380.0, 'https://images.unsplash.com/photo-1563379091339-03b21ab4a4f8?w=500', 1, 4.7, 0),
        ('Paneer Tikka Biryani', cat['Biryani'], 'Grilled tandoori paneer cubes layered with spicy basmati biryani rice', 220.0, 'https://images.unsplash.com/photo-1543339308-43e59d6b73a6?w=500', 1, 4.6, 1),
        ('Boneless Chicken Tikka Biryani', cat['Biryani'], 'Smokey grilled boneless chicken tikka layered with aromatic dum biryani rice', 270.0, 'https://images.unsplash.com/photo-1563379091339-03b21ab4a4f8?w=500', 1, 4.8, 0),

        # STARTERS (9)
        ('Chicken 65', cat['Starters'], 'Deep fried spicy chicken appetizers coated with curry leaves, mustard seeds, and chili yogurt sauce', 190.0, 'https://images.unsplash.com/photo-1610057099443-f63a15014605?w=500', 1, 4.7, 0),
        ('Tandoori Paneer Tikka', cat['Starters'], 'Tandoor grilled cottage cheese cubes marinated in spiced yogurt and capsicum', 180.0, 'https://images.unsplash.com/photo-1567188040759-fb8a883dc6d8?w=500', 1, 4.6, 1),
        ('Chilli Chicken Dry', cat['Starters'], 'Wok tossed crispy chicken chunks with bell peppers, green chilies, and soy garlic glaze', 210.0, 'https://images.unsplash.com/photo-1525755662778-989d0524087e?w=500', 1, 4.6, 0),
        ('Crispy Veg Spring Rolls', cat['Starters'], 'Golden fried thin pastry rolls filled with shredded cabbage, carrots, and sweet chili sauce', 150.0, 'https://images.unsplash.com/photo-1544025162-d76694265947?w=500', 1, 4.4, 1),
        ('Tandoori Chicken (Half)', cat['Starters'], 'Traditional clay oven roasted whole chicken leg and breast marinated in red spices', 280.0, 'https://images.unsplash.com/photo-1599487488170-d11ec9c172f0?w=500', 1, 4.8, 0),
        ('Malai Paneer Seekh Kebab', cat['Starters'], 'Melt-in-mouth creamy minced paneer kebabs seasoned with cardamom and cream', 200.0, 'https://images.unsplash.com/photo-1567188040759-fb8a883dc6d8?w=500', 1, 4.5, 1),
        ('Fish Amritsari Fry', cat['Starters'], 'Crispy ajwain spiced gram flour coated fish fillets fried golden brown', 260.0, 'https://images.unsplash.com/photo-1534422298391-e4f8c172dddb?w=500', 1, 4.7, 0),
        ('Crispy Corn Pepper Fry', cat['Starters'], 'Golden crispy sweet corn kernels tossed with freshly crushed black pepper and spring onion', 140.0, 'https://images.unsplash.com/photo-1540420773420-3366772f4999?w=500', 1, 4.3, 1),
        ('Chicken Lollipop (6 Pcs)', cat['Starters'], 'Crispy fried chicken winglets shaped into lollipops served with hot garlic dip', 220.0, 'https://images.unsplash.com/photo-1626082927389-6cd097cdc6ec?w=500', 1, 4.8, 0),

        # MAIN COURSE (9)
        ('Royal Butter Chicken Curry', cat['Main Course'], 'Rich tomato gravy cooked with tender grilled chicken chunks, heavy butter, and fresh cream', 280.0, 'https://images.unsplash.com/photo-1588166524941-3bf61a9c41db?w=500', 1, 4.9, 0),
        ('Dal Makhani Overnight Cooked', cat['Main Course'], 'Slow cooked black lentils simmered overnight with butter, cream, and subtle spices', 200.0, 'https://images.unsplash.com/photo-1546833999-b9f581a1996d?w=500', 1, 4.7, 1),
        ('Kadhai Paneer Special', cat['Main Course'], 'Fresh paneer cubes tossed in rich onion tomato gravy with capsicum and kadhai masala', 220.0, 'https://images.unsplash.com/photo-1631452180519-c014fe946bc7?w=500', 1, 4.6, 1),
        ('Chicken Tikka Masala', cat['Main Course'], 'Roasted chicken tikka pieces in thick spicy onion-tomato gravy', 270.0, 'https://images.unsplash.com/photo-1565557623262-b51c2513a641?w=500', 1, 4.8, 0),
        ('Shahi Paneer', cat['Main Course'], 'Soft paneer in rich royal gravy made from cashews, cream, and aromatic spices', 230.0, 'https://images.unsplash.com/photo-1631452180519-c014fe946bc7?w=500', 1, 4.7, 1),
        ('Mutton Rogan Josh', cat['Main Course'], 'Authentic Kashmiri style mutton curry cooked with ratanjot herb and whole spices', 360.0, 'https://images.unsplash.com/photo-1545247181-516773cae754?w=500', 1, 4.9, 0),
        ('Butter Naan', cat['Main Course'], 'Soft tandoori leavened flatbread brushed with fresh butter', 45.0, 'https://images.unsplash.com/photo-1626074353765-517a681e40be?w=500', 1, 4.7, 1),
        ('Garlic Butter Naan', cat['Main Course'], 'Tandoori flatbread topped with minced garlic, butter, and coriander', 55.0, 'https://images.unsplash.com/photo-1626074353765-517a681e40be?w=500', 1, 4.8, 1),
        ('Tandoori Roti', cat['Main Course'], 'Whole wheat flatbread baked inside hot clay tandoor', 30.0, 'https://images.unsplash.com/photo-1626074353765-517a681e40be?w=500', 1, 4.5, 1),

        # FAST FOOD (8)
        ('Classic Margherita Pizza', cat['Fast Food'], 'Classic Italian pizza with fresh mozzarella cheese, tomato basil sauce, and oregano', 260.0, 'https://images.unsplash.com/photo-1604382354936-07c5d9983bd3?w=500', 1, 4.6, 1),
        ('Loaded Chicken Pepperoni Pizza', cat['Fast Food'], 'Cheesy pizza loaded with spicy chicken pepperoni slices, jalapenos, and mozzarella', 360.0, 'https://images.unsplash.com/photo-1534308983496-4fabb1a015ee?w=500', 1, 4.8, 0),
        ('Veg Supreme Cheese Burger', cat['Fast Food'], 'Crispy veg patty burger with lettuce, tomato, cheese slice, and signature sauce', 140.0, 'https://images.unsplash.com/photo-1568901346375-23c9450c58cd?w=500', 1, 4.4, 1),
        ('Crispy Double Chicken Burger', cat['Fast Food'], 'Double fried chicken patties stacked with melted cheese, gherkins, and spicy mayo', 190.0, 'https://images.unsplash.com/photo-1586190848861-99aa4a171e90?w=500', 1, 4.7, 0),
        ('Peri Peri French Fries', cat['Fast Food'], 'Golden crispy potato fries tossed with fiery peri peri spice mix', 110.0, 'https://images.unsplash.com/photo-1573080496219-bb080dd4f877?w=500', 1, 4.5, 1),
        ('Cheesy Garlic Breadsticks', cat['Fast Food'], 'Freshly baked breadsticks brushed with garlic butter and melted mozzarella', 150.0, 'https://images.unsplash.com/photo-1573080496219-bb080dd4f877?w=500', 1, 4.6, 1),
        ('Chicken Club Sandwich', cat['Fast Food'], 'Triple-layer toasted sandwich filled with grilled chicken, egg, lettuce, and mayo', 160.0, 'https://images.unsplash.com/photo-1528735602780-2552fd46c7af?w=500', 1, 4.5, 0),
        ('Veg Grilled Cheese Toastie', cat['Fast Food'], 'Crispy toasted sandwich stuffed with spiced potatoes, cheese, and mint chutney', 120.0, 'https://images.unsplash.com/photo-1528735602780-2552fd46c7af?w=500', 1, 4.3, 1),

        # CHINESE (8)
        ('Veg Hakka Noodles', cat['Chinese'], 'Wok tossed thin noodles with crunchy julienned carrots, capsicum, and soy garlic', 160.0, 'https://images.unsplash.com/photo-1585032226651-759b368d7246?w=500', 1, 4.5, 1),
        ('Chicken Schezwan Noodles', cat['Chinese'], 'Spicy wok noodles tossed with tender shredded chicken and spicy Schezwan sauce', 190.0, 'https://images.unsplash.com/photo-1585032226651-759b368d7246?w=500', 1, 4.7, 0),
        ('Veg Manchurian Gravy', cat['Chinese'], 'Deep fried vegetable dumplings simmered in savory ginger garlic soy sauce', 170.0, 'https://images.unsplash.com/photo-1541696432-82c6da8ce7bf?w=500', 1, 4.4, 1),
        ('Chicken Chilli Gravy', cat['Chinese'], 'Boneless chicken cubes tossed with bell peppers and green chili soy sauce gravy', 220.0, 'https://images.unsplash.com/photo-1525755662778-989d0524087e?w=500', 1, 4.7, 0),
        ('Triple Schezwan Fried Rice', cat['Chinese'], 'Layered combination of Schezwan fried rice, crispy fried noodles, and spicy gravy', 230.0, 'https://images.unsplash.com/photo-1603133872878-684f208fb84b?w=500', 1, 4.8, 0),
        ('Gobi Manchurian Dry', cat['Chinese'], 'Crispy fried cauliflower florets tossed with chili garlic spring onion glaze', 150.0, 'https://images.unsplash.com/photo-1541696432-82c6da8ce7bf?w=500', 1, 4.5, 1),
        ('Dragon Chicken', cat['Chinese'], 'Stripped chicken tossed in cashew nuts, red chili paste, and spicy tangy sauce', 240.0, 'https://images.unsplash.com/photo-1525755662778-989d0524087e?w=500', 1, 4.8, 0),
        ('Honey Chilli Potato', cat['Chinese'], 'Crispy potato fingers tossed in sweet honey, chili sauce, and toasted sesame seeds', 160.0, 'https://images.unsplash.com/photo-1573080496219-bb080dd4f877?w=500', 1, 4.6, 1),

        # SOUTH INDIAN (7)
        ('Crisp Masala Dosa with Sambar', cat['South Indian'], 'Golden crispy rice crepe filled with spiced potato masala, served with coconut chutney & sambar', 110.0, 'https://images.unsplash.com/photo-1668236543090-82eba5ee5976?w=500', 1, 4.8, 1),
        ('Ghee Roast Paper Dosa', cat['South Indian'], 'Ultra-thin long crispy dosa roasted in pure desi ghee', 130.0, 'https://images.unsplash.com/photo-1668236543090-82eba5ee5976?w=500', 1, 4.7, 1),
        ('Soft Steamed Idli (3 Pcs)', cat['South Indian'], 'Fluffy steamed rice lentil cakes served hot with spicy sambar and fresh chutney', 70.0, 'https://images.unsplash.com/photo-1589301760014-d929f3979dbc?w=500', 1, 4.5, 1),
        ('Medu Vada (2 Pcs)', cat['South Indian'], 'Crispy fried savory lentil donuts infused with black pepper and ginger', 80.0, 'https://images.unsplash.com/photo-1589301760014-d929f3979dbc?w=500', 1, 4.6, 1),
        ('Onion Rava Masala Dosa', cat['South Indian'], 'Crispy semolina crepe studded with chopped onions and spiced potato filling', 140.0, 'https://images.unsplash.com/photo-1668236543090-82eba5ee5976?w=500', 1, 4.6, 1),
        ('Chettinad Chicken Curry', cat['South Indian'], 'Fiery South Indian chicken curry cooked with freshly roasted black pepper and coconut', 260.0, 'https://images.unsplash.com/photo-1588166524941-3bf61a9c41db?w=500', 1, 4.8, 0),
        ('Malabar Parotta with Veg Kurma', cat['South Indian'], 'Flaky layered Kerala parotta served with aromatic coconut veg kurma gravy', 150.0, 'https://images.unsplash.com/photo-1626074353765-517a681e40be?w=500', 1, 4.7, 1),

        # DESSERTS (7)
        ('Warm Chocolate Lava Cake', cat['Desserts'], 'Rich chocolate cake with a warm gooey molten chocolate center', 160.0, 'https://images.unsplash.com/photo-1606313564200-e75d5e30476c?w=500', 1, 4.9, 1),
        ('Chocolate Brownie Sundae', cat['Desserts'], 'Warm fudge chocolate brownie topped with vanilla ice cream and hot chocolate fudge', 170.0, 'https://images.unsplash.com/photo-1564355808539-22fda35bed7e?w=500', 1, 4.9, 1),
        ('Soft Gulab Jamun (2 Pcs)', cat['Desserts'], 'Soft fried milk dumplings soaked in cardamom flavored warm sugar syrup', 90.0, 'https://images.unsplash.com/photo-1589301760014-d929f3979dbc?w=500', 1, 4.8, 1),
        ('Authentic Royal Rasmalai (2 Pcs)', cat['Desserts'], 'Soft cottage cheese discs soaked in chilled saffron cardamom milk topped with pistachios', 110.0, 'https://images.unsplash.com/photo-1589301760014-d929f3979dbc?w=500', 1, 4.8, 1),
        ('New York Cheesecake Slice', cat['Desserts'], 'Creamy baked cheesecake slice on graham cracker crust served with strawberry compote', 220.0, 'https://images.unsplash.com/photo-1533134242443-d4fd215305ad?w=500', 1, 4.8, 1),
        ('Matka Kulfi Special', cat['Desserts'], 'Traditional dense Indian pistachio saffron ice cream served in clay pot', 100.0, 'https://images.unsplash.com/photo-1563805042-7684c019e1cb?w=500', 1, 4.7, 1),
        ('Belgian Chocolate Waffle', cat['Desserts'], 'Crispy warm Belgian waffle drenched in melted dark and milk chocolate glaze', 180.0, 'https://images.unsplash.com/photo-1562376552-0d160a2f238d?w=500', 1, 4.8, 1),

        # BEVERAGES (5)
        ('Chilled Coca Cola (500ml)', cat['Beverages'], 'Refreshing carbonated cola beverage served ice cold', 50.0, 'https://images.unsplash.com/photo-1622483767028-3f66f32aef97?w=500', 1, 4.5, 1),
        ('Fresh Mint Mojito', cat['Beverages'], 'Refreshing sparkling mocktail made with fresh crushed mint leaves, lime juice, and soda', 120.0, 'https://images.unsplash.com/photo-1513558161293-cdaf765ed2fd?w=500', 1, 4.7, 1),
        ('Thick Chocolate Milkshake', cat['Beverages'], 'Creamy thick milkshake blended with cocoa powder, milk, and chocolate ice cream', 150.0, 'https://images.unsplash.com/photo-1572490122747-3968b75cc699?w=500', 1, 4.8, 1),
        ('Refreshing Fresh Lime Soda', cat['Beverages'], 'Sparkling water infused with fresh lime juice, mint leaves, and rock salt', 70.0, 'https://images.unsplash.com/photo-1513558161293-cdaf765ed2fd?w=500', 1, 4.6, 1),
        ('Cold Coffee with Ice Cream', cat['Beverages'], 'Blended rich espresso cold coffee topped with a scoop of vanilla ice cream', 140.0, 'https://images.unsplash.com/photo-1517701604599-bb29b565090c?w=500', 1, 4.8, 1)
    ]

    cursor.executemany("""
        INSERT INTO foods (name, category_id, description, price, image, is_available, rating, is_veg)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, foods)

    print("Seeding Orders & Payments...")
    cursor.execute("SELECT id FROM users WHERE role='customer'")
    customer_ids = [r[0] for r in cursor.fetchall()]

    cursor.execute("SELECT id, name, price FROM foods")
    food_list = cursor.fetchall()

    statuses = ['Completed', 'Completed', 'Preparing', 'Ready', 'Confirmed', 'Pending']
    payment_methods = ['UPI', 'Card', 'Cash on Delivery', 'Demo Payment']

    now = datetime.now()

    for i in range(1, 35):
        cust_id = random.choice(customer_ids)
        cursor.execute("SELECT name, address FROM users WHERE id=?", (cust_id,))
        c_name, c_addr = cursor.fetchone()

        order_date = (now - timedelta(days=random.randint(0, 14), hours=random.randint(1, 12))).strftime('%Y-%m-%d %H:%M:%S')
        selected_foods = random.sample(food_list, random.randint(1, 5))
        
        subtotal = 0
        items_to_insert = []
        for f in selected_foods:
            qty = random.randint(1, 3)
            item_sub = f[2] * qty
            subtotal += item_sub
            items_to_insert.append((f[0], f[1], qty, f[2], item_sub))

        tax = round(subtotal * 0.05, 2)
        grand = round(subtotal + tax, 2)
        status = random.choice(statuses)
        pay_status = 'PAID' if status in ['Completed', 'Ready', 'Preparing', 'Confirmed'] else 'UNPAID'

        cursor.execute("""
            INSERT INTO orders (user_id, customer_name, total_amount, tax_amount, grand_total, status, payment_status, order_date, delivery_address)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (cust_id, c_name, subtotal, tax, grand, status, pay_status, order_date, c_addr))
        order_id = cursor.lastrowid

        for item in items_to_insert:
            cursor.execute("""
                INSERT INTO order_items (order_id, food_id, food_name, quantity, price, subtotal)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (order_id, item[0], item[1], item[2], item[3], item[4]))

        if pay_status == 'PAID':
            pay_method = random.choice(payment_methods)
            tx_id = f"DEMO{random.randint(100000, 999999)}"
            cursor.execute("""
                INSERT INTO payments (order_id, payment_method, transaction_id, amount, status, payment_date)
                VALUES (?, ?, ?, ?, 'PAID', ?)
            """, (order_id, pay_method, tx_id, grand, order_date))

    print("Seeding Reviews...")
    reviews = [
        (2, 1, 5, "Best Hyderabadi Biryani in town! Perfectly spiced and soft meat."),
        (2, 8, 4, "Chicken 65 was hot and fresh. Loved the curry leaf aroma."),
        (3, 34, 5, "Crust was crispy and cheese melted in mouth. Fantastic pizza."),
        (4, 17, 5, "Royal Butter Chicken curry with Garlic Naan is a match made in heaven.")
    ]
    cursor.executemany("""
        INSERT INTO reviews (user_id, food_id, rating, comment)
        VALUES (?, ?, ?, ?)
    """, reviews)

    conn.commit()
    conn.close()
    print("Database successfully seeded with 60 food items and realistic demo data!")

if __name__ == '__main__':
    seed_database()
