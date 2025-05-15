<template>
  <v-card
    :title="title"
    :subtitle="subtitle"
    :variant="variant"
    :color="color"
    :elevation="elevation"
    :rounded="rounded"
    :border="border"
    :class="classes"
  >
    <!-- <v-card-item v-if="$slots.item">
      <slot name="item"></slot>
    </v-card-item> -->

    <v-card-text v-if="text || $slots.default">
      <template v-if="text">{{ text }}</template>
      <slot v-else></slot>
    </v-card-text>

    <v-card-actions v-if="$slots.actions">
      <slot name="actions"></slot>
    </v-card-actions>
  </v-card>
</template>

<script setup lang="ts">
import type { PropType } from 'vue'

type CardVariant = 'text' | 'elevated' | 'flat' | 'tonal' | 'outlined' | 'plain' | undefined

defineProps({
  title: {
    type: String,
    default: '',
  },
  subtitle: {
    type: String,
    default: '',
  },
  text: {
    type: String,
    default: '',
  },
  variant: {
    type: String as PropType<CardVariant>,
    default: 'elevated',
  },
  color: {
    type: String,
    default: '',
  },
  elevation: {
    type: [Number, String],
    default: undefined,
  },
  rounded: {
    type: [Boolean, String, Number],
    default: undefined,
  },
  border: {
    type: [Boolean, String],
    default: false,
  },
  classes: {
    type: [String, Array, Object],
    default: '',
  },
})
</script>

<style>
.v-card {
  cursor: pointer;
}
</style>
