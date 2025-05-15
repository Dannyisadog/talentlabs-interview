<template>
  <v-alert
    :type="type"
    :title="title"
    :text="text"
    :variant="variant"
    :border="border"
    :icon="icon"
    :prominent="prominent"
    :closable="closable"
    :class="classes"
    :model-value="innerValue"
    @update:model-value="updateValue"
  >
    <slot></slot>
  </v-alert>
</template>

<script setup lang="ts">
import type { PropType } from 'vue'
import { computed } from 'vue'

type AlertType = 'success' | 'info' | 'warning' | 'error' | undefined
type AlertVariant = 'text' | 'elevated' | 'flat' | 'tonal' | 'outlined' | 'plain' | undefined
type AlertBorder = boolean | 'top' | 'end' | 'bottom' | 'start' | undefined
type IconValue = string | undefined

const props = defineProps({
  modelValue: {
    type: Boolean,
    default: true,
  },
  type: {
    type: String as PropType<AlertType>,
    default: 'info',
  },
  title: {
    type: String,
    default: '',
  },
  text: {
    type: String,
    default: '',
  },
  variant: {
    type: String as PropType<AlertVariant>,
    default: 'elevated',
  },
  border: {
    type: [Boolean, String] as PropType<AlertBorder>,
    default: false,
  },
  icon: {
    type: [Boolean, String] as PropType<false | IconValue>,
    default: false,
  },
  prominent: {
    type: Boolean,
    default: false,
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

const emit = defineEmits(['update:model-value'])

const innerValue = computed(() => props.modelValue)

const updateValue = (value: boolean) => {
  emit('update:model-value', value)
}
</script>
