
# StartSmart Deployment Guide for Render

## Environment Variables to Set in Render:
1. SECRET_KEY=your-random-secret-key-here
2. FLASK_ENV=production

## Build Command:
pip install -r requirements.txt

## Start Command:
gunicorn app:app

## Important Notes:
- Database will be reset on each deployment (consider using PostgreSQL for persistence)
- Upload files won't persist (consider using cloud storage)
- Sessions are configured for HTTP (change to HTTPS when using custom domain)

## Debugging Routes (remove in production):
- /test-auth - Test authentication system
- /debug-session - Debug session data

## Post-Deployment Testing:
1. Visit /test-auth to verify database connectivity
2. Try registering a new user
3. Test login functionality
4. Check dashboard access

## Common Issues:
- If login fails, check Render logs for database errors
- If sessions don't work, verify SECRET_KEY is set
- If styles don't load, check static file serving

