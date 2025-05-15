<template>
  <Dialog
    :model-value="modelValue"
    @update:model-value="$emit('update:modelValue', $event)"
    :title="title"
    :persistent="persistent"
    @submit="submitForm"
  >
    <v-form ref="form" v-model="isFormValid" @submit.prevent="submitForm">
      <slot></slot>
    </v-form>

    <template #actions>
      <v-spacer></v-spacer>
      <v-btn color="error" variant="text" @click="close">{{ cancelText }}</v-btn>
      <v-btn color="primary" @click="submitForm" :disabled="!isFormValid">{{ submitText }}</v-btn>
    </template>
  </Dialog>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import Dialog from './Dialog.vue'

const props = defineProps({
  modelValue: {
    type: Boolean,
    required: true,
  },
  title: {
    type: String,
    default: 'Form',
  },
  persistent: {
    type: Boolean,
    default: true,
  },
  cancelText: {
    type: String,
    default: 'Cancel',
  },
  submitText: {
    type: String,
    default: 'Submit',
  },
})

const emit = defineEmits(['update:modelValue', 'submit'])

const form = ref<{ validate: () => Promise<{ valid: boolean }> } | null>(null)
const isFormValid = ref(false)

const close = () => {
  emit('update:modelValue', false)
}

const submitForm = async () => {
  const validationResult = await form.value?.validate()

  if (!validationResult?.valid) return

  emit('submit')
  close()
}

defineExpose({
  form,
  close,
  submitForm,
})
</script>

<script lang="ts">
export default {
  name: 'FormDialog',
}
</script>
