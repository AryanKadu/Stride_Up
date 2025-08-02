# 🚀 Django App Deployment Guide

## ✅ Login/Signup Deployment Status

Your login and signup functionality **WILL work** after deployment, but you need to make these critical changes:

## 🔧 Required Changes for Production

### 1. **Environment Variables** (CRITICAL)
Set these environment variables on your hosting platform:

```bash
# Security
SECRET_KEY=your-super-secret-key-here
DEBUG=False

# Database (if using PostgreSQL)
DB_NAME=your_db_name
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=your_db_host
DB_PORT=5432

# Allowed hosts
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
```

### 2. **Database Migration**
```bash
# Run migrations on production
python manage.py migrate

# Create superuser
python manage.py createsuperuser
```

### 3. **Static Files**
```bash
# Collect static files
python manage.py collectstatic
```

## 🌐 Deployment Platforms

### **Heroku**
```bash
# Install Heroku CLI
# Create Procfile
echo "web: gunicorn pbl.wsgi --log-file -" > Procfile

# Deploy
git add .
git commit -m "Production ready"
git push heroku main

# Run migrations
heroku run python manage.py migrate
```

### **Railway**
```bash
# Connect your GitHub repo
# Set environment variables in Railway dashboard
# Deploy automatically
```

### **Render**
```bash
# Connect your GitHub repo
# Set environment variables
# Build command: pip install -r requirements.txt
# Start command: gunicorn pbl.wsgi:application
```

## 🔒 Security Checklist

- [ ] `DEBUG = False` in production
- [ ] `SECRET_KEY` set as environment variable
- [ ] `ALLOWED_HOSTS` configured
- [ ] HTTPS enabled
- [ ] Database credentials secured
- [ ] Static files collected
- [ ] Migrations run

## 🧪 Testing Login/Signup

After deployment, test these URLs:
- Login: `https://yourdomain.com/users/login/`
- Signup: `https://yourdomain.com/users/signup/`
- Dashboard: `https://yourdomain.com/dashboard/`

## ⚠️ Common Issues & Solutions

### Issue: "CSRF verification failed"
**Solution**: Ensure `CSRF_COOKIE_SECURE = True` and HTTPS is enabled

### Issue: "Static files not found"
**Solution**: Run `python manage.py collectstatic` and configure static file serving

### Issue: "Database connection failed"
**Solution**: Check database credentials and connection settings

### Issue: "Login redirects to wrong URL"
**Solution**: Verify `LOGIN_REDIRECT_URL` and `LOGOUT_REDIRECT_URL` settings

## 📝 Environment Variables Template

Create a `.env` file (don't commit to git):
```env
SECRET_KEY=your-super-secret-key-here
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
DB_NAME=your_db_name
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=your_db_host
DB_PORT=5432
USDA_API_KEY=your-usda-api-key
```

## 🎯 Quick Deployment Commands

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Set environment variables
export SECRET_KEY="your-secret-key"
export DEBUG="False"

# 3. Run migrations
python manage.py migrate

# 4. Collect static files
python manage.py collectstatic --noinput

# 5. Create superuser
python manage.py createsuperuser

# 6. Run with gunicorn
gunicorn pbl.wsgi:application --bind 0.0.0.0:8000
```

Your login/signup will work perfectly after following these steps! 🎉 