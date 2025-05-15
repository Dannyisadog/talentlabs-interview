<template>
  <v-select
    :modelValue="innerValue"
    @update:model-value="updateValue"
    :items="items"
    :label="label"
    :hint="hint"
    :variant="variant"
    :density="density"
    :disabled="disabled"
    :readonly="readonly"
    :clearable="clearable"
    :chips="chips"
    :multiple="multiple"
    :persistent-hint="persistentHint"
    :error="error"
    :error-messages="errorMessages"
    :item-title="itemTitle"
    :item-value="itemValue"
    :return-object="returnObject"
    :class="classes"
  >
    <template v-if="$slots['prepend']" #prepend>
      <slot name="prepend"></slot>
    </template>
    <template v-if="$slots['append']" #append>
      <slot name="append"></slot>
    </template>
  </v-select>
</template>

<script setup lang="ts">
import type { PropType } from 'vue'
import { computed } from 'vue'

type SelectVariant =
  | 'plain'
  | 'filled'
  | 'outlined'
  | 'underlined'
  | 'solo'
  | 'solo-inverted'
  | 'solo-filled'
  | undefined
type Density = 'default' | 'comfortable' | 'compact' | undefined

const props = defineProps({
  modelValue: {
    type: [String, Number, Object, Array],
    default: null,
  },
  items: {
    type: Array,
    default: () => [],
  },
  label: {
    type: String,
    default: '',
  },
  hint: {
    type: String,
    default: '',
  },
  variant: {
    type: String as PropType<SelectVariant>,
    default: 'outlined',
  },
  density: {
    type: String as PropType<Density>,
    default: 'default',
  },
  disabled: {
    type: Boolean,
    default: false,
  },
  readonly: {
    type: Boolean,
    default: false,
  },
  clearable: {
    type: Boolean,
    default: false,
  },
  chips: {
    type: Boolean,
    default: false,
  },
  multiple: {
    type: Boolean,
    default: false,
  },
  persistentHint: {
    type: Boolean,
    default: false,
  },
  error: {
    type: Boolean,
    default: false,
  },
  errorMessages: {
    type: [String, Array] as PropType<string | readonly string[] | null | undefined>,
    default: '',
  },
  itemTitle: {
    type: String,
    default: 'title',
  },
  itemValue: {
    type: String,
    default: 'value',
  },
  returnObject: {
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

const updateValue = (value: any) => {
  emit('update:model-value', value)
}
</script>
