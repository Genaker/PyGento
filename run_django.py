#!/usr/bin/env python
"""
Simple script to run the Django development server.
This is a convenience wrapper around manage.py runserver.
"""
import os
import sys

if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_app.settings')
    
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    
    # Only show the banner if this is not a reload (RUN_MAIN is set on reload)
    if os.environ.get('RUN_MAIN') != 'true':
        print("=" * 60)
        print("🐍 Starting PyGento Django Server")
        print("=" * 60)
        print()
        print("Visit http://127.0.0.1:8000/ to see the application")
        print()
        print("Available endpoints:")
        print("  / - Home page")
        print("  /products/ - Product listing")
        print("  /health/ - Health check")
        print()
        print("Press Ctrl+C to stop the server")
        print("=" * 60)
        print()
    
    execute_from_command_line(['manage.py', 'runserver'])

