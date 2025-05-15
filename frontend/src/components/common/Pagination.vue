<template>
  <v-pagination
    v-model="page"
    :length="length"
    :total-visible="totalVisible"
    @update:model-value="onPageChange"
  />
</template>

<script lang="ts">
import { ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'

export default {
  name: 'Pagination',
  props: {
    length: {
      type: Number,
      required: true,
    },
    totalVisible: {
      type: Number,
      default: 7,
    },
  },
  setup(props, { emit }) {
    const route = useRoute()
    const router = useRouter()
    const page = ref(parseInt(route.query.page as string) || 1)

    const onPageChange = (newPage: number) => {
      emit('onChange', newPage)
      router.push({ query: { ...route.query, page: newPage } })
    }

    return {
      page,
      onPageChange,
    }
  },
}
</script>
