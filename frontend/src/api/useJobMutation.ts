import { useMutation, useQueryClient } from "@tanstack/vue-query"
import type { BaseJob } from "../types/job"
import { addJob } from "./jobs"
import { JOBS_QUERY_KEY } from "./useJobs"

export const useJobMutation = () => {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: (job: BaseJob) => addJob(job),
    onSuccess: () => {
      // Invalidate and refetch jobs query
      queryClient.invalidateQueries({ queryKey: [JOBS_QUERY_KEY] })
    },
  })
}
