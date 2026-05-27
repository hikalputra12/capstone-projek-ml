<template>
  <BaseCard padding="none" class="overflow-hidden">
    <div class="relative aspect-video bg-slate-950">
      <div
        class="absolute inset-0 bg-gradient-to-br from-blue-600 via-violet-600 to-slate-950 opacity-90"
        aria-hidden="true"
      />
      <div class="absolute inset-0 flex flex-col items-center justify-center px-6 text-center text-white">
        <span class="grid h-16 w-16 place-items-center rounded-full bg-white/20 text-2xl font-black shadow-lg ring-1 ring-white/30">
          ▶
        </span>
        <p class="mt-5 text-sm font-black uppercase tracking-wide text-blue-100">{{ source }}</p>
        <h2 class="mt-2 max-w-2xl text-2xl font-black">{{ title }}</h2>
        <p class="mt-2 text-sm font-medium text-white/80">Preview video eksternal sebelum membuka sumber asli.</p>
      </div>
    </div>
  </BaseCard>
</template>

<script setup>
import BaseCard from '@/components/common/BaseCard.vue'

defineProps({
  title: {
    type: String,
    required: true,
  },
  source: {
    type: String,
    default: 'YouTube',
  },
})
</script>
