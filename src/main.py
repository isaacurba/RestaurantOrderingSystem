from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi import Request
from fastapi.middleware.cors import CORSMiddleware

from src.exceptions import AppException
from src.router.auth_router import router as auth_router
from src.router.admin_router import router as admin_router
from src.database import Base, engine


Base.metadata.create_all(bind=engine)
print("Database tables created successfully")

app = FastAPI(title="Restaurant Ordering System")

@app.exception_handler(AppException)
async def app_exception_handler(request: Request, exception: AppException):
    return JSONResponse(
        status_code=exception.status_code,
        content={"detail": str(exception)},
    )
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500", "http://localhost:5500"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(admin_router)