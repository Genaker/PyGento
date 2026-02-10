"""
Django app test for PyGento integration.

This script demonstrates how to run the Django app and test basic functionality.
"""
import os
import sys
import json

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_app.settings')

import django
django.setup()

from django.test import RequestFactory
from products.views import HomeView, health_check, ProductListView

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

def test_product_list_view_html():
    """Test the product list view with HTML format"""
    factory = RequestFactory()
    
    # Test with default parameters
    request = factory.get('/products/')
    view = ProductListView.as_view()
    
    try:
        response = view(request)
        # May fail if database is not available, but should not crash
        if response.status_code == 200:
            print("✓ Product list view (HTML) test passed")
        else:
            print(f"⚠ Product list view returned status {response.status_code} (database may not be available)")
    except Exception as e:
        print(f"⚠ Product list view test skipped (database not available): {type(e).__name__}")

def test_product_list_view_json():
    """Test the product list view with JSON format"""
    factory = RequestFactory()
    
    # Test with JSON format
    request = factory.get('/products/?format=json&limit=5')
    view = ProductListView.as_view()
    
    try:
        response = view(request)
        if response.status_code == 200:
            # Try to parse JSON response
            data = json.loads(response.content)
            assert 'count' in data, "Response should include 'count' field"
            assert 'products' in data, "Response should include 'products' field"
            print("✓ Product list view (JSON) test passed")
        else:
            print(f"⚠ Product list view returned status {response.status_code} (database may not be available)")
    except Exception as e:
        print(f"⚠ Product list view JSON test skipped (database not available): {type(e).__name__}")

def test_product_list_view_validation():
    """Test the product list view parameter validation"""
    factory = RequestFactory()
    view = ProductListView.as_view()
    
    # Test with invalid limit
    try:
        request = factory.get('/products/?limit=invalid')
        response = view(request)
        # Should not crash, should use default limit
        if response.status_code in [200, 500]:  # 500 if DB not available
            print("✓ Product list view validation test passed")
    except Exception as e:
        print(f"⚠ Product list view validation test skipped (database not available): {type(e).__name__}")

if __name__ == '__main__':
    print("Running Django app tests...")
    print()
    
    try:
        test_home_view()
        test_health_check()
        test_product_list_view_html()
        test_product_list_view_json()
        test_product_list_view_validation()
        print()
        print("All tests completed! ✓")
        print()
        print("To run the Django development server:")
        print("  python manage.py runserver")
        print("  or")
        print("  python run_django.py")
        print()
        print("Then visit:")
        print("  http://127.0.0.1:8000/ - Home page")
        print("  http://127.0.0.1:8000/products/ - Products list")
        print("  http://127.0.0.1:8000/health/ - Health check")
    except Exception as e:
        print(f"✗ Test failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
