# 🚀 StartSmart - Production Deployment Guide

## 🔧 Pre-Deployment Checklist

### 1. Environment Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Create .env file with your production settings
cp .env.example .env
# Edit .env with your actual values
```

### 2. Security Configuration
- ✅ Set strong SECRET_KEY in .env
- ✅ Configure HTTPS (if using reverse proxy)
- ✅ Set FLASK_ENV=production
- ✅ Review database permissions

### 3. Database Preparation
```bash
# Create database backup
python backup_system.py

# Verify database integrity
python -c "from backup_system import verify_database; verify_database()"
```

## 🌐 Deployment Options

### Option 1: Heroku Deployment
```bash
# Login to Heroku
heroku login

# Create app
heroku create your-app-name

# Set environment variables
heroku config:set SECRET_KEY=your-secret-key
heroku config:set FLASK_ENV=production

# Deploy
git push heroku main
```

### Option 2: Railway Deployment
```bash
# Connect to Railway
railway login

# Initialize project
railway init

# Deploy
railway up
```

### Option 3: VPS/Server Deployment
```bash
# Upload files to server
# Setup nginx/apache reverse proxy
# Configure SSL certificate
# Start application with production script
./start_production.sh
```

## 🔒 Security Best Practices

### 1. Environment Variables
```bash
# Never commit these to git:
SECRET_KEY=your-super-secret-key
DATABASE_URL=your-database-url
MAIL_PASSWORD=your-email-password
```

### 2. Server Configuration
```nginx
# Nginx example configuration
server {
    listen 80;
    server_name yourdomain.com;
    
    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### 3. SSL Certificate
```bash
# Using Let's Encrypt
certbot --nginx -d yourdomain.com
```

## 📊 Monitoring & Maintenance

### 1. Regular Backups
```bash
# Manual backup
python backup_system.py

# Schedule daily backups (crontab)
0 2 * * * /path/to/your/app/backup_system.py
```

### 2. Log Monitoring
```bash
# Check application logs
tail -f startsmart.log

# Check system logs
tail -f /var/log/nginx/error.log
```

### 3. Health Checks
```bash
# Check if app is running
curl -f http://yourapp.com/health || echo "App is down!"
```

## 🚨 Troubleshooting

### Common Issues:

1. **500 Internal Server Error**
   - Check logs: `tail -f startsmart.log`
   - Verify environment variables
   - Check database connectivity

2. **Database Connection Issues**
   - Verify database file permissions
   - Check backup integrity
   - Restore from backup if needed

3. **File Upload Issues**
   - Check uploads directory permissions
   - Verify file size limits
   - Check disk space

### Emergency Recovery:
```bash
# Restore from backup
python -c "from backup_system import restore_backup; restore_backup('backups/latest_backup.db')"

# Reset to clean state
python reset_for_production.py
```

## 📞 Support

If you encounter issues:
1. Check the logs first
2. Verify environment configuration
3. Test with clean database
4. Contact system administrator

---
**Last Updated:** July 31, 2025  
**Version:** Production Ready v1.0
