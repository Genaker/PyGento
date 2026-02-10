from django.shortcuts import render
from django.http import JsonResponse
from django.views import View
import time
from datetime import datetime

from models import init_db
from models.catalog import CatalogProductEntity as Product
from utils.database import DatabaseConnection


class ProductListView(View):
    """View to list Magento products using PyGento"""
    
    def get(self, request):
        # Get query parameters
        limit = int(request.GET.get('limit', 10))
        format_type = request.GET.get('format', 'html')  # html or json
        
        # Initialize PyGento database connection
        db_conn = DatabaseConnection()
        engine, Session = init_db(db_conn.get_connection_string())
        session = Session()
        
        try:
            start_time = time.time()
            
            # Query products using PyGento
            products = session.query(Product).limit(limit).all()
            
            query_time = time.time() - start_time
            
            # Prepare product data
            product_list = []
            for product in products:
                product_list.append({
                    'id': product.entity_id,
                    'sku': product.sku,
                    'created_at': product.created_at.isoformat() if product.created_at else None,
                    'updated_at': product.updated_at.isoformat() if product.updated_at else None,
                })
            
            # Return JSON if requested
            if format_type == 'json':
                return JsonResponse({
                    'count': len(product_list),
                    'query_time': round(query_time * 1000, 2),  # ms
                    'products': product_list
                })
            
            # Otherwise return HTML
            context = {
                'products': product_list,
                'count': len(product_list),
                'query_time': round(query_time * 1000, 2),
                'limit': limit,
            }
            return render(request, 'products/product_list.html', context)
            
        finally:
            session.close()


class HomeView(View):
    """Home page view"""
    
    def get(self, request):
        context = {
            'title': 'PyGento Django App',
            'description': 'Django application using PyGento to query Magento database',
            'timestamp': datetime.now().isoformat()
        }
        return render(request, 'products/home.html', context)


def health_check(request):
    """Health check endpoint"""
    return JsonResponse({
        'status': 'ok',
        'service': 'PyGento Django App',
        'timestamp': datetime.now().isoformat()
    })

