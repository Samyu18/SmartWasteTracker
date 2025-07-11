from flask import Flask, render_template, request, redirect, url_for, jsonify, session, flash
from datetime import datetime, timedelta
import heapq
import pandas as pd
from collections import defaultdict, deque
from models import db, Item, User
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///waste_tracker.db')
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'supersecretkey')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

def login_required(f):
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        if User.query.filter((User.username==username)|(User.email==email)).first():
            flash('Username or email already exists!')
            return render_template('signup.html')
        user = User(username=username, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        flash('Signup successful! Please log in.')
        return redirect(url_for('login'))
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            session['user_id'] = user.id
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password!')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('Logged out successfully!')
    return redirect(url_for('login'))

# --- DSA Structures ---
# Hash map for category lookup
def get_category_map():
    items = Item.query.filter_by(user_id=session['user_id']).all()
    category_map = defaultdict(list)
    for item in items:
        category_map[item.category].append(item)
    return category_map

# Priority queue for soon-to-expire items
def get_expiry_queue():
    items = Item.query.filter_by(user_id=session['user_id']).all()
    pq = []
    for item in items:
        heapq.heappush(pq, (item.expiry_date, item))
    return pq

# Sliding window for demand forecasting
def forecast_surplus(window_days=7):
    items = Item.query.filter_by(user_id=session['user_id']).all()
    df = pd.DataFrame([
        {'name': i.name, 'category': i.category, 'quantity': i.quantity, 'added_date': i.added_date} for i in items
    ])
    if df.empty:
        return []
    df['added_date'] = pd.to_datetime(df['added_date'])
    now = datetime.now()
    window_start = now - timedelta(days=window_days)
    recent = df[df['added_date'] >= window_start]
    surplus = recent.groupby('name').sum(numeric_only=True)
    # If quantity added in window > threshold, flag as surplus
    surplus_items = surplus[surplus['quantity'] > 10].index.tolist()  # threshold=10 for demo
    return surplus_items

# --- Routes ---
@app.route('/')
@login_required
def dashboard():
    items = Item.query.filter_by(user_id=session['user_id']).all()
    surplus = forecast_surplus()
    expiry_pq = get_expiry_queue()
    soon_expiring = [heapq.heappop(expiry_pq)[1] for _ in range(min(5, len(expiry_pq)))]
    return render_template('dashboard.html', items=items, surplus=surplus, soon_expiring=soon_expiring, now=datetime.now(), timedelta=timedelta)

@app.route('/inventory')
@login_required
def inventory():
    items = Item.query.filter_by(user_id=session['user_id']).all()
    surplus = forecast_surplus()
    return render_template('inventory.html', items=items, surplus=surplus, now=datetime.now(), timedelta=timedelta)

@app.route('/add_item', methods=['POST'])
def add_item():
    name = request.form['name']
    category = request.form['category']
    quantity = int(request.form['quantity'])
    shelf_life = int(request.form['shelf_life'])
    location = request.form['location']
    added_date = datetime.now()
    expiry_date = added_date + timedelta(days=shelf_life)
    item = Item(name=name, category=category, quantity=quantity, shelf_life=shelf_life, location=location, added_date=added_date, expiry_date=expiry_date, user_id=session['user_id'])
    db.session.add(item)
    db.session.commit()
    return redirect(url_for('inventory'))

@app.route('/recommendations')
@login_required
def recommendations():
    surplus = forecast_surplus()
    expiry_pq = get_expiry_queue()
    soon_expiring = [heapq.heappop(expiry_pq)[1] for _ in range(min(10, len(expiry_pq)))]
    recs = []
    for item in soon_expiring:
        recs.append({'item': item, 'action': 'Donate'})
    for name in surplus:
        item = Item.query.filter_by(name=name, user_id=session['user_id']).first()
        if item:
            if item.category in ['Canned', 'Beverages', 'Frozen']:
                recs.append({'item': item, 'action': 'Recycle'})
            else:
                recs.append({'item': item, 'action': 'Repurpose'})
    return render_template('recommendations.html', recs=recs, now=datetime.now(), timedelta=timedelta)

@app.route('/analytics')
@login_required
def analytics():
    items = Item.query.filter_by(user_id=session['user_id']).all()
    category_map = get_category_map()
    
    # Calculate analytics
    total_items = len(items)
    total_quantity = sum(item.quantity for item in items)
    categories = list(category_map.keys())
    category_counts = {cat: len(category_map[cat]) for cat in categories}
    
    # Waste reduction metrics
    surplus = forecast_surplus()
    expiry_pq = get_expiry_queue()
    soon_expiring = [heapq.heappop(expiry_pq)[1] for _ in range(min(10, len(expiry_pq)))]
    
    # Recommendation breakdown
    donate_count = 0
    repurpose_count = 0
    recycle_count = 0
    for item in soon_expiring:
        donate_count += 1
    for name in surplus:
        item = Item.query.filter_by(name=name, user_id=session['user_id']).first()
        if item:
            if item.category in ['Canned', 'Beverages', 'Frozen']:
                recycle_count += 1
            else:
                repurpose_count += 1
    
    waste_reduction = {
        'total_items': total_items,
        'surplus_items': len(surplus),
        'expiring_soon': len(soon_expiring),
        'categories': categories,
        'category_counts': category_counts,
        'total_quantity': total_quantity,
        'donate_count': donate_count,
        'repurpose_count': repurpose_count,
        'recycle_count': recycle_count
    }
    
    return render_template('analytics.html', analytics=waste_reduction, items=items, now=datetime.now(), timedelta=timedelta)

@app.route('/delete_item/<int:item_id>')
def delete_item(item_id):
    item = Item.query.filter_by(id=item_id, user_id=session.get('user_id')).first()
    if item:
        db.session.delete(item)
        db.session.commit()
    return redirect(url_for('inventory'))

@app.route('/update_quantity/<int:item_id>', methods=['POST'])
def update_quantity(item_id):
    item = Item.query.filter_by(id=item_id, user_id=session.get('user_id')).first()
    if item:
        new_quantity = int(request.form['quantity'])
        item.quantity = new_quantity
        db.session.commit()
    return redirect(url_for('inventory'))

@app.route('/mark_complete/<int:item_id>', methods=['POST'])
def mark_complete(item_id):
    item = Item.query.filter_by(id=item_id, user_id=session.get('user_id')).first()
    if item:
        db.session.delete(item)
        db.session.commit()
    return jsonify({'success': True})

@app.route('/delete_selected', methods=['POST'])
def delete_selected():
    item_ids = request.form.getlist('item_ids')
    for item_id in item_ids:
        item = Item.query.filter_by(id=item_id, user_id=session.get('user_id')).first()
        if item:
            db.session.delete(item)
    db.session.commit()
    return redirect(url_for('inventory'))

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5051))
    app.run(host='0.0.0.0', port=port, debug=False) 