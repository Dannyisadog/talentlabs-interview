<template>
  <div>
    <v-btn color="primary" @click="openDialog"> Create New Job </v-btn>

    <JobCreateFormDialog v-model="showDialog" />
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import JobCreateFormDialog from './JobCreateFormDialog.vue'

const showDialog = ref(false)

const openDialog = () => {
  showDialog.value = true
}
</script>
