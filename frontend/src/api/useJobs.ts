import { useQuery } from "@tanstack/vue-query"
import type { ComputedRef } from "vue"
import { computed } from "vue"
import type { JobsRequestParams } from "../types/job"
import { listJobs } from "./jobs"

export const JOBS_QUERY_KEY = 'jobs'

export const useJobs = (params: ComputedRef<JobsRequestParams>) => {
  const queryKey = computed(() => [JOBS_QUERY_KEY, params.value])

  return useQuery({
    queryKey,
    queryFn: () => listJobs(params.value),
    placeholderData: (previousData) => previousData,
    refetchOnMount: true,
    refetchOnReconnect: true,
    refetchOnWindowFocus: true,
  })
}