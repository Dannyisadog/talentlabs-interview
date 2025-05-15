<template>
  <Drawer
    :modelValue="modelValue"
    temporary
    location="right"
    :width="600"
    color="white"
    class="job-detail-drawer"
    @click:backdrop="closeDrawer"
  >
    <div v-if="parsedJob" class="job-detail-content">
      <button class="close-button" @click="closeDrawer">
        <Icon name="close" size="medium" />
      </button>
      <div class="job-header mb-4">
        <Typography variant="h4" class="job-title">{{ parsedJob.title }}</Typography>
        <Badge class="mt-2">{{ formatPosting(parsedJob.postingDate) }}</Badge>
      </div>

      <div class="job-company mb-4">
        <Typography variant="subtitle1" class="company-name">
          <Icon name="office-building" size="small" class="mr-1" /> {{ parsedJob.companyName }}
        </Typography>
        <Typography variant="body1" class="job-location d-flex align-center mt-1">
          <Icon name="map-marker" size="small" class="mr-1" /> {{ parsedJob.location }}
        </Typography>
      </div>

      <Divider />

      <div class="job-salary my-4">
        <Typography variant="subtitle1" class="d-flex align-center">
          <Icon name="currency-usd" size="small" class="mr-1" />{{ t('jobList.salaryRange') }}
        </Typography>
        <Typography variant="body1" class="salary-value">{{
          formatSalary(parsedJob.salaryRange)
        }}</Typography>
      </div>

      <div class="job-description mb-4">
        <Typography variant="subtitle1">{{ t('jobList.description') }}</Typography>
        <Typography variant="body1" class="mt-1">{{ parsedJob.description }}</Typography>
      </div>

      <div class="job-skills mb-4">
        <Typography variant="subtitle1" class="d-flex align-center">
          <Icon name="star" size="small" class="mr-1" />{{ t('jobList.requiredSkills') }}
        </Typography>
        <div class="d-flex flex-wrap gap-2 mt-2">
          <Badge v-for="(skill, index) in parsedJob.requiredSkills" :key="index">{{ skill }}</Badge>
        </div>
      </div>

      <div class="job-dates mb-4">
        <Typography variant="subtitle1" class="d-flex align-center">
          <Icon name="calendar" size="small" class="mr-1" />{{ t('jobList.jobDetails') }}
        </Typography>
        <div class="mt-1">
          <Typography variant="body2" class="d-flex align-center">
            <Icon name="calendar" size="x-small" class="mr-1" />{{ t('jobList.posted') }}:
            {{ formatDate(parsedJob.postingDate) }}
          </Typography>
          <Typography variant="body2" class="d-flex align-center">
            <Icon name="calendar" size="x-small" class="mr-1" />{{ t('jobList.expires') }}:
            {{ formatDate(parsedJob.expirationDate) }}
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
import { Badge, Button, Divider, Drawer, Icon, Typography } from '@/components/common'
import type { Job, SalaryRange } from '@/types/job'
import type { PropType } from 'vue'
import { computed, defineComponent } from 'vue'
import { useI18n } from 'vue-i18n'

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
    job: {
      type: [Object, String] as PropType<Job | string | undefined>,
      default: undefined,
    },
    modelValue: {
      type: Boolean,
      default: false,
    },
  },
  emits: ['close'],
  setup(props, { emit }) {
    const { t, locale } = useI18n()

    const currentLocale = computed(() => {
      return locale.value === 'zh' ? 'zh-CN' : 'en-US'
    })

    const parsedJob = computed((): Job | undefined => {
      if (!props.job) {
        return undefined
      }

      let jobData: any

      if (typeof props.job === 'string') {
        try {
          jobData = JSON.parse(props.job)
        } catch (e) {
          console.error('Failed to parse job string:', e)
          return undefined
        }
      } else {
        jobData = props.job
      }

      if (typeof jobData !== 'object' || jobData === null) {
        console.error('Job data is not an object after potential parsing:', jobData)
        return undefined
      }

      const tempJob = { ...jobData }

      if (tempJob.postingDate) {
        if (typeof tempJob.postingDate === 'string') {
          tempJob.postingDate = new Date(tempJob.postingDate)
        }
        if (!(tempJob.postingDate instanceof Date) || isNaN(tempJob.postingDate.getTime())) {
          console.warn('Invalid postingDate after processing:', jobData.postingDate)
          tempJob.postingDate = undefined
        }
      }

      if (tempJob.expirationDate) {
        if (typeof tempJob.expirationDate === 'string') {
          tempJob.expirationDate = new Date(tempJob.expirationDate)
        }
        if (!(tempJob.expirationDate instanceof Date) || isNaN(tempJob.expirationDate.getTime())) {
          console.warn('Invalid expirationDate after processing:', jobData.expirationDate)
          tempJob.expirationDate = undefined
        }
      }
      return tempJob as Job
    })

    const closeDrawer = () => {
      // trigger the close event
      emit('close')
    }

    return { t, currentLocale, parsedJob, closeDrawer }
  },
  methods: {
    formatSalary(salaryRange: SalaryRange | undefined): string {
      if (!salaryRange) {
        return '' // Or some default like 'N/A'
      }
      if (typeof salaryRange === 'string') {
        return salaryRange
      }
      // Ensure min/max are numbers before calling toLocaleString
      if (typeof salaryRange.min !== 'number' || typeof salaryRange.max !== 'number') {
        return 'Invalid salary data'
      }
      const currency = salaryRange.currency || '$'
      return `${currency}${salaryRange.min.toLocaleString()} - ${currency}${salaryRange.max.toLocaleString()}`
    },
    formatPosting(date: Date | undefined): string {
      if (!date || !(date instanceof Date) || isNaN(date.getTime())) {
        return this.t('jobList.dateNotAvailable') || 'Date N/A'
      }
      const now = new Date()
      const diffTime = Math.abs(now.getTime() - date.getTime())
      const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24))

      if (diffDays === 0) {
        return this.t('jobList.today')
      } else if (diffDays === 1) {
        return this.t('jobList.yesterday')
      } else {
        return `${diffDays} ${this.t('jobList.daysAgo')}`
      }
    },
    formatDate(date: Date | undefined): string {
      if (!date || !(date instanceof Date) || isNaN(date.getTime())) {
        return this.t('jobList.dateNotAvailable') || 'Date N/A'
      }
      return date.toLocaleDateString(this.currentLocale, {
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
