<template>
  <span
    class="inline-grid shrink-0 place-items-center rounded-2xl"
    :class="[sizeClass, colorClass, variant === 'solid' ? 'text-white' : '']"
  >
    <component :is="icon" :class="iconSizeClass" />
  </span>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  icon: {
    type: [Object, Function],
    required: true,
  },
  color: {
    type: String,
    default: 'blue',
  },
  size: {
    type: String,
    default: 'md',
  },
  variant: {
    type: String,
    default: 'soft',
  },
})

const sizeClass = computed(
  () =>
    ({
      sm: 'h-8 w-8',
      md: 'h-10 w-10',
      lg: 'h-12 w-12',
      xl: 'h-14 w-14',
    })[props.size] ?? 'h-10 w-10',
)

const iconSizeClass = computed(
  () =>
    ({
      sm: 'h-4 w-4',
      md: 'h-5 w-5',
      lg: 'h-6 w-6',
      xl: 'h-7 w-7',
    })[props.size] ?? 'h-5 w-5',
)

const colorClass = computed(() => {
  const solid = {
    blue: 'bg-blue-600',
    purple: 'bg-violet-600',
    slate: 'bg-slate-700',
  }

  const soft = {
    blue: 'bg-blue-100 text-blue-700',
    purple: 'bg-violet-100 text-violet-700',
    slate: 'bg-slate-100 text-slate-700',
  }

  return props.variant === 'solid'
    ? solid[props.color] ?? solid.blue
    : soft[props.color] ?? soft.blue
})
</script>
