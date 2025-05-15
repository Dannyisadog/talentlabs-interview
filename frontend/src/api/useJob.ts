import { useQuery } from "@tanstack/vue-query"
import { getJob } from "./jobs"

export const useJob = (jobId: string) => {
  return useQuery({
    queryKey: ['job', jobId],
    queryFn: () => {
      if (!jobId) throw new Error('Job ID is required')
      return getJob(jobId)
    },
    enabled: !!jobId,
    placeholderData: (previousData) => previousData,
  })
}
