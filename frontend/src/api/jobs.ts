import type { BaseJob, Job, JobsRequestParams, JobsResponse } from '../types/job';
import { get, post } from '../utils/httpClient';

const jobsApiPath = '/jobs/';

export const listJobs = async (params?: JobsRequestParams): Promise<JobsResponse> => {
  return await get<JobsResponse>(jobsApiPath, { params });
};

export const getJob = async (id: string): Promise<Job> => {
  return await get<Job>(`${jobsApiPath}${id}`);
};

export const addJob = async (job: BaseJob): Promise<Job> => {
  return await post<Job>(jobsApiPath, job);
};