# Deployment Configuration for HTTPS

## Overview
This document outlines the steps to configure HTTPS for the Django application in a production environment.

## Prerequisites
- Domain name configured and pointing to your server
- SSL/TLS certificate (can be obtained from Let's Encrypt, Cloudflare, or commercial CA)
- Web server (Nginx or Apache) installed

## Option 1: Nginx Configuration

### Step 1: Install Certbot for Let's Encrypt SSL
```bash