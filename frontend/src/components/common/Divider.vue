<template>
  <v-divider
    :thickness="thickness"
    :color="color"
    :inset="inset"
    :vertical="vertical"
    :class="classes"
  ></v-divider>
</template>

<script setup lang="ts">
defineProps({
  thickness: {
    type: [Number, String],
    default: undefined,
  },
  color: {
    type: String,
    default: 'grey-lighten-1',
  },
  inset: {
    type: Boolean,
    default: false,
  },
  vertical: {
    type: Boolean,
    default: false,
  },
  classes: {
    type: [String, Array, Object],
    default: '',
  },
})
</script>
