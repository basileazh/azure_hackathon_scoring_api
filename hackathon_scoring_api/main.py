import uvicorn
from fastapi import FastAPI
from hackathon_scoring_api.core.log import logger
from hackathon_scoring_api.routers import score

# Start the app
logger.info("Starting the app")
app = FastAPI(
    title="Scoring API",
    description="Scoring API for Eki.UK Hackathons. For any question, please contact basile.elazhari@ekimetrics.com",
    version="0.1",
)
logger.info("App started")

# Add routers
logger.info("Adding routers")
app.include_router(score.router)
logger.info("Routers added")


@app.get("/ping")
async def ping():
    return {"status": "alive"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True, lifespan="on")
