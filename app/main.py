from fastapi import FastAPI

from app.database import Base, engine

from app.routers.auth import router as auth_router
from app.routers.warehouse import router as warehouse_router
from app.routers.product import router as product_router
from app.routers.transfer import router as transfer_router
from app.routers.reports import router as reports_router


Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Warehouse Inventory Transfer Management System",
    description="Warehouse Inventory Transfer Management System using FastAPI",
    version="1.0.0"
)


app.include_router(auth_router)
app.include_router(warehouse_router)
app.include_router(product_router)
app.include_router(transfer_router)
app.include_router(reports_router)


@app.get("/", tags=["Root"])
def root():
    return {
        "message": "Welcome to Warehouse Inventory Transfer Management System API"
    }


@app.get("/health", tags=["Health"])
def health_check():
    return {
        "status": "Running"
    }