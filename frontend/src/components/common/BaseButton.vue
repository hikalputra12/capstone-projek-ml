<template>
  <component
    :is="buttonComponent"
    :to="to || undefined"
    :href="href || undefined"
    :target="external ? '_blank' : undefined"
    :rel="external ? 'noreferrer' : undefined"
    :type="isNativeButton ? type : undefined"
    :disabled="isNativeButton ? disabled : undefined"
    class="inline-flex items-center justify-center gap-2 rounded-xl font-bold transition focus:outline-none focus:ring-2 focus:ring-blue-200 focus:ring-offset-2"
    :class="[variantClass, sizeClass, fullWidth ? 'w-full' : '', disabled ? 'cursor-not-allowed opacity-60' : '']"
  >
    <slot />
  </component>
</template>

<script setup>
import { RouterLink } from 'vue-router'
import { computed } from 'vue'

const props = defineProps({
  to: {
    type: [String, Object],
    default: '',
  },
  href: {
    type: String,
    default: '',
  },
  type: {
    type: String,
    default: 'button',
  },
  variant: {
    type: String,
    default: 'primary',
  },
  size: {
    type: String,
    default: 'md',
  },
  fullWidth: {
    type: Boolean,
    default: false,
  },
  disabled: {
    type: Boolean,
    default: false,
  },
  external: {
    type: Boolean,
    default: false,
  },
})

const buttonComponent = computed(() => {
  if (props.to) return RouterLink
  if (props.href) return 'a'
  return 'button'
})

const isNativeButton = computed(() => buttonComponent.value === 'button')

const variantClass = computed(
  () =>
    ({
      primary: 'bg-blue-600 text-white shadow-sm hover:bg-blue-700',
      secondary: 'border border-slate-200 bg-white text-slate-700 shadow-sm hover:border-blue-200 hover:bg-blue-50 hover:text-blue-700',
      subtle: 'bg-slate-100 text-slate-700 hover:bg-slate-200',
      ghost: 'text-slate-600 hover:bg-slate-100 hover:text-slate-950',
    })[props.variant] ?? 'bg-blue-600 text-white shadow-sm hover:bg-blue-700',
)

const sizeClass = computed(
  () =>
    ({
      sm: 'h-8 px-3 text-xs',
      md: 'h-10 px-4 text-xs',
      lg: 'h-11 px-5 text-sm',
    })[props.size] ?? 'h-10 px-4 text-xs',
)
</script>
