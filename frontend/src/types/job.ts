export type SalaryRange = string | {
  min: number;
  max: number;
  currency?: string;
};

export enum JobStatus {
  Active = 'active',
  Expired = 'expired',
  Scheduled = 'scheduled'
}

export type JobsRequestParams = {
  page?: number;
  limit?: number;
  search?: string;
  status?: JobStatus;
  skills?: string[];
  location?: string;
  salaryMin?: number;
  salaryMax?: number;
  orderBy?: 'postingDate' | 'expirationDate';
  orderDirection?: 'asc' | 'desc';
}

export type BaseJob = {
  title: string;
  description: string;
  location: string;
  salaryRange: SalaryRange;
  companyName: string;
  postingDate: Date;
  expirationDate: Date;
  requiredSkills: string[];
}

export type Job = BaseJob & {
  id: string;
  createdAt: string;
  updatedAt: string;
  isActive: boolean;
  isDeleted: boolean;
}

export type PaginatedResponse<T> = {
  results: T[];
  total_count: number;
  page: number;
  page_size: number;
  total_pages: number;
}

export type JobsResponse = PaginatedResponse<Job>;
