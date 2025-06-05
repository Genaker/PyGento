from typing import Optional, Dict, Any
from fastapi import FastAPI, Query, Depends, Request, HTTPException, status, Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.responses import JSONResponse, HTMLResponse
from typing import Annotated
import secrets
import time
from datetime import datetime
from sqlalchemy.orm import Session
import logging

from models import init_db
from models.catalog import CatalogProductEntity as Product
from utils.database import DatabaseConnection

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)-8s | %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

app = FastAPI()
security = HTTPBasic()

# In a real application, use environment variables or a secure secret management system
SECRET_USERNAME = "admin"
SECRET_PASSWORD = "password"

def get_current_username(credentials: Annotated[HTTPBasicCredentials, Depends(security)]):
    current_username_bytes = credentials.username.encode("utf8")
    correct_username_bytes = SECRET_USERNAME.encode("utf8")
    is_correct_username = secrets.compare_digest(
        current_username_bytes, correct_username_bytes
    )
    current_password_bytes = credentials.password.encode("utf8")
    correct_password_bytes = SECRET_PASSWORD.encode("utf8")
    is_correct_password = secrets.compare_digest(
        current_password_bytes, correct_password_bytes
    )
    if not (is_correct_username and is_correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username

# ASCII Art
ASCII_ART = r'''
██████╗ ██╗   ██╗ ██████╗ ███████╗███╗   ██╗████████╗ ██████╗ 
██╔══██╗╚██╗ ██╔╝██╔════╝ ██╔════╝████╗  ██║╚══██╔══╝██╔═══██╗
██████╔╝ ╚████╔╝ ██║  ███╗█████╗  ██╔██╗ ██║   ██║   ██║   ██║
██╔═══╝   ╚██╔╝  ██║   ██║██╔══╝  ██║╚██╗██║   ██║   ██║   ██║
██║        ██║   ╚██████╔╝███████╗██║ ╚████║   ██║   ╚██████╔╝
╚═╝        ╚═╝    ╚═════╝ ╚══════╝╚═╝  ╚═══╝   ╚═╝    ╚═════╝
'''

# Middleware for request timing
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.perf_counter()
    response = await call_next(request)
    process_time = (time.perf_counter() - start_time) * 1000
    response.headers["X-Process-Time"] = f"{process_time:.2f}ms"
    
    logger.info(
        f"🌐 {request.method} {request.url.path} | "
        f"Status: {response.status_code} | "
        f"Time: {process_time:6.1f}ms"
    )
    return response

@app.on_event("startup")
async def startup_event():
    """Print ASCII art banner on startup."""
    print(ASCII_ART)
    print("🚀 PyGENTO FastAPI Server starting...")

# Database setup
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Create engine and session factory
db_connection = DatabaseConnection()
engine = create_engine(db_connection.get_connection_string())
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Database dependency
def get_db():
    """Dependency that provides a database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/products")
def list_products(
    limit: int = Query(5, ge=1, le=100),
    with_attributes: bool = Query(False),
    store_id: Optional[int] = Query(None),
    db: Session = Depends(get_db)
):
    total_start = time.perf_counter()
    query = db.query(Product)
    attribute_code_map = {}
    attr_load_time = 0
    
    if with_attributes:
        try:
            from models.eav import EavAttribute
            attr_load_start = time.perf_counter()
            attribute_code_map = {a.attribute_id: a.attribute_code for a in db.query(EavAttribute).all()}
            attr_load_time = (time.perf_counter() - attr_load_start) * 1000  # Convert to ms
        except Exception as e:
            logger.error(f"Error loading attribute codes: {str(e)}")
            return JSONResponse(
                status_code=500,
                content={"error": "Failed to load attribute codes", "details": str(e)}
            )

    query_start = time.perf_counter()
    products = query.limit(limit).all()
    query_exec_time = (time.perf_counter() - query_start) * 1000  # Convert to ms

    product_list = []
    for product in products:
        prod_data = {
            "id": product.entity_id,
            "sku": product.sku,
            "created_at": product.created_at.isoformat() if product.created_at else None,
            "updated_at": product.updated_at.isoformat() if product.updated_at else None,
        }

        if with_attributes:
            prod_start = time.perf_counter()
            # Add attribute loading logic here
            attr_load_time = (time.perf_counter() - prod_start) * 1000  # Convert to ms
            logger.debug(
                f"📦 Product {product.sku} | "
                f"Attributes: {len(prod_data.get('attributes', {}))} | "
                f"Time: {attr_load_time:5.1f}ms"
            )

        product_list.append(prod_data)

    total_time = (time.perf_counter() - total_start) * 1000  # Convert to ms
    
    logger.info(
        f"📊 Products: {len(product_list):3d} | "
        f"Load: {attr_load_time:5.1f}ms | "
        f"Query: {query_exec_time:5.1f}ms | "
        f"Total: {total_time:6.1f}ms"
    )
    
    return {
        "timing": {
            "attribute_load_ms": round(attr_load_time, 2),
            "query_exec_ms": round(query_exec_time, 2),
            "total_ms": round(total_time, 2)
        },
        "count": len(product_list),
        "products": product_list
    }

@app.get("/hello")
async def hello_world():
    """Simple hello world endpoint that returns JSON."""
    return {
        "message": "Hello, World!",
        "service": "PyGENTO API",
        "status": "running",
        "timestamp": datetime.now().isoformat()
    }

@app.get("/secret")
async def secret_endpoint(username: Annotated[str, Depends(get_current_username)]):
    """Protected endpoint that requires authentication."""
    return {
        "message": "This is a secret path!",
        "username": username,
        "timestamp": datetime.now().isoformat()
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("test_fastapi:app", host="0.0.0.0", port=8000, reload=True)