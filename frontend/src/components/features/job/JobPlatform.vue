<template>
  <v-app-bar color="white" elevation="4">
    <v-app-bar-title class="text-primary">Interview</v-app-bar-title>
    <v-spacer></v-spacer>
    <Button @click="showCreateDialog = true">Create Job</Button>
    <LanguageSwitcher />
  </v-app-bar>
  <v-main>
    <v-container>
      <!-- Filters Section -->
      <v-row class="mb-4">
        <v-col cols="12" md="6">
          <Input
            v-model="searchInput"
            label="Search Jobs"
            prepend-inner-icon="mdi-magnify"
            clearable
            @update:model-value="debouncedSearch"
          />
        </v-col>
        <v-col cols="12" md="6">
          <Input
            v-model="locationInput"
            label="Location"
            prepend-inner-icon="mdi-map-marker"
            clearable
            @update:model-value="debouncedLocation"
          />
        </v-col>
      </v-row>

      <!-- Sort Section -->
      <v-row class="mb-4">
        <v-col cols="12" md="6">
          <Select
            v-model="filters.orderBy"
            label="Sort By"
            :items="[
              { title: 'Posting Date', value: 'postingDate' },
              { title: 'Expiration Date', value: 'expirationDate' },
            ]"
            prepend-inner-icon="mdi-sort"
            @update:model-value="handleFilterChange"
          />
        </v-col>
        <v-col cols="12" md="6">
          <Select
            v-model="filters.orderDirection"
            label="Sort Direction"
            :items="[
              { title: 'Ascending', value: 'asc' },
              { title: 'Descending', value: 'desc' },
            ]"
            prepend-inner-icon="mdi-sort-variant"
            @update:model-value="handleFilterChange"
          />
        </v-col>
      </v-row>

      <JobCard v-for="job in jobData?.results" :key="job.id" :job="job" />
      <JobDetailDrawer
        :key="jobId"
        :job="jobDetail"
        :modelValue="jobId !== undefined"
        @close="handleClose"
      />
      <JobCreateFormDialog v-model="showCreateDialog" />
      <Pagination
        :total="jobData?.total_count"
        :page="jobData?.page"
        :limit="10"
        :length="jobData?.total_count ? Math.ceil(jobData?.total_count / 10) : 0"
        @change="handlePageChange"
      />
    </v-container>
  </v-main>
</template>

<script setup lang="ts">
import { useJob } from '@/api/useJob'
import { useJobs } from '@/api/useJobs'
import { LanguageSwitcher } from '@/components/common'
import Button from '@/components/common/Button.vue'
import Input from '@/components/common/Input.vue'
import Pagination from '@/components/common/Pagination.vue'
import Select from '@/components/common/Select.vue'
import { computed, ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import JobCard from './JobCard.vue'
import JobCreateFormDialog from './JobCreateFormDialog.vue'
import JobDetailDrawer from './JobDetailDrawer.vue'

const route = useRoute()
const router = useRouter()

const showCreateDialog = ref(false)
const searchInput = ref('')
const locationInput = ref('')
const searchTimeout = ref<number | null>(null)
const locationTimeout = ref<number | null>(null)

const filters = ref({
  search: '',
  location: '',
  orderBy: 'postingDate' as 'postingDate' | 'expirationDate',
  orderDirection: 'desc' as 'asc' | 'desc',
})

const debouncedSearch = () => {
  if (searchTimeout.value) {
    clearTimeout(searchTimeout.value)
  }

  searchTimeout.value = setTimeout(() => {
    filters.value.search = searchInput.value
    handleFilterChange()
  }, 500) // 500ms debounce delay
}

const debouncedLocation = () => {
  if (locationTimeout.value) {
    clearTimeout(locationTimeout.value)
  }

  locationTimeout.value = setTimeout(() => {
    filters.value.location = locationInput.value
    handleFilterChange()
  }, 500) // 500ms debounce delay
}

const queryParams = computed(() => ({
  page: Number(route.query.page) || 1,
  limit: 10,
  search: filters.value.search || undefined,
  location: filters.value.location || undefined,
  orderBy: filters.value.orderBy,
  orderDirection: filters.value.orderDirection,
}))

const { data: jobData } = useJobs(queryParams)

const jobId = ref<string | undefined>(undefined)
const { data: jobDetail } = useJob(jobId)

watch(
  () => route.params,
  (newParams) => {
    jobId.value = newParams.id as string
  },
)

// Initialize searchInput from URL query params on component mount
watch(
  () => route.query.search,
  (newSearch) => {
    if (newSearch !== undefined) {
      searchInput.value = newSearch as string
      filters.value.search = newSearch as string
    }
  },
  { immediate: true },
)

// Initialize locationInput from URL query params on component mount
watch(
  () => route.query.location,
  (newLocation) => {
    if (newLocation !== undefined) {
      locationInput.value = newLocation as string
      filters.value.location = newLocation as string
    }
  },
  { immediate: true },
)

const handleClose = () => {
  router.push({
    name: 'job-list',
    params: {
      ...route.params,
    },
    query: {
      ...route.query,
    },
  })
}

const handlePageChange = (page: number) => {
  router.push({
    query: {
      ...route.query,
      page: page.toString(),
    },
  })
}

const handleFilterChange = () => {
  router.push({
    query: {
      ...route.query,
      page: '1',
      ...Object.fromEntries(
        Object.entries(queryParams.value)
          .filter(([_, value]) => value !== undefined)
          .map(([key, value]) => [key, Array.isArray(value) ? value.join(',') : value]),
      ),
    },
  })
}
</script>
