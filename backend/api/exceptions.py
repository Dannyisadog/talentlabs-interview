class JobException(Exception):
    """Base exception for job-related errors"""
    pass


class JobNotFoundError(JobException):
    """Raised when a job is not found"""
    def __init__(self, job_id):
        self.job_id = job_id
        super().__init__(f"Job with id {job_id} not found")


class JobValidationError(JobException):
    """Raised when job data validation fails"""
    def __init__(self, message):
        super().__init__(message)


class JobCreationError(JobException):
    """Raised when job creation fails"""
    def __init__(self, message):
        super().__init__(message)


class JobUpdateError(JobException):
    """Raised when job update fails"""
    def __init__(self, job_id, message):
        self.job_id = job_id
        super().__init__(f"Failed to update job {job_id}: {message}")


class JobDeletionError(JobException):
    """Raised when job deletion fails"""
    def __init__(self, job_id, message):
        self.job_id = job_id
        super().__init__(f"Failed to delete job {job_id}: {message}") 