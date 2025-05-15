<template>
  <div class="job-list-container">
    <div class="filters-section">
      <v-text-field
        :model-value="searchQuery"
        :label="t('jobList.search')"
        prepend-inner-icon="mdi-magnify"
        clearable
        @keydown.enter="handleSearch"
        @update:model-value="(val) => (searchQuery = val)"
        @click:clear="handleClear"
      ></v-text-field>

      <div class="filter-row">
        <v-select
          v-model="statusFilter"
          :items="statusOptions"
          :label="t('jobList.status')"
          @update:model-value="updateFilters"
        ></v-select>

        <v-select
          v-model="sortBy"
          :items="sortOptions"
          :label="t('jobList.sortBy')"
          @update:model-value="updateFilters"
        ></v-select>

        <v-select
          v-model="sortDirection"
          :items="directionOptions"
          :label="t('jobList.sortDirection')"
          @update:model-value="updateFilters"
        ></v-select>
      </div>
    </div>

    <div v-if="isLoading" class="loading-state">
      <div class="job-list">
        <v-skeleton-loader
          v-for="n in 5"
          :key="n"
          type="card"
          class="mb-4"
          height="200"
        ></v-skeleton-loader>
      </div>
    </div>
    <div v-else>
      <div class="job-list">
        <JobCard v-for="job in jobs" :key="job.id" :job="job" @click="showJobDetails(job)" />
      </div>
      <div class="pagination">
        <button
          :disabled="currentPage === 1"
          @click="changePage(currentPage - 1)"
          class="pagination-button"
        >
          Previous
        </button>
        <span class="page-info">Page {{ currentPage }}</span>
        <button
          :disabled="!hasMorePages"
          @click="changePage(currentPage + 1)"
          class="pagination-button"
        >
          Next
        </button>
      </div>
    </div>
    <JobDetailDrawer v-model="isDrawerOpen" :job="selectedJob" />
  </div>
</template>

<script lang="ts">
import { computed, defineComponent, ref, watch } from 'vue'
import { useI18n } from 'vue-i18n'
import { useRoute, useRouter } from 'vue-router'
import { useJob } from '../api/useJob'
import { useJobs } from '../api/useJobs'
import { Typography } from '../components/common'
import JobCard from '../components/features/JobCard.vue'
import JobDetailDrawer from '../components/features/JobDetailDrawer.vue'
import type { Job, JobsResponse } from '../types/job'
import { JobStatus } from '../types/job'

export default defineComponent({
  name: 'JobListView',
  components: {
    JobCard,
    JobDetailDrawer,
    Typography,
  },
  setup() {
    const { t } = useI18n()
    const route = useRoute()
    const router = useRouter()
    const pageSize = 10

    // Initialize state from URL query parameters
    const currentPage = ref(Number(route.query.page) || 1)
    const searchQuery = ref((route.query.search as string) || '')
    const statusFilter = ref((route.query.status as JobStatus) || undefined)
    const sortBy = ref((route.query.orderBy as 'postingDate' | 'expirationDate') || 'postingDate')
    const sortDirection = ref((route.query.orderDirection as 'asc' | 'desc') || 'desc')

    // Create a computed property for the query parameters
    const queryParams = computed(() => ({
      page: currentPage.value,
      limit: pageSize,
      search: searchQuery.value,
      status: statusFilter.value,
      orderBy: sortBy.value,
      orderDirection: sortDirection.value,
    }))

    const { data: jobsData, isLoading, refetch } = useJobs(queryParams.value)

    const jobs = computed(() => (jobsData.value as JobsResponse)?.results || [])
    const hasMorePages = computed(() => jobs.value.length === pageSize)

    const statusOptions = [
      { title: t('jobList.all'), value: undefined },
      { title: t('jobList.active'), value: JobStatus.Active },
      { title: t('jobList.expired'), value: JobStatus.Expired },
      { title: t('jobList.scheduled'), value: JobStatus.Scheduled },
    ]

    const sortOptions = [
      { title: t('jobList.postingDate'), value: 'postingDate' },
      { title: t('jobList.expirationDate'), value: 'expirationDate' },
    ]

    const directionOptions = [
      { title: t('jobList.newestFirst'), value: 'desc' },
      { title: t('jobList.oldestFirst'), value: 'asc' },
    ]

    const updateFilters = () => {
      currentPage.value = 1 // Reset to first page when filters change
      updateUrl()
      refetch() // Force refetch when filters change
    }

    const changePage = (page: number) => {
      currentPage.value = page
      updateUrl()
      refetch() // Force refetch when page changes
    }

    const updateUrl = () => {
      const query: Record<string, string> = {}
      if (currentPage.value > 1) query.page = currentPage.value.toString()
      if (searchQuery.value) query.search = searchQuery.value
      if (statusFilter.value) query.status = statusFilter.value
      if (sortBy.value !== 'postingDate') query.orderBy = sortBy.value
      if (sortDirection.value !== 'desc') query.orderDirection = sortDirection.value

      router.push({ query })
    }

    // Watch for URL changes
    watch(
      () => route.query,
      (newQuery) => {
        currentPage.value = Number(newQuery.page) || 1
        searchQuery.value = (newQuery.search as string) || ''
        statusFilter.value = (newQuery.status as JobStatus) || undefined
        sortBy.value = (newQuery.orderBy as 'postingDate' | 'expirationDate') || 'postingDate'
        sortDirection.value = (newQuery.orderDirection as 'asc' | 'desc') || 'desc'
        refetch() // Force refetch when URL changes
      },
      { deep: true },
    )

    // Watch for filter changes (excluding search)
    watch([statusFilter, sortBy, sortDirection], () => {
      updateFilters()
    })

    return {
      t,
      route,
      router,
      jobs,
      isLoading,
      currentPage,
      hasMorePages,
      changePage,
      searchQuery,
      statusFilter,
      sortBy,
      sortDirection,
      statusOptions,
      sortOptions,
      directionOptions,
      updateFilters,
    }
  },
  data() {
    return {
      isDrawerOpen: false,
      selectedJob: undefined as Job | undefined,
    }
  },
  mounted() {
    // Check if job ID is in URL and open drawer if it is
    if (this.route.params.id) {
      this.openJobFromUrl(this.route.params.id as string)
    }
  },
  watch: {
    // Watch for route changes to update the drawer
    'route.params.id': function (newId) {
      if (newId) {
        this.openJobFromUrl(newId as string)
      } else {
        this.isDrawerOpen = false
        this.selectedJob = undefined
      }
    },
    // Close drawer should update URL
    isDrawerOpen(newValue) {
      if (!newValue && this.route.params.id) {
        this.router.push({ name: 'job-list' })
      }
    },
  },
  methods: {
    handleSearch() {
      this.updateFilters()
    },
    handleClear() {
      this.searchQuery = ''
      this.updateFilters()
    },
    showJobDetails(job: Job) {
      this.selectedJob = job
      this.isDrawerOpen = true
      // Update URL with job ID
      this.router.push({ name: 'job-details', params: { id: job.id } })
    },
    openJobFromUrl(jobId: string) {
      // First try to find the job in the current page's jobs
      const job = this.jobs.find((job: Job) => job.id === jobId)
      if (job) {
        this.selectedJob = job
        this.isDrawerOpen = true
      } else {
        // If job not found in current page, fetch it individually
        const { data: jobData, isLoading } = useJob(jobId)
        watch(jobData, (newJob) => {
          if (newJob) {
            this.selectedJob = newJob
            this.isDrawerOpen = true
          } else {
            // If job not found, redirect to job list
            this.router.push({ name: 'job-list' })
          }
        })
      }
    },
  },
})
</script>

<style scoped>
.job-list-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 1rem;
}

.filters-section {
  margin: 1.5rem 0;
}

.filter-row {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
  margin-top: 1rem;
}

.job-list {
  margin-top: 1.5rem;
}

.job-list-title {
  font-weight: bold !important;
}

.loading-state {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 200px;
}

.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 1rem;
  margin: 2rem 0;
}

.pagination-button {
  padding: 0.5rem 1rem;
  border: 1px solid #ccc;
  border-radius: 4px;
  background: white;
  cursor: pointer;
}

.pagination-button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.page-info {
  font-size: 1rem;
}
</style>
