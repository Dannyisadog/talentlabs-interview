<template>
  <v-checkbox
    :modelValue="innerValue"
    @update:model-value="updateValue"
    :label="label"
    :hint="hint"
    :disabled="disabled"
    :readonly="readonly"
    :error="error"
    :error-messages="errorMessages"
    :persistent-hint="persistentHint"
    :density="density"
    :color="color"
    :hide-details="hideDetails"
    :class="classes"
  >
    <slot></slot>
  </v-checkbox>
</template>

<script setup lang="ts">
import type { PropType } from 'vue'
import { computed } from 'vue'

type Density = 'default' | 'comfortable' | 'compact' | undefined

const props = defineProps({
  modelValue: {
    type: [Boolean, Array],
    default: false,
  },
  label: {
    type: String,
    default: '',
  },
  hint: {
    type: String,
    default: '',
  },
  disabled: {
    type: Boolean,
    default: false,
  },
  readonly: {
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
  persistentHint: {
    type: Boolean,
    default: false,
  },
  density: {
    type: String as PropType<Density>,
    default: 'default',
    validator: (value: string) => ['default', 'comfortable', 'compact'].includes(value),
  },
  color: {
    type: String,
    default: 'primary',
  },
  hideDetails: {
    type: [Boolean, String] as PropType<boolean | 'auto' | undefined>,
    default: false,
  },
  classes: {
    type: [String, Array, Object],
    default: '',
  },
})

const emit = defineEmits(['update:model-value'])

const innerValue = computed(() => props.modelValue)

const updateValue = (value: any) => {
  emit('update:model-value', value)
}
</script>
