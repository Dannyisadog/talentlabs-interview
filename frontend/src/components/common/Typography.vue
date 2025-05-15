<template>
  <component :is="tag" :class="[variantClass, weightClass, colorClass]">
    <slot />
  </component>
</template>

<script setup lang="ts">
import { computed } from 'vue'

const props = defineProps({
  variant: {
    type: String,
    default: 'body1',
    validator: (value: string) =>
      [
        'h1',
        'h2',
        'h3',
        'h4',
        'h5',
        'h6',
        'subtitle1',
        'subtitle2',
        'body1',
        'body2',
        'caption',
        'overline',
      ].includes(value),
  },
  tag: {
    type: String,
    default: 'p',
  },
  weight: {
    type: String,
    default: 'regular',
    validator: (value: string) =>
      ['thin', 'light', 'regular', 'medium', 'bold', 'black'].includes(value),
  },
  color: {
    type: String,
    default: '',
  },
  uppercase: {
    type: Boolean,
    default: false,
  },
  center: {
    type: Boolean,
    default: false,
  },
  right: {
    type: Boolean,
    default: false,
  },
})

const variantClass = computed(() => {
  const variant = props.variant

  const variantMap: Record<string, string> = {
    h1: 'text-h1',
    h2: 'text-h2',
    h3: 'text-h3',
    h4: 'text-h4',
    h5: 'text-h5',
    h6: 'text-h6',
    subtitle1: 'text-subtitle-1',
    subtitle2: 'text-subtitle-2',
    body1: 'text-body-1',
    body2: 'text-body-2',
    caption: 'text-caption',
    overline: 'text-overline',
  }

  return variantMap[variant] || 'text-body-1'
})

const weightClass = computed(() => {
  const weight = props.weight

  const weightMap: Record<string, string> = {
    thin: 'font-weight-thin',
    light: 'font-weight-light',
    regular: 'font-weight-regular',
    medium: 'font-weight-medium',
    bold: 'font-weight-bold',
    black: 'font-weight-black',
  }

  return weightMap[weight] || 'font-weight-regular'
})

const colorClass = computed(() => {
  return props.color ? `text-${props.color}` : ''
})
</script>
