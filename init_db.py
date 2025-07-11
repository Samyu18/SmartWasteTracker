from app import app, db
from models import User, Item
from werkzeug.security import generate_password_hash
import os
from datetime import datetime, timedelta

def init_database():
    with app.app_context():
        # Drop all tables and recreate them for a clean slate (for demo purposes)
        db.drop_all()
        db.create_all()
        
        # Create sample users
        users = [
            {'username': 'admin', 'email': 'admin@smartwastetracker.com', 'password': 'admin123'},
            {'username': 'alice', 'email': 'alice@example.com', 'password': 'alicepass'},
            {'username': 'bob', 'email': 'bob@example.com', 'password': 'bobpass'},
            {'username': 'carol', 'email': 'carol@example.com', 'password': 'carolpass'}
        ]
        user_objs = []
        for u in users:
            user = User(username=u['username'], email=u['email'])
            user.set_password(u['password'])
            db.session.add(user)
            user_objs.append(user)
        db.session.commit()
        print("Sample users created:")
        for u in user_objs:
            print(f"Username: {u.username}, Password: (see code)")
        # Add even more diverse sample items for each user
        sample_items_per_user = [
            [ # admin
                {'name': 'Milk', 'category': 'Dairy', 'quantity': 2, 'shelf_life': 7, 'location': 'Fridge'},
                {'name': 'Bread', 'category': 'Bakery', 'quantity': 1, 'shelf_life': 3, 'location': 'Pantry'},
                {'name': 'Eggs', 'category': 'Dairy', 'quantity': 12, 'shelf_life': 14, 'location': 'Fridge'},
                {'name': 'Apple', 'category': 'Fruit', 'quantity': 6, 'shelf_life': 10, 'location': 'Fridge'},
                {'name': 'Chicken', 'category': 'Meat', 'quantity': 1, 'shelf_life': 5, 'location': 'Freezer'},
                {'name': 'Orange Juice', 'category': 'Beverages', 'quantity': 2, 'shelf_life': 14, 'location': 'Fridge'},
                {'name': 'Rice', 'category': 'Grains', 'quantity': 5, 'shelf_life': 180, 'location': 'Pantry'},
                {'name': 'Spinach', 'category': 'Vegetable', 'quantity': 8, 'shelf_life': 5, 'location': 'Fridge'},
                {'name': 'Yogurt', 'category': 'Dairy', 'quantity': 4, 'shelf_life': 10, 'location': 'Fridge'},
                {'name': 'Cereal', 'category': 'Grains', 'quantity': 3, 'shelf_life': 365, 'location': 'Pantry'},
                {'name': 'Butter', 'category': 'Dairy', 'quantity': 2, 'shelf_life': 60, 'location': 'Fridge'},
                {'name': 'Soup', 'category': 'Canned', 'quantity': 5, 'shelf_life': 730, 'location': 'Pantry'},
                {'name': 'Ice Cream', 'category': 'Frozen', 'quantity': 2, 'shelf_life': 180, 'location': 'Freezer'},
                {'name': 'Lettuce', 'category': 'Vegetable', 'quantity': 3, 'shelf_life': 5, 'location': 'Fridge'},
                {'name': 'Tomato', 'category': 'Vegetable', 'quantity': 10, 'shelf_life': 7, 'location': 'Fridge'},
                {'name': 'Fish', 'category': 'Meat', 'quantity': 2, 'shelf_life': 3, 'location': 'Freezer'},
                {'name': 'Potato', 'category': 'Vegetable', 'quantity': 15, 'shelf_life': 30, 'location': 'Pantry'},
                {'name': 'Soda', 'category': 'Beverages', 'quantity': 6, 'shelf_life': 365, 'location': 'Pantry'},
                {'name': 'Banana', 'category': 'Fruit', 'quantity': 8, 'shelf_life': 5, 'location': 'Fridge'},
                {'name': 'Carrot', 'category': 'Vegetable', 'quantity': 12, 'shelf_life': 20, 'location': 'Fridge'}
            ],
            [ # alice
                {'name': 'Cheese', 'category': 'Dairy', 'quantity': 3, 'shelf_life': 30, 'location': 'Fridge'},
                {'name': 'Chicken Nuggets', 'category': 'Frozen', 'quantity': 1, 'shelf_life': 90, 'location': 'Freezer'},
                {'name': 'Apple Juice', 'category': 'Beverages', 'quantity': 3, 'shelf_life': 30, 'location': 'Fridge'},
                {'name': 'Beans', 'category': 'Canned', 'quantity': 8, 'shelf_life': 730, 'location': 'Pantry'},
                {'name': 'Pasta', 'category': 'Grains', 'quantity': 4, 'shelf_life': 365, 'location': 'Pantry'},
                {'name': 'Spinach', 'category': 'Vegetable', 'quantity': 5, 'shelf_life': 7, 'location': 'Fridge'},
                {'name': 'Butter', 'category': 'Dairy', 'quantity': 2, 'shelf_life': 60, 'location': 'Fridge'},
                {'name': 'Pear', 'category': 'Fruit', 'quantity': 7, 'shelf_life': 7, 'location': 'Fridge'},
                {'name': 'Ham', 'category': 'Meat', 'quantity': 1, 'shelf_life': 10, 'location': 'Fridge'},
                {'name': 'Soup', 'category': 'Canned', 'quantity': 5, 'shelf_life': 730, 'location': 'Pantry'},
                {'name': 'Ice Cream', 'category': 'Frozen', 'quantity': 2, 'shelf_life': 180, 'location': 'Freezer'},
                {'name': 'Watermelon', 'category': 'Fruit', 'quantity': 1, 'shelf_life': 5, 'location': 'Fridge'},
                {'name': 'Lettuce', 'category': 'Vegetable', 'quantity': 3, 'shelf_life': 5, 'location': 'Fridge'},
                {'name': 'Cereal', 'category': 'Grains', 'quantity': 2, 'shelf_life': 365, 'location': 'Pantry'},
                {'name': 'Orange', 'category': 'Fruit', 'quantity': 10, 'shelf_life': 14, 'location': 'Fridge'},
                {'name': 'Broccoli', 'category': 'Vegetable', 'quantity': 4, 'shelf_life': 7, 'location': 'Fridge'},
                {'name': 'Granola Bar', 'category': 'Snacks', 'quantity': 12, 'shelf_life': 180, 'location': 'Pantry'},
                {'name': 'Coffee', 'category': 'Beverages', 'quantity': 1, 'shelf_life': 365, 'location': 'Pantry'},
                {'name': 'Eggplant', 'category': 'Vegetable', 'quantity': 2, 'shelf_life': 10, 'location': 'Fridge'},
                {'name': 'Mushroom', 'category': 'Vegetable', 'quantity': 6, 'shelf_life': 5, 'location': 'Fridge'}
            ],
            [ # bob
                {'name': 'Yogurt', 'category': 'Dairy', 'quantity': 6, 'shelf_life': 14, 'location': 'Fridge'},
                {'name': 'Chicken Breast', 'category': 'Meat', 'quantity': 2, 'shelf_life': 7, 'location': 'Freezer'},
                {'name': 'Rice', 'category': 'Grains', 'quantity': 10, 'shelf_life': 365, 'location': 'Pantry'},
                {'name': 'Tomato Sauce', 'category': 'Canned', 'quantity': 4, 'shelf_life': 365, 'location': 'Pantry'},
                {'name': 'Apple', 'category': 'Fruit', 'quantity': 10, 'shelf_life': 10, 'location': 'Fridge'},
                {'name': 'Banana', 'category': 'Fruit', 'quantity': 12, 'shelf_life': 5, 'location': 'Fridge'},
                {'name': 'Carrot', 'category': 'Vegetable', 'quantity': 10, 'shelf_life': 20, 'location': 'Fridge'},
                {'name': 'Cucumber', 'category': 'Vegetable', 'quantity': 8, 'shelf_life': 7, 'location': 'Fridge'},
                {'name': 'Granola', 'category': 'Snacks', 'quantity': 5, 'shelf_life': 120, 'location': 'Pantry'},
                {'name': 'Milk', 'category': 'Dairy', 'quantity': 3, 'shelf_life': 7, 'location': 'Fridge'},
                {'name': 'Eggs', 'category': 'Dairy', 'quantity': 18, 'shelf_life': 14, 'location': 'Fridge'},
                {'name': 'Orange Juice', 'category': 'Beverages', 'quantity': 2, 'shelf_life': 14, 'location': 'Fridge'},
                {'name': 'Potato Chips', 'category': 'Snacks', 'quantity': 4, 'shelf_life': 90, 'location': 'Pantry'},
                {'name': 'Peanut Butter', 'category': 'Snacks', 'quantity': 1, 'shelf_life': 365, 'location': 'Pantry'},
                {'name': 'Celery', 'category': 'Vegetable', 'quantity': 3, 'shelf_life': 10, 'location': 'Fridge'},
                {'name': 'Strawberry', 'category': 'Fruit', 'quantity': 15, 'shelf_life': 5, 'location': 'Fridge'},
                {'name': 'Ham', 'category': 'Meat', 'quantity': 1, 'shelf_life': 10, 'location': 'Fridge'},
                {'name': 'Soup', 'category': 'Canned', 'quantity': 3, 'shelf_life': 730, 'location': 'Pantry'},
                {'name': 'Ice Cream', 'category': 'Frozen', 'quantity': 2, 'shelf_life': 180, 'location': 'Freezer'},
                {'name': 'Lettuce', 'category': 'Vegetable', 'quantity': 2, 'shelf_life': 5, 'location': 'Fridge'}
            ],
            [ # carol
                {'name': 'Butter', 'category': 'Dairy', 'quantity': 2, 'shelf_life': 60, 'location': 'Fridge'},
                {'name': 'Pear', 'category': 'Fruit', 'quantity': 7, 'shelf_life': 7, 'location': 'Fridge'},
                {'name': 'Ham', 'category': 'Meat', 'quantity': 1, 'shelf_life': 10, 'location': 'Fridge'},
                {'name': 'Soup', 'category': 'Canned', 'quantity': 5, 'shelf_life': 730, 'location': 'Pantry'},
                {'name': 'Ice Cream', 'category': 'Frozen', 'quantity': 2, 'shelf_life': 180, 'location': 'Freezer'},
                {'name': 'Watermelon', 'category': 'Fruit', 'quantity': 1, 'shelf_life': 5, 'location': 'Fridge'},
                {'name': 'Lettuce', 'category': 'Vegetable', 'quantity': 3, 'shelf_life': 5, 'location': 'Fridge'},
                {'name': 'Cereal', 'category': 'Grains', 'quantity': 2, 'shelf_life': 365, 'location': 'Pantry'},
                {'name': 'Orange', 'category': 'Fruit', 'quantity': 10, 'shelf_life': 14, 'location': 'Fridge'},
                {'name': 'Broccoli', 'category': 'Vegetable', 'quantity': 4, 'shelf_life': 7, 'location': 'Fridge'},
                {'name': 'Granola Bar', 'category': 'Snacks', 'quantity': 12, 'shelf_life': 180, 'location': 'Pantry'},
                {'name': 'Coffee', 'category': 'Beverages', 'quantity': 1, 'shelf_life': 365, 'location': 'Pantry'},
                {'name': 'Eggplant', 'category': 'Vegetable', 'quantity': 2, 'shelf_life': 10, 'location': 'Fridge'},
                {'name': 'Mushroom', 'category': 'Vegetable', 'quantity': 6, 'shelf_life': 5, 'location': 'Fridge'},
                {'name': 'Yogurt', 'category': 'Dairy', 'quantity': 4, 'shelf_life': 10, 'location': 'Fridge'},
                {'name': 'Chicken', 'category': 'Meat', 'quantity': 2, 'shelf_life': 5, 'location': 'Freezer'},
                {'name': 'Apple', 'category': 'Fruit', 'quantity': 8, 'shelf_life': 10, 'location': 'Fridge'},
                {'name': 'Banana', 'category': 'Fruit', 'quantity': 10, 'shelf_life': 5, 'location': 'Fridge'},
                {'name': 'Carrot', 'category': 'Vegetable', 'quantity': 10, 'shelf_life': 20, 'location': 'Fridge'},
                {'name': 'Cucumber', 'category': 'Vegetable', 'quantity': 8, 'shelf_life': 7, 'location': 'Fridge'}
            ]
        ]
        for idx, user in enumerate(user_objs):
            for item in sample_items_per_user[idx]:
                added_date = datetime.utcnow() - timedelta(days=idx)
                expiry_date = added_date + timedelta(days=item['shelf_life'])
                db_item = Item(
                    name=item['name'],
                    category=item['category'],
                    quantity=item['quantity'],
                    shelf_life=item['shelf_life'],
                    location=item['location'],
                    added_date=added_date,
                    expiry_date=expiry_date,
                    user_id=user.id
                )
                db.session.add(db_item)
        db.session.commit()
        print("More diverse sample items added for each user.")
        print("Database initialized successfully!")

if __name__ == '__main__':
    init_database() 