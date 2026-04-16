import asyncio
from datetime import datetime
from ..core.database import db

analytics_queue = asyncio.Queue()

async def process_analytics_worker():
    """Background worker that continuously processes analytics events."""
    while True:
        try:
            event = await analytics_queue.get()
            if event is None:
                break
                
            short_code = event.get("short_code")
            
            # 1. Raw event insertion
            await db.db.raw_clicks.insert_one({
                "short_code": short_code,
                "timestamp": datetime.utcnow(),
                "ip": event.get("ip"),
                "user_agent": event.get("user_agent")
            })
            
            # 2. Aggregated updates
            today = datetime.utcnow().strftime("%Y-%m-%d")
            await db.db.analytics.update_one(
                {"short_code": short_code},
                {
                    "$inc": {
                        "total_clicks": 1,
                        f"clicks_per_day.{today}": 1
                    }
                },
                upsert=True
            )
            analytics_queue.task_done()
        except asyncio.CancelledError:
            break
        except Exception as e:
            print(f"Analytics Worker Error: {e}")
