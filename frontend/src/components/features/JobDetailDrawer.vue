<template>
  <Drawer
    v-model="modelValue"
    location="right"
    temporary
    :width="600"
    color="white"
    class="job-detail-drawer"
    :closeOnBackdropClick="true"
    @click:backdrop="$emit('update:modelValue', false)"
  >
    <button class="close-button" @click="$emit('update:modelValue', false)" aria-label="Close">
      <Icon name="close" size="small" />
    </button>

    <div v-if="isLoading" class="pa-4">
      <Typography variant="body1">{{ t('jobList.loading') }}</Typography>
    </div>

    <div v-else-if="job" class="job-detail-content">
      <div class="job-header mb-4">
        <Typography variant="h4" class="job-title">{{ job.title }}</Typography>
        <Badge class="mt-2">{{ formatPosting(job.postingDate) }}</Badge>
      </div>

      <div class="job-company mb-4">
        <Typography variant="subtitle1" class="company-name">
          <Icon name="office-building" size="small" class="mr-1" /> {{ job.companyName }}
        </Typography>
        <Typography variant="body1" class="job-location d-flex align-center mt-1">
          <Icon name="map-marker" size="small" class="mr-1" /> {{ job.location }}
        </Typography>
      </div>

      <Divider />

      <div class="job-salary my-4">
        <Typography variant="subtitle1" class="d-flex align-center">
          <Icon name="currency-usd" size="small" class="mr-1" />{{ t('jobList.salaryRange') }}
        </Typography>
        <Typography variant="body1" class="salary-value">{{
          formatSalary(job.salaryRange)
        }}</Typography>
      </div>

      <div class="job-description mb-4">
        <Typography variant="subtitle1">{{ t('jobList.description') }}</Typography>
        <Typography variant="body1" class="mt-1">{{ job.description }}</Typography>
      </div>

      <div class="job-skills mb-4">
        <Typography variant="subtitle1" class="d-flex align-center">
          <Icon name="star" size="small" class="mr-1" />{{ t('jobList.requiredSkills') }}
        </Typography>
        <div class="d-flex flex-wrap gap-2 mt-2">
          <Badge v-for="(skill, index) in job.requiredSkills" :key="index">{{ skill }}</Badge>
        </div>
      </div>

      <div class="job-dates mb-4">
        <Typography variant="subtitle1" class="d-flex align-center">
          <Icon name="calendar" size="small" class="mr-1" />{{ t('jobList.jobDetails') }}
        </Typography>
        <div class="mt-1">
          <Typography variant="body2" class="d-flex align-center">
            <Icon name="calendar" size="x-small" class="mr-1" />{{ t('jobList.posted') }}:
            {{ formatDate(job.postingDate) }}
          </Typography>
          <Typography variant="body2" class="d-flex align-center">
            <Icon name="calendar" size="x-small" class="mr-1" />{{ t('jobList.expires') }}:
            {{ formatDate(job.expirationDate) }}
          </Typography>
        </div>
      </div>

      <div class="job-actions">
        <Button color="primary" class="mr-2">
          <Icon name="email" size="small" class="mr-1" />{{ t('jobList.applyNow') }}
        </Button>
      </div>
    </div>

    <div v-else class="pa-4">
      <Typography variant="body1">{{ t('jobList.noJobSelected') }}</Typography>
    </div>
  </Drawer>
</template>

<script lang="ts">
import type { PropType } from 'vue'
import { computed, defineComponent } from 'vue'
import { useI18n } from 'vue-i18n'
import type { Job, SalaryRange } from '../../types/job'
import { Badge, Button, Divider, Drawer, Icon, Typography } from '../common'

export default defineComponent({
  name: 'JobDetailDrawer',
  components: {
    Drawer,
    Typography,
    Badge,
    Icon,
    Divider,
    Button,
  },
  props: {
    modelValue: {
      type: Boolean,
      default: false,
    },
    job: {
      type: Object as PropType<Job>,
      required: false,
    },
    isLoading: {
      type: Boolean,
      default: false,
    },
  },
  emits: ['update:modelValue', 'click:backdrop'],
  setup() {
    const { t, locale } = useI18n()
    const currentLocale = computed(() => {
      return locale.value === 'zh' ? 'zh-CN' : 'en-US'
    })

    return { t, currentLocale }
  },
  methods: {
    formatSalary(salaryRange: SalaryRange): string {
      if (!salaryRange) return ''

      if (typeof salaryRange === 'string') {
        return salaryRange
      }

      const currency = salaryRange.currency || '$'
      return `${currency}${salaryRange.min.toLocaleString()} - ${currency}${salaryRange.max.toLocaleString()}`
    },
    formatPosting(date: string | Date): string {
      if (!date) return ''

      const dateObj = typeof date === 'string' ? new Date(date) : date
      const now = new Date()
      const diffTime = Math.abs(now.getTime() - dateObj.getTime())
      const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24))

      if (diffDays === 0) {
        return this.t('jobList.today')
      } else if (diffDays === 1) {
        return this.t('jobList.yesterday')
      } else {
        return `${diffDays} ${this.t('jobList.daysAgo')}`
      }
    },
    formatDate(date: string | Date): string {
      if (!date) return ''

      const dateObj = typeof date === 'string' ? new Date(date) : date
      return dateObj.toLocaleDateString(this.currentLocale, {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
      })
    },
  },
})
</script>

<style>
/* Global style to ensure drawer and backdrop are always on top */
.v-navigation-drawer {
  z-index: 10000 !important;
}

.drawer-backdrop {
  z-index: 9999 !important;
}
</style>

<style scoped>
.job-detail-drawer {
  overflow-y: auto;
  position: fixed;
  right: 0;
  top: 0;
  bottom: 0;
  box-shadow: -2px 0 10px rgba(0, 0, 0, 0.1);
}

.job-detail-content {
  padding: 16px;
}

.job-title {
  word-wrap: break-word;
  word-break: break-word;
  overflow-wrap: break-word;
  max-width: 100%;
  display: block;
  padding-right: 16px;
  line-height: 1.3;
  font-size: 2rem;
}

.gap-2 {
  gap: 0.5rem;
}

.close-button {
  position: absolute;
  top: 10px;
  right: 10px;
  z-index: 1;
  background: transparent;
  border: none;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  width: 32px;
  height: 32px;
  transition: background-color 0.2s;
}

.close-button:hover {
  background-color: rgba(0, 0, 0, 0.1);
}
</style>
