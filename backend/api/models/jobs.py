import json
import uuid

from django.db import models

from api.models.base import BaseModel


class Job(BaseModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200)
    description = models.TextField()
    location = models.CharField(max_length=200)
    salary_range = models.JSONField()
    company_name = models.CharField(max_length=200)
    posting_date = models.DateField()
    expiration_date = models.DateField()
    required_skills = models.JSONField()

    def __str__(self):
        return f"{self.title} at {self.company_name}"

    def to_dict(self):
        # Parse salary_range if it's a string
        salary_range = self.salary_range
        if isinstance(salary_range, str):
            try:
                salary_range = json.loads(salary_range)
            except Exception:
                pass  # If parsing fails, keep as string

        # If it's a dict, ensure all keys are present
        if isinstance(salary_range, dict):
            salary_range = {
                "min": salary_range.get("min"),
                "max": salary_range.get("max"),
                "currency": salary_range.get("currency", "USD")
            }

        return {
            'id': str(self.id),
            'title': self.title,
            'description': self.description,
            'location': self.location,
            'salaryRange': salary_range,
            'companyName': self.company_name,
            'postingDate': self.posting_date if isinstance(self.posting_date, str) else self.posting_date.isoformat(),
            'expirationDate': self.expiration_date if isinstance(self.expiration_date, str) else self.expiration_date.isoformat(),
            'requiredSkills': self.required_skills,
            'createdAt': self.created_at.isoformat(),
            'updatedAt': self.updated_at.isoformat(),
            'isActive': self.is_active,
            'isDeleted': self.is_deleted
        }

    class Meta:
        db_table = "jobs"
