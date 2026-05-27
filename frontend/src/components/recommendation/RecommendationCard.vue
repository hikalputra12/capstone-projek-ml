<template>
  <BaseCard interactive padding="md">
    <div class="flex flex-col gap-5">
      <div class="flex items-start justify-between gap-4">
        <div>
          <p class="flex items-center gap-2 text-sm font-black text-blue-600">
            <Video class="h-4 w-4" />
            {{ resource.source }}
          </p>
          <h2 class="mt-2 text-xl font-black text-slate-950">{{ resource.title }}</h2>
        </div>
        <span class="inline-flex items-center gap-1.5 rounded-full bg-blue-50 px-3 py-1 text-xs font-black text-blue-700">
          <Sparkles class="h-3.5 w-3.5" />
          {{ resource.relevanceScore }}% match
        </span>
      </div>

      <div class="flex flex-wrap gap-2">
        <span class="inline-flex items-center gap-1.5 rounded-full bg-slate-100 px-3 py-1 text-xs font-bold text-slate-600">
          <Tag class="h-3.5 w-3.5" />
          {{ resource.category }}
        </span>
        <span class="inline-flex items-center gap-1.5 rounded-full bg-violet-50 px-3 py-1 text-xs font-bold text-violet-700">
          <Layers class="h-3.5 w-3.5" />
          {{ resource.level }}
        </span>
        <span class="inline-flex items-center gap-1.5 rounded-full bg-slate-100 px-3 py-1 text-xs font-bold text-slate-600">
          <Clock class="h-3.5 w-3.5" />
          {{ resource.duration }}
        </span>
      </div>

      <div class="flex flex-wrap gap-2">
        <span
          v-for="tag in resource.tags"
          :key="tag"
          class="rounded-full bg-white px-3 py-1 text-xs font-bold text-slate-500 ring-1 ring-slate-200"
        >
          {{ tag }}
        </span>
      </div>

      <div class="rounded-2xl bg-slate-50 p-4">
        <p class="text-xs font-black uppercase tracking-wide text-slate-400">Alasan direkomendasikan</p>
        <p class="mt-2 text-sm leading-6 text-slate-600">{{ resource.reason }}</p>
      </div>

      <div class="flex flex-col gap-3 sm:flex-row">
        <BaseButton :to="`/resources/${resource.id}`" variant="secondary" full-width>
          <Eye class="h-4 w-4" />
          Preview Materi
        </BaseButton>
        <BaseButton :href="resource.externalUrl" external full-width>
          <ExternalLink class="h-4 w-4" />
          Buka Link
        </BaseButton>
      </div>
    </div>
  </BaseCard>
</template>

<script setup>
import BaseButton from '@/components/common/BaseButton.vue'
import BaseCard from '@/components/common/BaseCard.vue'
import { Clock, ExternalLink, Eye, Layers, Sparkles, Tag, Video } from 'lucide-vue-next'

defineProps({
  resource: {
    type: Object,
    required: true,
  },
})
</script>
