from fastapi import FastAPI

from app.routers import auth, cargo, tracking, notifications

app = FastAPI()

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://cargo-frontend-dusky.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(cargo.router, prefix="/cargo", tags=["Cargo"])
app.include_router(tracking.router, prefix="/tracking", tags=["Tracker"])
app.include_router(notifications.router, prefix="/notifications", tags=["Notifications"])

@app.get("/")
def read_root():
    return {"message": "Welcome to Cargo Management System"}
