<template>
  <v-dialog
    :model-value="modelValue"
    @update:model-value="$emit('update:modelValue', $event)"
    :max-width="maxWidth"
    :persistent="persistent"
  >
    <v-card>
      <v-card-title>
        <slot name="title">{{ title }}</slot>
        <v-spacer></v-spacer>
        <Button v-if="closable" icon @click="close">
          <v-icon>mdi-close</v-icon>
        </Button>
      </v-card-title>

      <v-card-text>
        <slot></slot>
      </v-card-text>

      <v-card-actions v-if="$slots.actions">
        <slot name="actions"></slot>
      </v-card-actions>

      <v-card-actions v-else-if="showDefaultActions">
        <v-spacer></v-spacer>
        <Button color="error" variant="text" @click="close">
          {{ cancelText }}
        </Button>
        <Button color="primary" @click="submit">
          {{ confirmText }}
        </Button>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script setup lang="ts">
import Button from './Button.vue'

defineProps({
  modelValue: {
    type: Boolean,
    required: true,
  },
  title: {
    type: String,
    default: '',
  },
  maxWidth: {
    type: [String, Number],
    default: 600,
  },
  persistent: {
    type: Boolean,
    default: false,
  },
  closable: {
    type: Boolean,
    default: true,
  },
  showDefaultActions: {
    type: Boolean,
    default: true,
  },
  confirmText: {
    type: String,
    default: 'Confirm',
  },
  cancelText: {
    type: String,
    default: 'Cancel',
  },
})

const emit = defineEmits(['update:modelValue', 'submit'])

const close = () => {
  emit('update:modelValue', false)
}

const submit = () => {
  emit('submit')
  close()
}

defineExpose({
  close,
  submit,
})
</script>
