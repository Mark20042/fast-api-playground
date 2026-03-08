from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from secure import Secure
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from beanie import init_beanie

# local imports
from config.database import db, ping_db
from models.users import User 
from routers.Auth import auth_router

# init 
limiter = Limiter(key_func=get_remote_address)
secure_headers = Secure()
secure_headers = Secure.with_default_headers()

# database connection
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting up server...")
    await ping_db()
   
    await init_beanie(database=db, document_models=[User])
    print("Database and Models connected successfully!")
    yield
    print("Shutting down server...")

# initialize app
app = FastAPI(lifespan=lifespan)

# secure http headers
@app.middleware("http")
async def set_secure_headers(request: Request, call_next):
    response = await call_next(request)
    secure_headers.set_headers_async(response)
    return response

# rate limiter middleware
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(SlowAPIMiddleware)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# routers
app.include_router(auth_router)

# routers
@app.get("/")
async def root():
    return {"message": "Crypto Vault API is running!"}