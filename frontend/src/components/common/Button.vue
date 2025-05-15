<template>
  <v-btn
    :color="color"
    :variant="variant"
    :size="size"
    :block="block"
    :rounded="rounded"
    :disabled="disabled"
    :loading="loading"
    :icon="icon"
    :prepend-icon="prependIcon"
    :append-icon="appendIcon"
    :elevation="elevation"
    :class="classes"
    @click="$emit('click', $event)"
  >
    <slot></slot>
  </v-btn>
</template>

<script setup lang="ts">
import type { PropType } from 'vue'

type ButtonVariant = 'text' | 'flat' | 'elevated' | 'tonal' | 'outlined' | 'plain' | undefined

defineProps({
  color: {
    type: String,
    default: 'primary',
  },
  variant: {
    type: String as PropType<ButtonVariant>,
    default: 'elevated',
  },
  size: {
    type: String,
    default: 'default',
    validator: (value: string) =>
      ['x-small', 'small', 'default', 'large', 'x-large'].includes(value),
  },
  block: {
    type: Boolean,
    default: false,
  },
  rounded: {
    type: [Boolean, String],
    default: false,
  },
  disabled: {
    type: Boolean,
    default: false,
  },
  loading: {
    type: Boolean,
    default: false,
  },
  icon: {
    type: [Boolean, String],
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
  elevation: {
    type: [Number, String],
    default: undefined,
  },
  classes: {
    type: [String, Array, Object],
    default: '',
  },
})

defineEmits(['click'])
</script>
