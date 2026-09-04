from app.database.connection import get_connection


def job_exists(
    source: str,
    source_job_id: str | None,
    url: str
) -> bool:

    connection = get_connection()

    try:
        with connection.cursor() as cursor:

            if source_job_id:
                cursor.execute(
                    """
                    SELECT 1
                    FROM jobs
                    WHERE source = %s
                    AND source_job_id = %s
                    LIMIT 1
                    """,
                    (source, source_job_id)
                )

            else:
                cursor.execute(
                    """
                    SELECT 1
                    FROM jobs
                    WHERE url = %s
                    LIMIT 1
                    """,
                    (url,)
                )

            return cursor.fetchone() is not None

    finally:
        connection.close()