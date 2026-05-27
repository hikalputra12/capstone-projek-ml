<template>
  <BaseCard padding="lg" class="bg-gradient-to-br from-blue-50 to-violet-50">
    <div class="flex items-center gap-3">
      <span class="grid h-9 w-9 place-items-center rounded-xl bg-blue-100 text-blue-700">
        <Sparkles class="h-4 w-4" />
      </span>
      <p class="text-sm font-black uppercase tracking-wide text-blue-700">Ringkasan AI</p>
    </div>
    <p class="mt-3 text-base font-medium leading-8 text-slate-700">{{ summary }}</p>
  </BaseCard>
</template>

<script setup>
import BaseCard from '@/components/common/BaseCard.vue'
import { Sparkles } from 'lucide-vue-next'

defineProps({
  summary: {
    type: String,
    required: true,
  },
})
</script>
