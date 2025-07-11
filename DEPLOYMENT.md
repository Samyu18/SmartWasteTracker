# Deployment Guide

This guide will help you deploy the Smart Waste Tracker application to various platforms.

## Quick Deploy Options

### 1. Heroku (Recommended for beginners)

#### Option A: One-Click Deploy
[![Deploy to Heroku](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/yourusername/smart-waste-tracker)

#### Option B: Manual Deploy
1. **Install Heroku CLI**
   ```bash
   # macOS
   brew tap heroku/brew && brew install heroku
   
   # Windows
   # Download from https://devcenter.heroku.com/articles/heroku-cli
   ```

2. **Login to Heroku**
   ```bash
   heroku login
   ```

3. **Create Heroku app**
   ```bash
   heroku create your-app-name
   ```

4. **Add PostgreSQL database**
   ```bash
   heroku addons:create heroku-postgresql:hobby-dev
   ```

5. **Set environment variables**
   ```bash
   heroku config:set SECRET_KEY=$(python -c "import secrets; print(secrets.token_hex(16))")
   ```

6. **Deploy**
   ```bash
   git add .
   git commit -m "Deploy to Heroku"
   git push heroku main
   ```

7. **Initialize database**
   ```bash
   heroku run python init_db.py
   ```

### 2. Railway

1. **Go to [Railway](https://railway.app)**
2. **Connect your GitHub account**
3. **Click "New Project" → "Deploy from GitHub repo"**
4. **Select your repository**
5. **Set environment variables in the dashboard:**
   - `SECRET_KEY`: Generate a random string
   - `DATABASE_URL`: Railway will provide this automatically
6. **Deploy automatically on push**

### 3. Render

1. **Go to [Render](https://render.com)**
2. **Connect your GitHub account**
3. **Click "New" → "Web Service"**
4. **Connect your repository**
5. **Configure:**
   - **Name**: smart-waste-tracker
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
6. **Set environment variables**
7. **Deploy**

### 4. PythonAnywhere

1. **Create account at [PythonAnywhere](https://www.pythonanywhere.com)**
2. **Go to "Web" tab**
3. **Add a new web app**
4. **Choose "Flask" and Python 3.11**
5. **Upload your files or clone from GitHub**
6. **Install requirements:**
   ```bash
   pip install -r requirements.txt
   ```
7. **Set up WSGI file**
8. **Configure environment variables**

## Environment Variables

Set these environment variables for production:

```bash
SECRET_KEY=your-secure-random-string-here
DATABASE_URL=your-database-connection-string
PORT=5000  # Usually set by platform
```

## Database Setup

### SQLite (Development)
- Default for local development
- No additional setup required

### PostgreSQL (Production)
- Recommended for production deployments
- Heroku, Railway, and Render provide PostgreSQL automatically
- For manual setup:
  ```bash
  # Install PostgreSQL
  # Create database
  # Set DATABASE_URL environment variable
  ```

## Troubleshooting

### Common Issues

1. **Import Error: No module named 'flask'**
   - Solution: Ensure requirements.txt is properly installed
   - Run: `pip install -r requirements.txt`

2. **Database connection error**
   - Solution: Check DATABASE_URL environment variable
   - Ensure database is accessible

3. **Port already in use**
   - Solution: Use environment variable PORT
   - Or change port in app.py

4. **Static files not loading**
   - Solution: Ensure static folder structure is correct
   - Check file permissions

### Debug Mode

For debugging, temporarily enable debug mode:
```python
app.run(debug=True)
```

**Warning**: Never use debug=True in production!

## Security Considerations

1. **Change default admin credentials**
   - Default: admin/admin123
   - Change immediately after deployment

2. **Use strong SECRET_KEY**
   - Generate using: `python -c "import secrets; print(secrets.token_hex(16))"`

3. **Enable HTTPS**
   - Most platforms provide this automatically

4. **Database security**
   - Use environment variables for database credentials
   - Never commit database files to version control

## Monitoring

### Logs
- Heroku: `heroku logs --tail`
- Railway: View in dashboard
- Render: View in dashboard

### Health Check
Add a health check endpoint:
```python
@app.route('/health')
def health():
    return jsonify({'status': 'healthy'})
```

## Performance Optimization

1. **Database indexing**
2. **Caching strategies**
3. **CDN for static files**
4. **Load balancing (for high traffic)**

## Backup Strategy

1. **Database backups**
2. **Code version control**
3. **Environment variable backups**
4. **Regular testing of restore procedures** 