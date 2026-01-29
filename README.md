# QR Landing Pages

Django app for creating and managing QR-code-accessible landing pages.

## Development

### Setup

1. Set environment variables
   - Make a copy of `.env.example` named `.env`
   - Follow instructions in [Configuration](#configuration) to obtain values
2. Build and start containers:
   ```bash
   docker compose up -d
   ```
3. Complete [First Time Setup](#first-time-setup)

The app will then be accessible at http://localhost:8000

### Services

- **web** (Django) - http://localhost:8000
- **postgres** - PostgreSQL database

## Configuration

Environment variables are used for configuration.

### Google OAuth (for Sign In with Google)

1. Go to https://console.cloud.google.com/apis/credentials
2. Create OAuth 2.0 Client ID (or use existing credentials)
   - Application type: Web application
   - Add authorized redirect URIs:
     - `http://localhost:8000/accounts/google/login/callback/` (development)
     - `https://yourdomain.com/accounts/google/login/callback/` (production)
3. Set env vars with values from dashboard:
   - `GOOGLE_OAUTH_CLIENT_ID`
   - `GOOGLE_OAUTH_SECRET`

## First Time Setup

Some actions must be completed once to finish setting up the site:

1. Run migrations:
   ```bash
   docker compose exec web python manage.py migrate
   ```
2. Create an initial admin user:
   ```bash
   docker compose exec web python manage.py createsuperuser
   ```
3. Update the site domain (required for OAuth redirects):
   ```bash
   docker compose exec web python manage.py update_site_domain
   ```
