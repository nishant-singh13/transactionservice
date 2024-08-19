from fastapi import FastAPI, HTTPException

from app.database.db import engine, Base
from app.route.transection import router

app = FastAPI()
Base.metadata.create_all(bind=engine)

"""
Here we bind transaction with main app module  
"""
app.include_router(router)


@app.get("/")
async def health_check():
    """
    Health check endpoint to verify the service status.
    """
    try:
        return {"status": "healthy"}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Service is not healthy")

