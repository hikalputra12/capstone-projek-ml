<template>
  <header class="relative z-10 mx-auto mb-8 flex w-full max-w-5xl flex-col items-center gap-8 lg:mb-10">
    <RouterLink to="/" class="flex items-center gap-2">
      <span
        class="grid h-9 w-9 place-items-center rounded-full bg-gradient-to-br from-blue-500 to-violet-600 text-white shadow-[0_10px_24px_rgba(93,111,243,0.24)] ring-4 ring-white"
        aria-hidden="true"
      >
        <svg class="h-5 w-5" viewBox="0 0 24 24" fill="none">
          <path
            d="M9.5 4.75a3.25 3.25 0 0 0-3.21 2.76 3.63 3.63 0 0 0-.54 7.1 3.75 3.75 0 0 0 7.25 1.26V7.75a3 3 0 0 0-3.5-3Z"
            stroke="currentColor"
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="1.8"
          />
          <path
            d="M14.5 4.75a3.25 3.25 0 0 1 3.21 2.76 3.63 3.63 0 0 1 .54 7.1A3.75 3.75 0 0 1 11 15.87V7.75a3 3 0 0 1 3.5-3Z"
            stroke="currentColor"
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="1.8"
          />
        </svg>
      </span>
      <span class="text-base font-extrabold tracking-tight text-blue-700">Brainpath</span>
    </RouterLink>

    <StepProgress :current="current" />
  </header>
</template>

<script setup>
import StepProgress from '@/components/common/StepProgress.vue'

defineProps({
  current: {
    type: Number,
    required: true,
  },
})
</script>
