from datetime import datetime
from typing import Any, Dict, List, Optional
from uuid import UUID

from django.core.exceptions import ValidationError
from django.db.models import Q, QuerySet
from django.utils import timezone

from api.exceptions import (JobCreationError, JobDeletionError,
                            JobNotFoundError, JobUpdateError,
                            JobValidationError)
from api.models.jobs import Job


class JobRepository:
    @staticmethod
    def create(
        title: str,
        description: str,
        location: str,
        salary_range: dict,
        company_name: str,
        posting_date: datetime,
        expiration_date: datetime,
        required_skills: List[str],
    ) -> Job:
        try:
            # Convert datetime to date if needed
            posting_date = posting_date.date() if isinstance(posting_date, datetime) else posting_date
            expiration_date = expiration_date.date() if isinstance(expiration_date, datetime) else expiration_date
            
            return Job.objects.create(
                title=title,
                description=description,
                location=location,
                salary_range=salary_range,
                company_name=company_name,
                posting_date=posting_date,
                expiration_date=expiration_date,
                required_skills=required_skills,
            )
        except ValidationError as e:
            raise JobValidationError(str(e))
        except Exception as e:
            raise JobCreationError(f"Failed to create job: {str(e)}")

    @staticmethod
    def get_by_id(condition: dict) -> Job:
        try:
            # Add is_deleted=False to the condition if not explicitly specified
            if 'is_deleted' not in condition:
                condition['is_deleted'] = False
            return Job.objects.get(**condition)
        except Job.DoesNotExist:
            raise JobNotFoundError(condition)
    
    @staticmethod
    def list(
        condition: dict,
        page: int = 1,
        page_size: int = 10,
        search: Optional[str] = None,
        status: Optional[str] = None,
        order_by: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        List jobs with pagination, search, filtering, and ordering.
        
        Args:
            condition: Base filter conditions
            page: Page number (1-based)
            page_size: Number of items per page
            search: Search term for title, description, or company name
            status: Filter by job status ('active', 'expired', 'scheduled')
            order_by: Field to order by ('posting_date' or 'expiration_date')
            
        Returns:
            Dict containing paginated results and metadata
        """
        if 'is_deleted' not in condition:
            condition['is_deleted'] = False

        # Build the base queryset
        queryset = Job.objects.filter(**condition)

        # Apply search if provided
        if search:
            search_query = Q(title__icontains=search) | \
                          Q(description__icontains=search) | \
                          Q(company_name__icontains=search)
            queryset = queryset.filter(search_query)

        # Apply status filter
        today = timezone.now().date()
        if status:
            if status.lower() == 'active':
                queryset = queryset.filter(
                    posting_date__lte=today,
                    expiration_date__gte=today
                )
            elif status.lower() == 'expired':
                queryset = queryset.filter(expiration_date__lt=today)
            elif status.lower() == 'scheduled':
                queryset = queryset.filter(posting_date__gt=today)

        # Apply ordering
        if order_by:
            queryset = queryset.order_by(order_by)
        else:
            queryset = queryset.order_by('-posting_date')  # Default ordering

        # Calculate pagination
        total_count = queryset.count()
        start_index = (page - 1) * page_size
        end_index = start_index + page_size
        
        # Get paginated results
        jobs = queryset[start_index:end_index]

        return {
            'results': jobs,
            'total_count': total_count,
            'page': page,
            'page_size': page_size,
            'total_pages': (total_count + page_size - 1) // page_size
        }
    
    @staticmethod
    def update(condition: dict, **kwargs) -> Job:
        if 'company_name' in kwargs:
            raise JobValidationError("Cannot modify company name of a job")
        try:
            job = JobRepository.get_by_id(condition)
            for key, value in kwargs.items():
                setattr(job, key, value)
            job.save()
            return job
        except ValidationError as e:
            raise JobValidationError(str(e))
        except JobNotFoundError:
            raise
        except Exception as e:
            raise JobUpdateError(condition, str(e))

    @staticmethod
    def delete(id: UUID) -> None:
        try:
            job = JobRepository.get_by_id({"id": id, "is_deleted": False})
            job.is_deleted = True
            job.save()
        except JobNotFoundError:
            raise
        except Exception as e:
            raise JobDeletionError(id, str(e))
