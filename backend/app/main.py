import os
import asyncio
import joblib
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from .core.logging import LoggingMiddleware

from .core.database import connect_to_mongo, close_mongo_connection
from .core.redis import redis_client
from .worker.analytics import process_analytics_worker, analytics_queue
from .core.config import settings
from .api import routes

# Global state for ML model
ml_model = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup Events
    print("Starting up...")
    await connect_to_mongo()
    
    # Load ML Model
    global ml_model
    model_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "ml_model", "spam_model.pkl")
    try:
        if os.path.exists(model_path):
            ml_model = joblib.load(model_path)
            print("ML Spam Model loaded successfully.")
        else:
            print("Warning: ML model not found. Run train.py first.")
    except Exception as e:
        print(f"Error loading ML model: {e}")
        
    # Start background analytics worker
    asyncio.create_task(process_analytics_worker())
    
    yield
    
    # Shutdown Events
    print("Shutting down...")
    await close_mongo_connection()
    await redis_client.close()
    
    # Signal worker to stop
    await analytics_queue.put(None)

app = FastAPI(title=settings.PROJECT_NAME, lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(LoggingMiddleware)

# Include APIs
app.include_router(routes.router)

@app.get("/health")
async def health_check():
    return {"status": "ok"}
