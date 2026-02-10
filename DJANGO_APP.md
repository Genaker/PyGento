# Django App for PyGento

This document provides a comprehensive guide to the Django application integrated with PyGento.

## Overview

The Django app demonstrates how to use PyGento to access Magento database directly without using the Magento 2 core. It provides a web interface for querying and displaying Magento products.

## Architecture

```
django_app/              # Main Django project
├── settings.py         # Django settings with PyGento configuration
├── urls.py            # Main URL routing
└── wsgi.py            # WSGI application entry point

products/               # Django app for Magento products
├── views.py           # Views with PyGento integration
├── urls.py            # App-specific URL routing
├── apps.py            # App configuration
└── templates/         # HTML templates
    └── products/
        ├── base.html         # Base template with styling
        ├── home.html         # Home page with documentation
        └── product_list.html # Product listing page

manage.py              # Django management script
run_django.py          # Convenience script to run the server
test_django.py         # Test suite for the Django app
```

## Features

### 1. Home Page (`/`)
- Welcome message and documentation
- Quick start guide
- API endpoint documentation
- Feature overview

### 2. Product Listing (`/products/`)
- HTML view with styled table
- JSON API support (`?format=json`)
- Pagination control (`?limit=20`)
- Query performance metrics
- Error handling with user-friendly messages

### 3. Health Check (`/health/`)
- JSON endpoint for monitoring
- Returns service status and timestamp

## Running the Application

### Method 1: Using the convenience script
```bash
python run_django.py
```

### Method 2: Using Django management command
```bash
python manage.py runserver
```

### Method 3: Specify host and port
```bash
python manage.py runserver 0.0.0.0:8080
```

## Configuration

The Django app uses the same `.env` file as the FastAPI app:

```ini
# Database Configuration
DB_HOST=localhost
DB_PORT=3306
DB_NAME=magento
DB_USER=magento
DB_PASSWORD=magento
DB_CHARSET=utf8mb4

# Magento Edition (community/enterprise)
MAGENTO_EDITION=enterprise

# Django Secret Key (optional, for production)
DJANGO_SECRET_KEY=your-secret-key-here
```

## API Endpoints

### GET `/`
Home page with documentation.

**Response:** HTML page

### GET `/products/`
List Magento products.

**Query Parameters:**
- `limit` (integer, default: 10): Number of products to return (1-100)
- `format` (string, default: html): Response format (html or json)

**Example Requests:**
```bash
# HTML view with 20 products
curl http://127.0.0.1:8000/products/?limit=20

# JSON API with 5 products
curl http://127.0.0.1:8000/products/?format=json&limit=5
```

**JSON Response Example:**
```json
{
  "count": 5,
  "query_time": 45.23,
  "products": [
    {
      "id": 1,
      "sku": "PRODUCT-001",
      "created_at": "2024-01-01T00:00:00",
      "updated_at": "2024-01-15T12:30:00"
    },
    ...
  ]
}
```

### GET `/health/`
Health check endpoint for monitoring.

**Response:**
```json
{
  "status": "ok",
  "service": "PyGento Django App",
  "timestamp": "2024-01-15T12:30:45.123456"
}
```

## Testing

Run the test suite:

```bash
python test_django.py
```

The tests cover:
- Home view rendering
- Health check endpoint
- Product list view (HTML format)
- Product list view (JSON format)
- Input validation for query parameters
- Error handling when database is unavailable

## Security Features

1. **Secret Key Management**: Django SECRET_KEY can be set via environment variable
2. **Input Validation**: All user inputs are validated and sanitized
3. **Error Handling**: Graceful error messages without exposing sensitive information
4. **Database Connection**: Secure connection using environment variables
5. **CSRF Protection**: Django's built-in CSRF protection enabled

## Code Quality

- **Type Hints**: Views use proper type annotations
- **Error Handling**: Comprehensive try-except blocks for database operations
- **Resource Management**: Database sessions properly closed in finally blocks
- **Input Validation**: All query parameters validated with bounds checking
- **Code Review**: Passed automated code review checks
- **Security Scan**: Passed CodeQL security analysis (0 vulnerabilities)

## Performance

- Direct database access via PyGento (faster than Magento core)
- Query time metrics displayed for each request
- Efficient SQLAlchemy queries with proper limits
- Minimal overhead compared to standalone PyGento

## Development

### Adding New Views

1. Create view in `products/views.py`:
```python
from django.views import View
from models import init_db
from models.catalog import CatalogProductEntity as Product
from utils.database import DatabaseConnection

class MyView(View):
    def get(self, request):
        db_conn = DatabaseConnection()
        engine, Session = init_db(db_conn.get_connection_string())
        session = Session()
        try:
            # Your PyGento queries here
            products = session.query(Product).all()
            return render(request, 'my_template.html', {'products': products})
        finally:
            session.close()
```

2. Add URL pattern in `products/urls.py`:
```python
path('myview/', views.MyView.as_view(), name='myview'),
```

3. Create template in `products/templates/products/my_template.html`

### Adding Tests

Add test functions to `test_django.py`:
```python
def test_my_view():
    factory = RequestFactory()
    request = factory.get('/myview/')
    view = MyView.as_view()
    response = view(request)
    assert response.status_code == 200
    print("✓ My view test passed")
```

## Troubleshooting

### Database Connection Error
**Error:** `Database connection failed`
**Solution:** Check your `.env` file and ensure database credentials are correct.

### Module Not Found Error
**Error:** `ModuleNotFoundError: No module named 'django'`
**Solution:** Install requirements: `pip install -r requirements.txt`

### Port Already in Use
**Error:** `Error: That port is already in use.`
**Solution:** Use a different port: `python manage.py runserver 8001`

### Import Error
**Error:** `ImportError: cannot import name 'Product'`
**Solution:** Ensure MAGENTO_EDITION is set in `.env` file.

## Production Deployment

For production deployment:

1. Set `DEBUG = False` in settings.py
2. Configure ALLOWED_HOSTS in settings.py
3. Set DJANGO_SECRET_KEY environment variable
4. Use a production database
5. Set up static file serving
6. Use a production WSGI server (gunicorn, uWSGI)
7. Configure reverse proxy (Nginx, Apache)
8. Set up SSL/TLS certificates
9. Configure logging and monitoring

Example production command:
```bash
gunicorn django_app.wsgi:application --bind 0.0.0.0:8000 --workers 4
```

## Comparison: Django vs FastAPI

Both implementations are included in PyGento:

| Feature | Django App | FastAPI App |
|---------|-----------|-------------|
| File | `products/` app | `test_fastapi.py` |
| Templates | HTML templates | API only |
| Web UI | Yes | Swagger UI |
| API | Yes (JSON) | Yes (JSON) |
| Authentication | Built-in | Basic Auth |
| Admin | Available | Not available |
| Async | Sync | Async |
| Speed | Fast | Faster |

Choose Django for:
- Full web application with UI
- Admin interface needed
- Form handling
- Template rendering
- Traditional web app patterns

Choose FastAPI for:
- Pure API backend
- Maximum performance
- Async operations
- Modern async/await patterns
- API documentation (Swagger)

## License

MIT License - same as PyGento

## Support

For issues or questions:
- Create an issue on GitHub
- Email: yegorshytikov@gmail.com
