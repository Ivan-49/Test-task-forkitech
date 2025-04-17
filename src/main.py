from fastapi import FastAPI
from routers.all_routers import all_routers
from loguru import logger
from database import init_models


logger.add(
    "logs/app.log",
    format="{time} {level} {message}",
    level="DEBUG",
    rotation="00:00",
    compression="zip",
    enqueue=True,
)

app = FastAPI(debug=True)


@app.on_event("startup")
async def startup_event():
    try:
        await init_models()
        logger.info("Database tables created")
    except Exception as e:
        logger.error(f"database error: {e}")
        raise e


for i in all_routers:
    app.include_router(i)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
