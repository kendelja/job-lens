from app.models.job import Job


def validate_job(job: Job) -> tuple[bool, list[str]]:

    errors = []

    if not job.title:
        errors.append("Missing title")

    if not job.company:
        errors.append("Missing company")

    if not job.url:
        errors.append("Missing URL")

    if not job.source:
        errors.append("Missing source")

    return len(errors) == 0, errors