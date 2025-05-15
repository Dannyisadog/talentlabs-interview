from datetime import datetime
from typing import List, Union
from uuid import UUID

from ninja import Field, Schema


class SalaryRange(Schema):
    min: int
    max: int
    currency: str


class JobBaseSchema(Schema):
    title: str
    company_name: str = Field(..., alias="companyName")
    location: str
    description: str
    salary_range: Union[SalaryRange, str] = Field(..., alias="salaryRange")
    posting_date: datetime = Field(..., alias="postingDate")
    expiration_date: datetime = Field(..., alias="expirationDate")
    required_skills: List[str] = Field(..., alias="requiredSkills")


class JobSchema(JobBaseSchema):
    id: UUID


class JobCreateSchema(JobBaseSchema):
    pass


class JobUpdateSchema(Schema):
    title: str = None
    company_name: str = None
    location: str = None
    description: str = None
    salary_range: Union[SalaryRange, str] = None
    posting_date: str = None
    expiration_date: str = None
    required_skills: List[str] = None


class ErrorResponse(Schema):
    error: str
