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
        return {
            'id': str(self.id),
            'title': self.title,
            'description': self.description,
            'location': self.location,
            'salaryRange': self.salary_range,
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
