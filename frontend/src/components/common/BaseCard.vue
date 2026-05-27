<template>
  <component
    :is="as"
    class="rounded-2xl border bg-white shadow-sm transition"
    :class="[paddingClass, selected ? 'border-blue-400 ring-2 ring-blue-100' : 'border-slate-200', interactive ? 'hover:-translate-y-0.5 hover:border-blue-300 hover:shadow-md' : '']"
  >
    <slot />
  </component>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  as: {
    type: String,
    default: 'div',
  },
  padding: {
    type: String,
    default: 'md',
  },
  selected: {
    type: Boolean,
    default: false,
  },
  interactive: {
    type: Boolean,
    default: false,
  },
})

const paddingClass = computed(
  () =>
    ({
      none: '',
      sm: 'p-3',
      md: 'p-4',
      lg: 'p-5',
    })[props.padding] ?? 'p-4',
)
</script>
