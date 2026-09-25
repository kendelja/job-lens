from scripts.runIngestion import main

from fastapi import APIRouter, Query

from app.database.repositories import get_jobs


router = APIRouter(
    prefix="/jobs",
    tags=["Jobs"]
)

@router.post("/ingest")
async def ingest_jobs():
    await main()

    return {
        "status": "complete"
    }


@router.get("/")
def jobs(
    limit: int = Query(
        default=200,
        ge=1,
        le=200
    )
):

    return get_jobs(limit)