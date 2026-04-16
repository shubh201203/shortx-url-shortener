import string
import random
from ..core.database import db

def generate_short_code(length=7):
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(length))

async def create_unique_short_code():
    while True:
        code = generate_short_code()
        # Ensure it doesn't already exist
        existing = await db.db.urls.find_one({"short_code": code})
        if not existing:
            return code

def predict_spam_status(url: str) -> str:
    from ..main import ml_model
    if not ml_model:
        return "safe" # fallback if model not loaded
    
    try:
        prediction = ml_model.predict([url])[0]
        return "suspicious" if prediction == 1 else "safe"
    except Exception as e:
        print(f"Prediction error: {e}")
        return "safe"
