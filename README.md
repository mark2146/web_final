# University Course Review Platform

A Django course project that combines course evaluations, a student account flow, a resume preview tool, and automated collection of public course/teacher listings from Yuan Ze University's course portal.

## Features

- Student registration and login using Django password hashing
- Course evaluation submission and listing
- Semester-based course and instructor discovery
- Selenium/Beautiful Soup scraper for public course listings
- Resume form and browser preview
- Server-rendered Django templates

## Requirements

- Python 3.10+
- MySQL 8 or a compatible database
- Google Chrome/Chromium for the course scraper
- A ChromeDriver version compatible with the installed browser, or Selenium Manager

## Setup

```bash
git clone https://github.com/mark2146/web_final.git
cd web_final
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
python -m pip install -r requirements.txt
cp .env.example .env
cd web
python manage.py migrate
python manage.py runserver
```

The historical project expects custom MySQL tables (`custom_users` and the course-evaluation table) that are accessed with parameterized SQL rather than Django models. Their schema must be created separately before those features work.

## Configuration

All production settings should come from environment variables. See `.env.example` for variable names; never commit real values.

| Variable | Purpose |
|---|---|
| `DJANGO_SECRET_KEY` | Signs sessions and security tokens |
| `DJANGO_DEBUG` | Development debug mode only |
| `DJANGO_ALLOWED_HOSTS` | Comma-separated host allowlist |
| `DB_NAME`, `DB_USER`, `DB_PASSWORD` | MySQL credentials |
| `DB_HOST`, `DB_PORT` | MySQL endpoint |
| `CHROMEDRIVER_PATH` | Optional explicit driver path |

## Main routes

- `/register/` and `/login/` — account flow
- course evaluation form/list pages
- course-data refresh and semester selection
- resume form and preview

## Security warning

The current historical version is **not safe to deploy publicly**. It contains credentials/configuration that have been committed to Git history, enables Django debug mode, lacks deployment hardening, and uses custom authentication tables. Rotate all exposed credentials, remove them from the current tree and history, migrate authentication to Django's built-in user system, and run `python manage.py check --deploy` before any deployment.

The checked-in ChromeDriver executable should be removed from source control. Use Selenium Manager or install a verified driver separately.

## Status

Archived course/portfolio project. Local development and study are supported; public deployment requires the remediation described above.
