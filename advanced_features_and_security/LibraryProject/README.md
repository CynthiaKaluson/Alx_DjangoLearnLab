# Introduction to Django Project
## Permissions and Groups

Custom permissions were added to the Book model:
- can_view
- can_create
- can_edit
- can_delete

Groups created via Django Admin:
- Viewers: can_view
- Editors: can_view, can_create, can_edit
- Admins: can_view, can_create, can_edit, can_delete

Views are protected using Django's @permission_required decorator.

## HTTPS and Secure Redirects Configuration

### Django HTTPS Settings
The application enforces HTTPS using Django security settings:
- SECURE_SSL_REDIRECT redirects all HTTP requests to HTTPS.
- HSTS is enabled for one year to force browsers to use HTTPS.
- Subdomains are included and HSTS preload is enabled.

### Secure Cookies
- SESSION_COOKIE_SECURE ensures session cookies are sent only over HTTPS.
- CSRF_COOKIE_SECURE ensures CSRF cookies are sent only over HTTPS.

### Secure Headers
- X_FRAME_OPTIONS is set to DENY to prevent clickjacking.
- SECURE_CONTENT_TYPE_NOSNIFF prevents MIME type sniffing.
- SECURE_BROWSER_XSS_FILTER enables browser XSS protection.

### Deployment (HTTPS Setup)
In production, HTTPS should be configured using a web server such as Nginx or Apache.
An SSL/TLS certificate (e.g., from Let's Encrypt) should be installed and configured
to serve traffic securely over HTTPS.

## Security Review

The application follows Django security best practices by enforcing HTTPS,
using secure cookies, and adding protective HTTP headers. These measures
protect user data in transit and reduce the risk of common attacks such
as XSS, clickjacking, and session hijacking.

Potential improvements include:
- Setting DEBUG=False in production
- Using a reverse proxy with automatic certificate renewal
- Adding Content Security Policy (CSP) headers
