<template>
  <v-app>
    <v-app-bar>
      <v-app-bar-title>
        <Typography class="font-weight-bold">Interview</Typography>
      </v-app-bar-title>
      <v-spacer></v-spacer>
      <v-btn color="primary" class="mr-4" prepend-icon="mdi-plus" @click="openJobDialog">
        Create
      </v-btn>
      <LanguageSwitcher />
    </v-app-bar>
    <v-main class="main-container">
      <RouterView />
    </v-main>

    <JobCreateFormDialog v-model="showJobDialog" @create="handleCreateJob" />
  </v-app>
</template>

<style scoped>
.main-container {
  padding-top: 64px;
}
</style>

<script setup lang="ts">
import { ref } from 'vue'
import { useJobMutation } from './api/useJobMutation'
import { LanguageSwitcher, Typography } from './components/common'
import JobCreateFormDialog from './components/features/job/JobCreateFormDialog.vue'
import type { BaseJob } from './types/job'

const showJobDialog = ref(false)
const { mutate: createJob, isPending } = useJobMutation()

const openJobDialog = () => {
  showJobDialog.value = true
}

const handleCreateJob = (job: BaseJob) => {
  createJob(job, {
    onSuccess: () => {
      showJobDialog.value = false
    },
  })
}
</script>
