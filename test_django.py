"""
Django app test for PyGento integration.

This script demonstrates how to run the Django app and test basic functionality.
"""
import os
import sys

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_app.settings')

import django
django.setup()

from django.test import RequestFactory
from products.views import HomeView, health_check

def test_home_view():
    """Test the home view"""
    factory = RequestFactory()
    request = factory.get('/')
    view = HomeView.as_view()
    response = view(request)
    
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    print("✓ Home view test passed")

def test_health_check():
    """Test the health check endpoint"""
    factory = RequestFactory()
    request = factory.get('/health/')
    response = health_check(request)
    
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    print("✓ Health check test passed")

if __name__ == '__main__':
    print("Running Django app tests...")
    print()
    
    try:
        test_home_view()
        test_health_check()
        print()
        print("All tests passed! ✓")
        print()
        print("To run the Django development server:")
        print("  python manage.py runserver")
        print()
        print("Then visit:")
        print("  http://127.0.0.1:8000/ - Home page")
        print("  http://127.0.0.1:8000/products/ - Products list")
        print("  http://127.0.0.1:8000/health/ - Health check")
    except Exception as e:
        print(f"✗ Test failed: {e}")
        sys.exit(1)
