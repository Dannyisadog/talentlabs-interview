from datetime import datetime
from typing import List, Optional
from uuid import UUID

from ninja import Query, Router

from api.exceptions import JobException, JobNotFoundError
from api.presentation.jobs import (ErrorResponse, JobCreateSchema, JobSchema,
                                   JobUpdateSchema)
from api.routes.auth import GlobalAuth
from api.service.jobs import (create_job, delete_job, get_job, list_jobs,
                              update_job)

router = Router(
    tags=["Jobs"],
    auth=GlobalAuth()
)

@router.post("/", response={201: JobSchema, 400: ErrorResponse})
def create_job_endpoint(request, payload: JobCreateSchema):
    try:
        job = create_job(payload.dict())
        return 201, job
    except JobException as e:
        return 400, {"error": str(e)}


@router.get("/{job_id}", response={200: JobSchema, 404: ErrorResponse})
def get_job_endpoint(request, job_id: UUID):
    try:
        job = get_job(job_id)
        return job
    except JobException as e:
        return 404, {"error": str(e)}
    

@router.get("/", response={200: dict, 400: ErrorResponse})
def list_jobs_endpoint(
    request,
    page: int = Query(1, description="Page number"),
    limit: int = Query(10, description="Number of items per page"),
    search: Optional[str] = Query(None, description="Search term for title, description, or company name"),
    location: Optional[str] = Query(None, description="Filter by location"),
    skills: Optional[List[str]] = Query(None, description="Filter by required skills"),
    salaryMin: Optional[int] = Query(None, description="Minimum salary"),
    salaryMax: Optional[int] = Query(None, description="Maximum salary"),
    orderBy: Optional[str] = Query(None, description="Sort by: postingDate or expirationDate"),
    orderDirection: Optional[str] = Query("desc", description="Sort direction: asc or desc")
):
    try:
        filters = {}
        
        if search:
            filters["search"] = search
        if location:
            filters["location__icontains"] = location
        if skills:
            filters["required_skills__overlap"] = skills
        if salaryMin is not None or salaryMax is not None:
            salary_filter = {}
            if salaryMin is not None:
                salary_filter["salary_range__min__gte"] = salaryMin
            if salaryMax is not None:
                salary_filter["salary_range__max__lte"] = salaryMax
            filters.update(salary_filter)
            
        # Sorting
        order_by = None
        if orderBy:
            if orderBy == "postingDate":
                order_by = f"{'-' if orderDirection == 'desc' else ''}posting_date"
            elif orderBy == "expirationDate":
                order_by = f"{'-' if orderDirection == 'desc' else ''}expiration_date"
            
        jobs = list_jobs(
            filters=filters,
            page=page,
            page_size=limit,
            order_by=order_by
        )
        return jobs
    except JobException as e:
        return 400, {"error": str(e)}


@router.put("/{job_id}", response={200: JobSchema, 404: ErrorResponse, 400: ErrorResponse})
def update_job_endpoint(request, job_id: UUID, payload: JobUpdateSchema):
    try:
        update_data = {k: v for k, v in payload.dict().items() if v is not None}
        job = update_job(job_id, update_data)
        return job
    except JobException as e:
        if isinstance(e, JobNotFoundError):
            return 404, {"error": str(e)}
        return 400, {"error": str(e)}


@router.delete("/{job_id}", response={200: dict, 404: ErrorResponse})
def delete_job_endpoint(request, job_id: UUID):
    try:
        delete_job(job_id)
        return {"message": "Job deleted successfully"}
    except JobException as e:
        return 404, {"error": str(e)}


