import json
import os
from datetime import datetime

import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'api.settings')
django.setup()

from api.models.jobs import Job


def insert_fake_jobs():
    # Read the fake jobs JSON file
    with open('fake_jobs.json', 'r') as f:
        data = json.load(f)
    
    # Get all jobs from the JSON file
    jobs = data['jobs']
    
    # Counter for successful insertions
    inserted_count = 0
    
    # Insert each job into the database
    for job_data in jobs:
        try:
            # Convert string dates to datetime objects
            posting_date = datetime.strptime(job_data['postingDate'], '%Y-%m-%d').date()
            expiration_date = datetime.strptime(job_data['expirationDate'], '%Y-%m-%d').date()
            
            # Create a new Job instance
            job = Job(
                title=job_data['title'],
                description=job_data['description'],
                location=job_data['location'],
                salary_range=job_data['salaryRange'],
                company_name=job_data['companyName'],
                posting_date=posting_date,
                expiration_date=expiration_date,
                required_skills=job_data['requiredSkills']
            )
            
            # Save the job to the database
            job.save()
            inserted_count += 1
            print(f"Inserted job: {job.title} at {job.company_name}")
            
        except Exception as e:
            print(f"Error inserting job {job_data['title']}: {str(e)}")
    
    print(f"\nSuccessfully inserted {inserted_count} jobs out of {len(jobs)}")

if __name__ == '__main__':
    insert_fake_jobs() 