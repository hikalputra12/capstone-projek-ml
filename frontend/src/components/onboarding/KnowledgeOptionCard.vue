<template>
  <button
    type="button"
    :disabled="disabled"
    class="group h-full min-h-[190px] w-full rounded-2xl border bg-white p-6 text-left shadow-sm transition duration-200 focus:outline-none focus:ring-2 focus:ring-blue-200 focus:ring-offset-2"
    :class="
      selected
        ? 'border-blue-500 bg-blue-50 ring-2 ring-blue-100'
        : 'border-slate-200 hover:-translate-y-1 hover:border-blue-400 hover:bg-blue-50 hover:shadow-[0_18px_42px_rgba(37,99,235,0.14)]'
    "
  >
    <IconBox v-if="typeof icon !== 'string'" :icon="icon" color="blue" size="lg" class="mb-5 transition group-hover:scale-105" />
    <div
      v-else
      class="mb-5 flex h-14 w-14 items-center justify-center rounded-2xl bg-gradient-to-br from-blue-100 to-violet-100 text-sm font-black text-blue-700 transition group-hover:scale-105"
    >
      {{ icon }}
    </div>

    <h3 class="mb-2 text-lg font-bold text-slate-950">{{ title }}</h3>
    <p class="text-sm leading-6 text-slate-600">{{ description }}</p>
  </button>
</template>

<script setup>
import IconBox from '@/components/common/IconBox.vue'

defineProps({
  icon: {
    type: [String, Object, Function],
    default: 'OK',
  },
  title: {
    type: String,
    required: true,
  },
  description: {
    type: String,
    default: '',
  },
  selected: {
    type: Boolean,
    default: false,
  },
  disabled: {
    type: Boolean,
    default: false,
  },
})
</script>
