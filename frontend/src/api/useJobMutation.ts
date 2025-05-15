import { useMutation } from "@tanstack/vue-query"
import type { BaseJob } from "../types/job"
import { addJob } from "./jobs"

export const useJobMutation = () => {
  return useMutation({
    mutationFn: (job: BaseJob) => addJob(job),
  })
}
