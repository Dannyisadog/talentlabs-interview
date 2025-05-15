<template>
  <v-chip
    :text="text"
    :color="color"
    :variant="variant"
    :size="size"
    :density="density"
    :pill="pill"
    :closable="closable"
    :class="classes"
    @click="$emit('click', $event)"
  >
    <slot></slot>
  </v-chip>
</template>

<script setup lang="ts">
import type { PropType } from 'vue'

type ChipVariant = 'text' | 'outlined' | 'elevated' | 'flat' | 'tonal' | 'plain' | undefined
type ChipSize = 'x-small' | 'small' | 'default' | 'large' | 'x-large' | undefined
type ChipDensity = 'default' | 'comfortable' | 'compact' | undefined

const props = defineProps({
  text: {
    type: [String, Number],
    default: '',
  },
  color: {
    type: String,
    default: 'primary',
  },
  variant: {
    type: String as PropType<ChipVariant>,
    default: 'tonal',
  },
  size: {
    type: String as PropType<ChipSize>,
    default: 'default',
  },
  density: {
    type: String as PropType<ChipDensity>,
    default: 'default',
  },
  pill: {
    type: Boolean,
    default: true,
  },
  closable: {
    type: Boolean,
    default: false,
  },
  classes: {
    type: [String, Array, Object],
    default: '',
  },
})

defineEmits(['click'])
</script>
