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
    title: Optional[str] = None,
    description: Optional[str] = None,
    company_name: Optional[str] = None,
    location: Optional[str] = None,
    status: Optional[str] = Query(None, description="Filter by status: active, expired, scheduled"),
    sort_by: Optional[str] = Query(None, description="Sort by: posting_date or expiration_date"),
    sort_order: Optional[str] = Query("desc", description="Sort order: asc or desc"),
    page: int = Query(1, description="Page number"),
    page_size: int = Query(10, description="Number of items per page")
):
    try:
        filters = {}
        
        if title:
            filters["title__icontains"] = title
        if description:
            filters["description__icontains"] = description
        if company_name:
            filters["company_name__icontains"] = company_name
        if location:
            filters["location__icontains"] = location
            
        # Status filter
        if status:
            current_date = datetime.now().date()
            if status.lower() == "active":
                filters["expiration_date__gt"] = current_date
            elif status.lower() == "expired":
                filters["expiration_date__lte"] = current_date
            elif status.lower() == "scheduled":
                filters["posting_date__gt"] = current_date
                
        # Sorting
        order_by = None
        if sort_by:
            if sort_by == "posting_date":
                order_by = f"{'-' if sort_order == 'desc' else ''}posting_date"
            elif sort_by == "expiration_date":
                order_by = f"{'-' if sort_order == 'desc' else ''}expiration_date"
            
        jobs = list_jobs(
            filters=filters,
            page=page,
            page_size=page_size,
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


