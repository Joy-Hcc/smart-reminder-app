from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.api import auth, categories, reminders, history
from app.tasks.scheduler import start_scheduler, shutdown_scheduler

Base.metadata.create_all(bind=engine)

app = FastAPI(title="SmartReminder API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(categories.router)
app.include_router(reminders.router)
app.include_router(history.router)


@app.on_event("startup")
def startup():
    start_scheduler()


@app.on_event("shutdown")
def shutdown():
    shutdown_scheduler()
