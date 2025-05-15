<template>
  <Card class="job-card" @click="handleJobClick">
    <div class="job-header">
      <Typography :variant="isMobile ? 'h5' : 'h4'" class="job-title">{{ job.title }}</Typography>
      <Badge class="job-badge">
        <Icon name="calendar-month" size="small" class="badge-icon" />
        {{ job.postingDate }}
      </Badge>
    </div>

    <div class="job-company">
      <Typography variant="body1" class="company-name">
        <Icon name="office-building" size="small" class="company-icon" /> {{ job.companyName }}
      </Typography>
      <Typography variant="body2" class="job-location">
        <Icon name="map-marker" size="small" /> {{ job.location }}
      </Typography>
    </div>

    <Divider class="custom-divider" />

    <div class="job-salary">
      <Typography variant="body1" class="salary-value">
        <Icon name="currency-usd" size="small" class="salary-icon" />
        {{ formatSalary(job.salaryRange) }}</Typography
      >
    </div>

    <div class="job-skills">
      <div
        v-for="(skill, index) in job.requiredSkills.slice(0, 3)"
        :key="index"
        class="skill-badge"
      >
        <Badge>{{ skill }}</Badge>
      </div>
      <Badge v-if="job.requiredSkills.length > 3" class="more-skills"
        >+{{ job.requiredSkills.length - 3 }}</Badge
      >
    </div>
  </Card>
</template>

<script lang="ts">
import { Badge, Button, Card, Divider, Icon, Typography } from '@/components/common'
import type { Job, SalaryRange } from '@/types/job'
import type { PropType } from 'vue'
import { defineComponent, onMounted, onUnmounted, ref } from 'vue'
import { useI18n } from 'vue-i18n'
import { useRoute, useRouter } from 'vue-router'

export default defineComponent({
  name: 'JobCard',
  components: {
    Card,
    Typography,
    Badge,
    Icon,
    Divider,
    Button,
  },
  props: {
    job: {
      type: Object as PropType<Job>,
      required: true,
    },
  },
  emits: ['click'],
  setup(props) {
    const { t } = useI18n()
    const isMobile = ref(false)
    const router = useRouter()
    const route = useRoute()

    const checkScreenSize = () => {
      isMobile.value = window.innerWidth <= 480
    }

    const handleJobClick = () => {
      router.push({
        path: `/${props.job.id}`,
        query: route.query,
      })
    }

    onMounted(() => {
      checkScreenSize()
      window.addEventListener('resize', checkScreenSize)
    })

    onUnmounted(() => {
      window.removeEventListener('resize', checkScreenSize)
    })

    return {
      isMobile,
      t,
      handleJobClick,
    }
  },
  methods: {
    formatSalary(salaryRange: SalaryRange): string {
      if (typeof salaryRange === 'string') {
        return salaryRange
      }

      const currency = salaryRange.currency || '$'
      return `${currency}${salaryRange.min.toLocaleString()} - ${currency}${salaryRange.max.toLocaleString()}`
    },
  },
})
</script>

<style scoped>
.job-card {
  padding: 0 1rem;
  margin-bottom: 1.25rem;
  transition: all 0.3s ease;
  width: 100%;
  cursor: pointer;
  border-radius: 12px;
  border-left: none;
  box-shadow:
    rgba(0, 0, 0, 0.05) 0px 6px 24px 0px,
    rgba(0, 0, 0, 0.08) 0px 0px 0px 1px;
  position: relative;
  overflow: hidden;
  background-color: #ffffff;
}

.job-card::before {
  content: '';
  position: absolute;
  left: 0;
  top: 0;
  height: 100%;
  width: 6px;
  background: linear-gradient(to bottom, #3498db, #2980b9);
}

.job-card:hover {
  transform: translateY(-4px);
  box-shadow:
    rgba(0, 0, 0, 0.1) 0px 10px 30px 0px,
    rgba(0, 0, 0, 0.08) 0px 0px 0px 1px;
}

.job-title {
  font-weight: 600;
  color: #2c3e50;
  margin-bottom: 4px;
  font-size: 1.5rem;
  line-height: 1.4;
  transition: font-size 0.3s ease;
}

.job-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 1rem;
}

.job-badge {
  display: flex;
  align-items: center;
  gap: 4px;
  background-color: rgba(52, 152, 219, 0.1);
  border-radius: 20px;
  padding: 4px 12px;
  font-size: 0.85rem;
  color: #3498db;
  font-weight: 500;
}

.badge-icon {
  color: #3498db;
}

.job-company {
  display: flex;
  justify-content: space-between;
  margin-bottom: 1.25rem;
}

.company-name,
.job-location,
.salary-value {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #555;
}

.job-location {
  display: flex;
  align-items: center;
  gap: 6px;
  color: #777;
  font-size: 0.9rem;
}

.company-icon,
.salary-icon {
  color: #666;
}

.custom-divider {
  margin: 0.75rem 0;
  opacity: 0.6;
}

.job-salary {
  display: flex;
  justify-content: space-between;
  margin: 1rem 0;
}

.salary-value {
  font-weight: 600;
  color: #2c3e50;
}

.job-skills {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.skill-badge {
  transition: transform 0.2s ease;
}

.skill-badge .badge {
  background-color: #f8f9fa;
  border: 1px solid #e9ecef;
  border-radius: 20px;
  padding: 4px 12px;
  font-size: 0.85rem;
  color: #495057;
  font-weight: 500;
}

.more-skills {
  background-color: #e9ecef;
  border-radius: 20px;
  padding: 4px 12px;
  font-size: 0.85rem;
  color: #6c757d;
  font-weight: 500;
}

.skill-badge:hover {
  transform: scale(1.05);
}

.job-footer {
  display: flex;
  justify-content: space-between;
  margin-top: 1.5rem;
}

.view-btn {
  flex: 1;
  border-radius: 8px;
  border: 1.5px solid #3498db;
  color: #3498db;
  font-weight: 500;
  padding: 10px 16px;
  transition: all 0.2s ease;
  background-color: rgba(52, 152, 219, 0.03);
}

.view-btn:hover {
  background-color: rgba(52, 152, 219, 0.1);
  transform: translateY(-2px);
}

.save-btn {
  border-radius: 8px;
  color: #3498db;
  background: transparent;
  padding: 10px 12px;
  transition: all 0.2s ease;
}

.save-btn:hover {
  background-color: rgba(52, 152, 219, 0.05);
}

.button-icon {
  margin-right: 6px;
}

/* Responsive styles */
@media (max-width: 1200px) {
  .job-title {
    font-size: 1.35rem;
    line-height: 1.35;
  }
}

@media (max-width: 992px) {
  .job-title {
    font-size: 1.25rem;
    line-height: 1.3;
  }
}

@media (max-width: 768px) {
  .job-card {
    padding: 1.25rem;
  }

  .job-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.75rem;
  }

  .job-title {
    font-size: 1.15rem;
    line-height: 1.25;
  }

  .job-footer {
    flex-direction: column;
    gap: 0.75rem;
  }

  .job-footer button {
    width: 100%;
  }
}

@media (max-width: 480px) {
  .job-card {
    padding: 0 0.75rem;
    width: 100%;
    min-width: 0;
    max-width: 100%;
    box-sizing: border-box;
    border-radius: 8px;
    overflow: hidden;
  }

  .job-title {
    font-size: 1rem;
    line-height: 1.3;
    max-width: 100%;
    overflow: visible;
    white-space: normal;
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    margin-bottom: 0.5rem;
  }

  .job-badge {
    font-size: 0.7rem;
    padding: 2px 6px;
    white-space: nowrap;
  }

  .job-company {
    margin-bottom: 0.5rem;
    flex-wrap: nowrap;
    flex-direction: row;
    justify-content: space-between;
    align-items: center;
    gap: 0.5rem;
  }

  .company-name,
  .job-location {
    font-size: 0.8rem;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }

  .company-name {
    max-width: 55%;
  }

  .job-location {
    max-width: 45%;
  }

  .custom-divider {
    margin: 0.5rem 0;
  }

  .job-salary {
    margin: 0.8rem 0;
    font-size: 0.85rem;
  }

  .salary-value {
    font-size: 0.85rem;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }

  .job-skills {
    flex-wrap: nowrap;
    overflow-x: auto;
    padding-bottom: 0.25rem;
    -webkit-overflow-scrolling: touch;
    scrollbar-width: none; /* Firefox */
    gap: 0.25rem;
  }

  .skill-badge .badge {
    padding: 2px 8px;
    font-size: 0.75rem;
  }

  .more-skills {
    padding: 2px 8px;
    font-size: 0.75rem;
  }

  .job-skills::-webkit-scrollbar {
    display: none; /* Safari and Chrome */
  }

  .skill-badge {
    flex-shrink: 0;
  }

  .job-footer {
    margin-top: 0.75rem;
    flex-direction: row;
    gap: 0.5rem;
  }

  .view-btn {
    padding: 6px 8px;
    font-size: 0.8rem;
    border-width: 1px;
  }

  .save-btn {
    padding: 6px;
    width: auto !important;
    min-width: 36px;
  }

  .button-icon {
    margin-right: 4px;
  }

  .hide-text-mobile {
    display: none;
  }
}
</style>
