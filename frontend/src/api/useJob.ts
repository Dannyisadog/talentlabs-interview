import { useQuery } from "@tanstack/vue-query"
import type { Ref } from 'vue'
import { computed, unref } from 'vue'
import { getJob } from "./jobs"

export const useJob = (jobId: string | Ref<string | undefined>) => {
  // 讓 id 是 reactive 的
  const id = computed(() => unref(jobId))
  return useQuery({
    queryKey: computed(() => ['job', id.value]),
    queryFn: () => {
      if (!id.value) throw new Error('Job ID is required')
      return getJob(id.value)
    },
    enabled: computed(() => !!id.value),
    placeholderData: (previousData) => previousData,
  })
}
