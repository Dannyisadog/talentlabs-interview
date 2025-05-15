<template>
  <v-avatar :color="color" :size="size" :rounded="rounded" :variant="variant" :class="classes">
    <v-img v-if="src" :src="src" alt="avatar"></v-img>
    <span v-else-if="text">{{ text }}</span>
    <v-icon v-else-if="icon" :icon="icon"></v-icon>
    <slot v-else></slot>
  </v-avatar>
</template>

<script setup lang="ts">
import type { PropType } from 'vue'

type AvatarVariant = 'flat' | 'elevated' | 'tonal' | 'outlined' | 'text' | 'plain' | undefined

defineProps({
  src: {
    type: String,
    default: '',
  },
  text: {
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
    default: 'default',
  },
  rounded: {
    type: [Boolean, String],
    default: undefined,
  },
  variant: {
    type: String as PropType<AvatarVariant>,
    default: 'flat',
  },
  classes: {
    type: [String, Array, Object],
    default: '',
  },
})
</script>
