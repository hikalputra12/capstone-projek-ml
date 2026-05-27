<template>
  <button
    type="button"
    :disabled="disabled"
    class="group flex min-h-[142px] w-full flex-col justify-between rounded-2xl border bg-white px-5 py-5 text-left shadow-sm transition duration-200 focus:outline-none focus:ring-2 focus:ring-blue-200 focus:ring-offset-2"
    :class="
      selected
        ? 'border-blue-500 bg-blue-50 ring-2 ring-blue-100'
        : 'border-slate-200 hover:-translate-y-1 hover:border-blue-300 hover:shadow-[0_18px_42px_rgba(37,99,235,0.12)]'
    "
  >
    <span
      class="grid h-11 w-11 place-items-center rounded-2xl text-sm font-black transition group-hover:scale-105"
      :class="accent"
    >
      {{ icon || initial }}
    </span>

    <span class="mt-5 block text-sm font-black leading-5 text-slate-950">{{ label }}</span>
    <p v-if="description" class="mt-2 text-xs leading-5 text-slate-500">{{ description }}</p>
  </button>
</template>

<script setup>
defineProps({
  icon: {
    type: String,
    default: '',
  },
  initial: {
    type: String,
    default: '',
  },
  label: {
    type: String,
    required: true,
  },
  description: {
    type: String,
    default: '',
  },
  accent: {
    type: String,
    default: 'bg-blue-100 text-blue-700',
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
