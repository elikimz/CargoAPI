from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import auth, cargo, tracking, notifications,users

app = FastAPI()

origins = [
    "http://localhost:5173",  # Local development
    "https://cargo-frontend-dusky.vercel.app"  # Deployed frontend
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,  # Allow cookies/auth headers
    allow_methods=["*"],  # Allow all request methods
    allow_headers=["*"],  # Allow all headers
)

# Include API routes
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(cargo.router, prefix="/cargo", tags=["Cargo"])
app.include_router(tracking.router, prefix="/tracking", tags=["Tracker"])
app.include_router(notifications.router, prefix="/notifications", tags=["Notifications"])

@app.get("/")
def read_root():
    return {"message": "Welcome to Cargo Management System"}
