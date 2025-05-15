<template>
  <div>
    <v-btn color="primary" @click="openDialog"> Create New Job </v-btn>

    <JobCreateFormDialog v-model="showDialog" @create="handleCreateJob" />
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import type { BaseJob } from '../../../types/job'
import JobCreateFormDialog from './JobCreateFormDialog.vue'

const showDialog = ref(false)

const openDialog = () => {
  showDialog.value = true
}

const handleCreateJob = (job: BaseJob) => {
  console.log('New job created:', job)
  // Here you would typically send the job to your backend API
  // Example: await api.jobs.create(job);
}
</script>
