<template>
  <v-app>
    <v-main class="main-container">
      <JobPlatform />
    </v-main>
  </v-app>
</template>

<style scoped>
.main-container {
  padding-top: 64px;
}
</style>

<script lang="ts">
import { defineComponent } from 'vue'
import JobPlatform from './components/features/job/JobPlatform.vue'

export default defineComponent({
  name: 'App',
  components: {
    JobPlatform,
  },
})
</script>
