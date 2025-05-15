<template>
  <v-menu
    ref="menu"
    v-model="isOpen"
    :close-on-content-click="false"
    transition="scale-transition"
    offset-y
    min-width="auto"
    :open-on-click="true"
    :open-on-focus="false"
    :open-on-hover="false"
  >
    <template v-slot:activator="{ props }">
      <Input
        :model-value="formattedDate"
        @update:model-value="updateValue"
        :label="label"
        readonly
        v-bind="props"
        :error-messages="errorMessages"
        :error="error"
        :required="required"
        :placeholder="placeholder"
        :hint="hint"
        :persistent-hint="persistentHint"
        :class="classes"
        :variant="variant"
        :prepend-icon="prependIcon"
        :prepend-inner-icon="prependInnerIcon"
        :density="density"
        :bg-color="bgColor"
      />
    </template>
    <v-date-picker :model-value="innerValue" @update:model-value="handleDateSelect"></v-date-picker>
  </v-menu>
</template>

<script setup lang="ts">
import type { PropType } from 'vue'
import { computed, ref } from 'vue'
import { Input } from './'

const props = defineProps({
  modelValue: {
    type: String,
    default: '',
  },
  label: {
    type: String,
    default: 'Date',
  },
  placeholder: {
    type: String,
    default: '',
  },
  hint: {
    type: String,
    default: '',
  },
  persistentHint: {
    type: Boolean,
    default: false,
  },
  error: {
    type: Boolean,
    default: false,
  },
  errorMessages: {
    type: [String, Array] as PropType<string | readonly string[] | null | undefined>,
    default: '',
  },
  required: {
    type: Boolean,
    default: false,
  },
  closeOnSelect: {
    type: Boolean,
    default: true,
  },
  classes: {
    type: [String, Array, Object],
    default: '',
  },
  variant: {
    type: String as PropType<
      | 'plain'
      | 'filled'
      | 'outlined'
      | 'underlined'
      | 'solo'
      | 'solo-inverted'
      | 'solo-filled'
      | undefined
    >,
    default: 'outlined',
  },
  prependIcon: {
    type: String,
    default: '',
  },
  prependInnerIcon: {
    type: String,
    default: '',
  },
  density: {
    type: String as PropType<'default' | 'comfortable' | 'compact' | undefined>,
    default: 'default',
  },
  bgColor: {
    type: String,
    default: '',
  },
})

const emit = defineEmits(['update:model-value'])

const isOpen = ref(false)
const innerValue = computed(() => props.modelValue)
const formattedDate = computed(() => props.modelValue)

const handleDateSelect = (value: string) => {
  emit('update:model-value', value)

  if (props.closeOnSelect) {
    isOpen.value = false
  }
}

const updateValue = (value: string) => {
  emit('update:model-value', value)
}
</script>

<script lang="ts">
export default {
  name: 'DatePicker',
}
</script>
