# Deploying To Render

## Local

1. Copy `.env.example` to `.env` and fill values.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run:
   ```bash
   python manage.py migrate
   python manage.py runserver
   ```

## Render

1. Push this folder to GitHub.
2. Create a new Render Web Service from the GitHub repo.
3. Use:
   - Build command: `bash build.sh`
   - Start command: `gunicorn portfolio_project.wsgi:application`
4. Add environment variables:
   - `DJANGO_DEBUG=False`
   - `DJANGO_SECRET_KEY`
   - `DATABASE_URL`
   - `CLOUDINARY_CLOUD_NAME`
   - `CLOUDINARY_API_KEY`
   - `CLOUDINARY_API_SECRET`
   - `SECURE_HSTS_SECONDS=31536000` for production HTTPS

Render sets `RENDER_EXTERNAL_HOSTNAME` automatically, and the app adds it to `ALLOWED_HOSTS` and CSRF trusted origins.

Do not push `.env` to GitHub.
