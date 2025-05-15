from typing import Any, Dict, List, Optional
from uuid import UUID

from api.exceptions import JobNotFoundError
from api.repository.jobs import JobRepository


def create_job(job_data: dict) -> dict:
    job = JobRepository.create(**job_data)
    return job.to_dict()

def get_job(job_id: UUID) -> dict:
    job = JobRepository.get_by_id({"id": job_id})
    return job.to_dict()

def update_job(job_id: UUID, job_data: dict) -> dict:
    job = JobRepository.update({"id": job_id}, **job_data)
    return job.to_dict()

def delete_job(job_id: UUID) -> None:
    JobRepository.delete(job_id)

def list_jobs(
    filters: Optional[dict] = None,
    page: int = 1,
    page_size: int = 10,
    search: Optional[str] = None,
    status: Optional[str] = None,
    order_by: Optional[str] = None,
) -> Dict[str, Any]:
    """
    List jobs with pagination, search, filtering, and sorting.
    
    Args:
        filters: Base filter conditions for other fields
        page: Page number (1-based)
        page_size: Number of items per page
        search: Search term for title, description, or company name
        status: Filter by job status ('active', 'expired', 'scheduled')
        order_by: Field to order by ('posting_date' or 'expiration_date')
        
    Returns:
        Dict containing paginated results and metadata
    """
    # Extract search from filters if present
    if filters and 'search' in filters:
        search = filters.pop('search')
    
    result = JobRepository.list(
        condition=filters or {},
        page=page,
        page_size=page_size,
        search=search,
        status=status,
        order_by=order_by
    )
    
    # Convert Job objects to dictionaries
    result['results'] = [job.to_dict() for job in result['results']]
    return result