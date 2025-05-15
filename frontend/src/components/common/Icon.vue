<template>
  <v-icon
    :icon="getIcon"
    :color="color"
    :size="size"
    :density="density"
    :start="start"
    :end="end"
    :class="classes"
  >
    <slot></slot>
  </v-icon>
</template>

<script setup lang="ts">
import type { PropType } from 'vue'
import { computed } from 'vue'

type Density = 'default' | 'comfortable' | 'compact' | undefined

const props = defineProps({
  name: {
    type: String,
    default: '',
  },
  icon: {
    type: String,
    default: '',
  },
  color: {
    type: String,
    default: undefined,
  },
  size: {
    type: [String, Number],
    default: undefined,
  },
  density: {
    type: String as PropType<Density>,
    default: 'default',
  },
  start: {
    type: Boolean,
    default: false,
  },
  end: {
    type: Boolean,
    default: false,
  },
  classes: {
    type: [String, Array, Object],
    default: '',
  },
})

const getIcon = computed(() => {
  // If a direct icon path is provided, use it
  if (props.icon) {
    return props.icon
  }

  // Otherwise, prepend 'mdi-' to the icon name for Vuetify's built-in MDI icons
  if (props.name) {
    return `mdi-${props.name}`
  }

  return ''
})
</script>
