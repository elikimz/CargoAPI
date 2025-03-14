from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import auth, cargo, tracking, notifications

app = FastAPI()

# Enable CORS with proper settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://cargo-frontend-dusky.vercel.app"],  # Frontend URL
    allow_credentials=True,  # Allow cookies, tokens, etc.
    allow_methods=["*"],  # Allow all methods (GET, POST, PUT, DELETE)
    allow_headers=["*"],  # Allow all headers
    expose_headers=["*"],  # Expose headers to the client
)

app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(cargo.router, prefix="/cargo", tags=["Cargo"])
app.include_router(tracking.router, prefix="/tracking", tags=["Tracker"])
app.include_router(notifications.router, prefix="/notifications", tags=["Notifications"])

@app.get("/")
def read_root():
    return {"message": "Welcome to Cargo Management System"}
