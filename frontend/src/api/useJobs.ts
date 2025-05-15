import { useQuery } from "@tanstack/vue-query"
import type { JobsRequestParams } from "../types/job"
import { listJobs } from "./jobs"

export const useJobs = (params?: JobsRequestParams) => {
  return useQuery({
    queryKey: ['jobs', params],
    queryFn: () => listJobs(params),
    placeholderData: (previousData) => previousData,
    refetchOnMount: true,
    refetchOnReconnect: true,
    staleTime: 0, // Consider data stale immediately
    gcTime: 0, // Don't cache the results
  })
}