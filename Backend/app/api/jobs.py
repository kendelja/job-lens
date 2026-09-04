from fastapi import APIRouter, Query

from app.database.repositories import get_jobs


router = APIRouter(
    prefix="/jobs",
    tags=["Jobs"]
)


@router.get("/")
def jobs(
    limit: int = Query(
        default=50,
        ge=1,
        le=200
    )
):

    return get_jobs(limit)