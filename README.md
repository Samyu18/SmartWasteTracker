
# Smart Waste Tracker

A web application for retail stores to track, predict, and minimize inventory waste using Python, Flask, and advanced data structures.

## Features
- **Inventory Management**: Track items by category, quantity, and shelf life
- **Waste Prediction**: Predict surplus items using demand forecasting (sliding window algorithm)
- **Smart Recommendations**: Suggest donation, repurposing, or recycling plans
- **Analytics Dashboard**: Visualize waste reduction metrics and trends
- **User Authentication**: Secure login and signup system
- **Optimization**: Space-time efficiency using hash maps and priority queues

## Tech Stack
- **Backend**: Python, Flask, SQLAlchemy
- **Frontend**: HTML, CSS, Bootstrap, JavaScript
- **Database**: SQLite (development), PostgreSQL (production)
- **Data Structures**: Hash Maps, Priority Queues, Sliding Windows
- **Machine Learning**: Pandas, Scikit-learn for analytics

## Local Development Setup

### Prerequisites
- Python 3.11 or higher
- pip (Python package installer)

### Installation
1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/smart-waste-tracker.git
   cd smart-waste-tracker
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Initialize the database**
   ```bash
   python init_db.py
   ```

5. **Run the application**
   ```bash
   python app.py
   ```

6. **Open in browser**
   Visit [http://127.0.0.1:5000](http://127.0.0.1:5000)

## Deployment

### GitHub Pages (Static Frontend)
This is a Flask application, so GitHub Pages won't work directly. Consider these alternatives:

### Heroku Deployment
1. **Install Heroku CLI**
2. **Login to Heroku**
   ```bash
   heroku login
   ```

3. **Create Heroku app**
   ```bash
   heroku create your-app-name
   ```

4. **Set environment variables**
   ```bash
   heroku config:set SECRET_KEY=your-secret-key-here
   heroku config:set DATABASE_URL=postgresql://your-database-url
   ```

5. **Deploy**
   ```bash
   git add .
   git commit -m "Deploy to Heroku"
   git push heroku main
   ```

### Railway Deployment
1. **Connect your GitHub repository to Railway**
2. **Set environment variables in Railway dashboard**
3. **Deploy automatically on push**

### Render Deployment
1. **Connect your GitHub repository to Render**
2. **Create a new Web Service**
3. **Set build command**: `pip install -r requirements.txt`
4. **Set start command**: `gunicorn app:app`
5. **Set environment variables**

### Environment Variables
For production deployment, set these environment variables:
- `SECRET_KEY`: A secure random string for session encryption
- `DATABASE_URL`: Your database connection string
- `PORT`: Port number (usually set by deployment platform)

## Project Structure
```
smart-waste-tracker/
├── app.py                 # Main Flask application
├── models.py              # SQLAlchemy database models
├── init_db.py             # Database initialization script
├── requirements.txt       # Python dependencies
├── Procfile              # Heroku deployment configuration
├── runtime.txt           # Python version specification
├── .gitignore           # Git ignore rules
├── README.md            # Project documentation
├── templates/           # HTML templates
│   ├── dashboard.html
│   ├── inventory.html
│   ├── recommendations.html
│   ├── analytics.html
│   ├── login.html
│   └── signup.html
└── static/              # Static files (CSS, JS, images)
    ├── css/
    └── js/
```

## Data Structures Used
- **Hash Maps**: For category-based item lookup and analytics
- **Priority Queues**: For managing soon-to-expire items
- **Sliding Windows**: For demand forecasting and surplus prediction

## Contributing
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support
For support, email support@smartwastetracker.com or create an issue in this repository. 
>>>>>>> 44499eb (Initial commit)
