<template>
  <FormDialog
    :model-value="modelValue"
    @update:model-value="$emit('update:modelValue', $event)"
    :persistent="true"
    @submit="handleSubmit"
    submitText="Create Job"
    max-width="800px"
    :closable="false"
    :title="''"
    class="job-create-dialog"
    :loading="isPending"
  >
    <v-container @click="formTouched = true" class="pa-6 pt-8 position-relative" fluid>
      <button type="button" class="close-btn" @click="$emit('update:modelValue', false)">
        <v-icon>mdi-close</v-icon>
      </button>
      <div class="mb-6">
        <div class="d-flex align-center mb-4">
          <v-icon size="30" class="mr-3 text-grey-darken-1">mdi-briefcase-outline</v-icon>
          <span class="text-h6 font-weight-regular">Job Details</span>
        </div>

        <v-row>
          <v-col cols="12" md="6">
            <Input
              v-model="job.title"
              label="Job Title"
              required
              prepend-inner-icon="mdi-format-title"
              :error-messages="formTouched && !job.title ? 'Title is required' : ''"
              :error="formTouched && !job.title"
              variant="outlined"
              density="comfortable"
              bg-color="white"
            />
          </v-col>

          <v-col cols="12" md="6">
            <Input
              v-model="job.companyName"
              label="Company Name"
              required
              prepend-inner-icon="mdi-office-building-outline"
              :error-messages="formTouched && !job.companyName ? 'Company name is required' : ''"
              :error="formTouched && !job.companyName"
              variant="outlined"
              density="comfortable"
              bg-color="white"
            />
          </v-col>

          <v-col cols="12">
            <v-textarea
              v-model="job.description"
              label="Job Description"
              required
              rows="4"
              prepend-inner-icon="mdi-text-box-outline"
              :rules="formTouched ? [(v) => !!v || 'Description is required'] : []"
              variant="outlined"
              density="comfortable"
              bg-color="white"
            ></v-textarea>
          </v-col>

          <v-col cols="12">
            <Input
              v-model="job.location"
              label="Location"
              required
              prepend-inner-icon="mdi-map-marker-outline"
              :error-messages="formTouched && !job.location ? 'Location is required' : ''"
              :error="formTouched && !job.location"
              variant="outlined"
              density="comfortable"
              bg-color="white"
            />
          </v-col>
        </v-row>
      </div>

      <!-- Divider -->
      <v-divider class="mb-6"></v-divider>

      <!-- Salary Section -->
      <div class="mb-6">
        <div class="d-flex align-center mb-4">
          <v-icon size="30" class="mr-3 text-grey-darken-1">mdi-currency-usd</v-icon>
          <span class="text-h6 font-weight-regular">Salary Information</span>
        </div>

        <div class="mb-3 ml-1">Salary Type</div>
        <div class="mb-4">
          <v-radio-group v-model="salaryType" inline density="compact">
            <v-radio label="Range" value="range" color="primary"></v-radio>
            <v-radio label="Text" value="text" color="primary"></v-radio>
          </v-radio-group>
        </div>

        <v-row v-if="salaryType === 'text'">
          <v-col cols="12">
            <Input
              v-model="textSalary"
              label="Salary Description"
              required
              prepend-inner-icon="mdi-cash"
              :error-messages="formTouched && !textSalary ? 'Salary description is required' : ''"
              :error="formTouched && !textSalary"
              variant="outlined"
              density="comfortable"
              bg-color="white"
            />
          </v-col>
        </v-row>

        <v-row v-else>
          <v-col cols="10" md="4">
            <Input
              v-model.number="rangeSalary.min"
              label="Minimum Salary"
              type="number"
              required
              prepend-inner-icon="mdi-arrow-down-bold"
              :error-messages="formTouched && !rangeSalary.min ? 'Minimum salary is required' : ''"
              :error="formTouched && !rangeSalary.min"
              variant="outlined"
              density="comfortable"
              bg-color="white"
            />
          </v-col>

          <v-col cols="10" md="4">
            <Input
              v-model.number="rangeSalary.max"
              label="Maximum Salary"
              type="number"
              required
              prepend-inner-icon="mdi-arrow-up-bold"
              :error-messages="
                formTouched && !rangeSalary.max
                  ? 'Maximum salary is required'
                  : formTouched && rangeSalary.max < rangeSalary.min
                    ? 'Maximum must be greater than minimum'
                    : ''
              "
              :error="formTouched && (!rangeSalary.max || rangeSalary.max < rangeSalary.min)"
              variant="outlined"
              density="comfortable"
              bg-color="white"
            />
          </v-col>

          <v-col cols="3" md="4">
            <Select
              v-model="rangeSalary.currency"
              label="Currency"
              :items="['USD', 'TWD', 'SGD', 'JPY']"
              prepend-inner-icon="mdi-currency-usd"
              variant="outlined"
              density="comfortable"
              bg-color="white"
            />
          </v-col>
        </v-row>
      </div>

      <!-- Divider -->
      <v-divider class="mb-6"></v-divider>

      <!-- Dates Section -->
      <div class="mb-6">
        <div class="d-flex align-center mb-4">
          <v-icon size="30" class="mr-3 text-grey-darken-1">mdi-calendar-range</v-icon>
          <span class="text-h6 font-weight-regular">Job Timeline</span>
        </div>

        <v-row>
          <v-col cols="12" md="6">
            <DatePicker
              v-model="postingDate"
              label="Posting Date"
              prepend-inner-icon="mdi-calendar-plus"
              :error-messages="formTouched && !postingDate ? 'Posting date is required' : ''"
              :error="formTouched && !postingDate"
              required
              variant="outlined"
              density="comfortable"
              bg-color="white"
            />
          </v-col>

          <v-col cols="12" md="6">
            <DatePicker
              v-model="expirationDate"
              label="Expiration Date"
              prepend-inner-icon="mdi-calendar-end"
              :error-messages="
                formTouched && !expirationDate
                  ? 'Expiration date is required'
                  : formTouched && new Date(expirationDate) <= new Date(postingDate)
                    ? 'Expiration date must be after posting date'
                    : ''
              "
              :error="
                formTouched &&
                (!expirationDate || new Date(expirationDate) <= new Date(postingDate))
              "
              required
              variant="outlined"
              density="comfortable"
              bg-color="white"
            />
          </v-col>
        </v-row>
      </div>

      <!-- Divider -->
      <v-divider class="mb-6"></v-divider>

      <!-- Skills Section -->
      <div>
        <div class="d-flex align-center mb-4">
          <v-icon size="30" class="mr-3 text-grey-darken-1">mdi-lightbulb-outline</v-icon>
          <span class="text-h6 font-weight-regular">Required Skills</span>
        </div>

        <v-row>
          <v-col cols="12">
            <v-combobox
              v-model="job.requiredSkills"
              label="Required Skills"
              multiple
              chips
              closable-chips
              prepend-inner-icon="mdi-lightning-bolt"
              hint="Type skill name and press Enter to add"
              persistent-hint
              :error-messages="
                formTouched && job.requiredSkills.length === 0
                  ? 'At least one skill is required'
                  : ''
              "
              :error="formTouched && job.requiredSkills.length === 0"
              variant="outlined"
              density="comfortable"
              bg-color="white"
            >
              <template v-slot:chip="{ props, item }">
                <v-chip v-bind="props" :text="item.raw" color="primary" label closable></v-chip>
              </template>
            </v-combobox>
          </v-col>
        </v-row>
      </div>
    </v-container>
  </FormDialog>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useJobMutation } from '../../../api/useJobMutation'
import { DatePicker, FormDialog, Input, Select } from '../../../components/common'
import type { BaseJob } from '../../../types/job'

const props = defineProps({
  modelValue: {
    type: Boolean,
    required: true,
  },
})

const emit = defineEmits(['update:modelValue', 'create'])
const { mutate: createJob, isPending } = useJobMutation()

const formTouched = ref(false)
const salaryType = ref('range')
const textSalary = ref('')
const postingDate = ref(new Date().toISOString().substr(0, 10))
const expirationDate = ref(
  new Date(Date.now() + 30 * 24 * 60 * 60 * 1000).toISOString().substr(0, 10),
)

const rangeSalary = ref({
  min: 0,
  max: 0,
  currency: 'USD',
})

const job = ref<Omit<BaseJob, 'salaryRange' | 'postingDate' | 'expirationDate'>>({
  title: '',
  description: '',
  location: '',
  companyName: '',
  requiredSkills: [],
})

const handleSubmit = () => {
  formTouched.value = true

  // Create the job object with all required fields
  const newJob: BaseJob = {
    ...job.value,
    salaryRange: salaryType.value === 'text' ? textSalary.value : rangeSalary.value,
    postingDate: new Date(postingDate.value),
    expirationDate: new Date(expirationDate.value),
  }

  createJob(newJob, {
    onSuccess: () => {
      emit('update:modelValue', false)
    },
  })
}
</script>

<script lang="ts">
export default {
  name: 'JobCreateFormDialog',
}
</script>

<style scoped>
.close-btn {
  position: absolute;
  top: 2px;
  right: 2px;
  z-index: 100;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

@media (max-width: 600px) {
  .job-create-dialog :deep(.v-dialog) {
    margin: 0 !important;
    position: fixed !important;
    top: 0 !important;
    left: 0 !important;
    width: 100vw !important;
    height: 100vh !important;
    max-width: none !important;
    max-height: none !important;
    border-radius: 0 !important;
    overflow-y: auto !important;
  }

  .job-create-dialog :deep(.v-card) {
    min-height: 100vh !important;
    border-radius: 0 !important;
  }

  .text-h6 {
    font-size: 1.1rem !important;
  }

  .close-btn {
    top: 8px;
    right: 8px;
  }
}
</style>
