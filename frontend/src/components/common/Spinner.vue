<template>
  <v-progress-circular
    :indeterminate="indeterminate"
    :size="size"
    :width="width"
    :color="color"
    :model-value="modelValue"
    :class="classes"
  >
    <slot></slot>
  </v-progress-circular>
</template>

<script setup lang="ts">
defineProps({
  indeterminate: {
    type: Boolean,
    default: true,
  },
  modelValue: {
    type: [Number, String],
    default: 0,
  },
  size: {
    type: [Number, String],
    default: 36,
  },
  width: {
    type: [Number, String],
    default: 4,
  },
  color: {
    type: String,
    default: 'primary',
  },
  classes: {
    type: [String, Array, Object],
    default: '',
  },
})
</script>
