# Shibangi Khan Portfolio

A Django portfolio website for Shibangi Khan, built to showcase graphic design, visual art, categories, product work, education, experience, and recent highlights.

## Features

- Admin-managed portfolio hierarchy: categories, sub categories, product categories, and products
- Admin-managed education and experience sections
- Recent highlights with tags, short list previews, detail pages, images, documents, links, and dynamic likes
- Image viewer with zoom support
- Best-effort image protection against right-click save, dragging, printing, and common capture shortcuts
- Local development support with SQLite or external database
- Render-ready deployment with Gunicorn, WhiteNoise, and Cloudinary media support

## Tech Stack

- Python 3.11
- Django 5.2
- PostgreSQL or SQLite
- Cloudinary for uploaded media in production
- WhiteNoise for static files
- Render for hosting

## Local Setup

1. Create and activate a virtual environment.

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Copy environment variables:
   ```bash
   copy .env.example .env
   ```

4. Fill `.env` with local values.

5. Run migrations:
   ```bash
   python manage.py migrate
   ```

6. Create an admin user:
   ```bash
   python manage.py createsuperuser
   ```

7. Start the development server:
   ```bash
   python manage.py runserver
   ```

Open `http://127.0.0.1:8000/`.

## Admin Content

Use `/admin/` to manage:

- Categories
- Sub categories
- Product categories
- Product items
- Education
- Experience
- Highlight posts

Highlight posts support optional image, document, and external link fields. The highlights list page stays short, while the detail page shows full content.

Portfolio work follows this structure:

`Category -> Sub Category -> Product Category -> Product Item`

## Deployment

This project is ready for Render.

See [DEPLOYMENT.md](DEPLOYMENT.md) for the full deployment checklist.

Do not commit `.env` or real secrets to GitHub. Use Render environment variables for production credentials.

## Notes

Screenshot blocking is not fully possible in a normal browser because screenshots are controlled by the operating system. The project includes best-effort protections, but watermarking and controlled access are the safest practical options for public web content.
