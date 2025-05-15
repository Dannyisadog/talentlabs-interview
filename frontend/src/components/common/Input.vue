<template>
  <v-text-field
    :modelValue="innerValue"
    @update:model-value="updateValue"
    :label="label"
    :placeholder="placeholder"
    :hint="hint"
    :variant="variant"
    :density="density"
    :disabled="disabled"
    :readonly="readonly"
    :clearable="clearable"
    :persistent-hint="persistentHint"
    :error="error"
    :error-messages="errorMessages"
    :required="required"
    :prepend-icon="prependIcon"
    :append-icon="appendIcon"
    :class="classes"
  >
    <slot></slot>
  </v-text-field>
</template>

<script setup lang="ts">
import type { PropType } from 'vue'
import { computed } from 'vue'

const props = defineProps({
  modelValue: {
    type: [String, Number],
    default: '',
  },
  label: {
    type: String,
    default: '',
  },
  placeholder: {
    type: String,
    default: '',
  },
  hint: {
    type: String,
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
    validator: (value: string) =>
      ['plain', 'filled', 'outlined', 'underlined', 'solo'].includes(value),
  },
  density: {
    type: String as PropType<'default' | 'comfortable' | 'compact' | undefined>,
    default: 'default',
    validator: (value: string) => ['default', 'comfortable', 'compact'].includes(value),
  },
  disabled: {
    type: Boolean,
    default: false,
  },
  readonly: {
    type: Boolean,
    default: false,
  },
  clearable: {
    type: Boolean,
    default: false,
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
  prependIcon: {
    type: String,
    default: '',
  },
  appendIcon: {
    type: String,
    default: '',
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
