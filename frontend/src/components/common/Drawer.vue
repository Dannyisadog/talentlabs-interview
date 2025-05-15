<template>
  <div class="drawer-container">
    <div
      v-if="modelValue && temporary"
      class="drawer-backdrop"
      @click.stop="handleBackdropClick"
    ></div>
    <v-navigation-drawer
      :modelValue="modelValue"
      @update:modelValue="$emit('update:modelValue', $event)"
      :location="location"
      :temporary="temporary"
      :color="color"
      :width="width"
      :elevation="elevation"
      :rail="rail"
      :expandOnHover="expandOnHover"
      :class="classes"
      class="custom-drawer"
      :style="{ zIndex: 10000 }"
    >
      <v-list v-if="$slots.list">
        <slot name="list"></slot>
      </v-list>

      <template v-if="$slots.prepend" #prepend>
        <slot name="prepend"></slot>
      </template>

      <template v-if="$slots.append" #append>
        <slot name="append"></slot>
      </template>

      <slot></slot>
    </v-navigation-drawer>
  </div>
</template>

<script setup lang="ts">
import type { PropType } from 'vue'
import { onBeforeUnmount, watch } from 'vue'

type DrawerLocation = 'left' | 'right' | 'bottom' | 'top' | undefined

const props = defineProps({
  modelValue: {
    type: Boolean,
    default: false,
  },
  location: {
    type: String as PropType<DrawerLocation>,
    default: 'left',
  },
  temporary: {
    type: Boolean,
    default: false,
  },
  color: {
    type: String,
    default: undefined,
  },
  width: {
    type: [Number, String],
    default: 256,
  },
  elevation: {
    type: [Number, String],
    default: undefined,
  },
  rail: {
    type: Boolean,
    default: false,
  },
  expandOnHover: {
    type: Boolean,
    default: false,
  },
  classes: {
    type: [String, Array, Object],
    default: '',
  },
  closeOnBackdropClick: {
    type: Boolean,
    default: true,
  },
})

const emit = defineEmits(['update:modelValue', 'click:backdrop'])

// Handle backdrop click
const handleBackdropClick = () => {
  emit('click:backdrop')
  if (props.closeOnBackdropClick) {
    emit('update:modelValue', false)
  }
}

// Store original body styles
let originalOverflow = ''
let originalPosition = ''
let originalWidth = ''
let originalHeight = ''
let originalTop = ''
let scrollY = 0

// Completely disable scrolling when drawer is open
watch(
  () => props.modelValue,
  (isOpen) => {
    if (isOpen && props.temporary) {
      // Store original values
      scrollY = window.scrollY
      originalOverflow = document.body.style.overflow
      originalPosition = document.body.style.position
      originalWidth = document.body.style.width
      originalHeight = document.body.style.height
      originalTop = document.body.style.top

      // Disable scrolling completely
      document.body.style.position = 'fixed'
      document.body.style.width = '100%'
      document.body.style.height = '100%'
      document.body.style.top = `-${scrollY}px`

      // Add a class to indicate drawer is open
      document.body.classList.add('drawer-open')
    } else {
      // Restore original values
      document.body.style.overflow = originalOverflow
      document.body.style.position = originalPosition
      document.body.style.width = originalWidth
      document.body.style.height = originalHeight
      document.body.style.top = originalTop

      // Remove the class
      document.body.classList.remove('drawer-open')

      // Restore scroll position
      window.scrollTo(0, scrollY)
    }
  },
  { immediate: true },
)

// Clean up on component unmount
onBeforeUnmount(() => {
  if (document.body.classList.contains('drawer-open')) {
    document.body.style.overflow = originalOverflow
    document.body.style.position = originalPosition
    document.body.style.width = originalWidth
    document.body.style.height = originalHeight
    document.body.style.top = originalTop
    document.body.classList.remove('drawer-open')
    window.scrollTo(0, scrollY)
  }
})
</script>

<style scoped>
.drawer-container {
  position: relative;
}

.drawer-backdrop {
  position: fixed;
  inset: 0;
  background-color: rgba(0, 0, 0, 0.5);
  z-index: 9999;
  cursor: pointer;
  width: 100%;
  height: 100%;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
}

:deep(.custom-drawer) {
  z-index: 10000 !important;
}

:deep(.v-navigation-drawer) {
  z-index: 10000 !important;
}
</style>
