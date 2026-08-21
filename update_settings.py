#!/usr/bin/env python3
"""
Script to update Django settings for GoDaddy VPS deployment
"""

import os
import sys

# Update settings.py for production
settings_updates = """
# Add at the end of settings.py
import os
from decouple import config

# Production settings
if not DEBUG:
    ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='dasandpartners.com,www.dasandpartners.com').split(',')
    
    # Database
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': config('DB_NAME'),
            'USER': config('DB_USER'),
            'PASSWORD': config('DB_PASSWORD'),
            'HOST': config('DB_HOST', default='localhost'),
            'PORT': config('DB_PORT', default='5432'),
        }
    }
    
    # Security
    SECURE_SSL_REDIRECT = True
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    X_FRAME_OPTIONS = 'DENY'
"""

print("✅ Settings update template created!")
print("This will be applied during deployment.")


