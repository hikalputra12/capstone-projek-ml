<template>
  <main class="flex min-h-screen bg-slate-50 text-slate-950">
    <AppSidebar />

    <section class="flex-1 px-5 py-6 md:px-8">
      <div class="mb-6 flex flex-col gap-4 lg:flex-row lg:items-end lg:justify-between">
        <div>
          <p class="text-sm font-black uppercase tracking-wide text-blue-600">AI Course Recommender</p>
          <div class="mt-2 flex items-center gap-3">
            <span class="grid h-11 w-11 place-items-center rounded-2xl bg-blue-100 text-blue-700">
              <Sparkles class="h-5 w-5" />
            </span>
            <h1 class="text-3xl font-black tracking-tight text-slate-950">
              Rekomendasi Kursus Untukmu
            </h1>
          </div>
          <p class="mt-2 max-w-2xl text-sm leading-6 text-slate-500">
            Berdasarkan minat dan jawaban onboarding kamu
          </p>
        </div>

        <BaseButton to="/onboarding">
          Ulangi Onboarding
        </BaseButton>
      </div>

      <RecommendationFilter
        v-model:active-category="activeCategory"
        v-model:sort-by="sortBy"
        :categories="categories"
        :sort-options="sortOptions"
        class="mb-6"
      />

      <div class="mb-4 flex items-center justify-between gap-4">
        <p class="text-sm font-bold text-slate-500">
          Menampilkan {{ sortedResources.length }} resource eksternal
        </p>
        <p class="text-sm font-bold text-slate-500">
          Filter: <span class="text-blue-700">{{ activeCategory }}</span>
        </p>
      </div>

      <div class="grid gap-4 xl:grid-cols-2">
        <RecommendationCard
          v-for="resource in sortedResources"
          :key="resource.id"
          :resource="resource"
        />
      </div>
    </section>
  </main>
</template>

<script setup>
import { computed, ref } from 'vue'
import AppSidebar from '@/components/layout/AppSidebar.vue'
import BaseButton from '@/components/common/BaseButton.vue'
import RecommendationCard from '@/components/recommendation/RecommendationCard.vue'
import RecommendationFilter from '@/components/recommendation/RecommendationFilter.vue'
import { resources } from '@/data/resources'
import { Sparkles } from 'lucide-vue-next'

const categories = ['Semua', 'Frontend', 'Backend', 'Data', 'AI', 'General IT']
const sortOptions = [
  { label: 'Paling Relevan', value: 'relevance' },
  { label: 'Pemula', value: 'beginner' },
  { label: 'Durasi Singkat', value: 'short' },
]

const activeCategory = ref('Semua')
const sortBy = ref('relevance')

const filteredResources = computed(() => {
  if (activeCategory.value === 'Semua') return resources
  return resources.filter((resource) => resource.category === activeCategory.value)
})

const sortedResources = computed(() => {
  const items = [...filteredResources.value]

  if (sortBy.value === 'beginner') {
    return items.sort((a, b) => {
      if (a.level === b.level) return b.relevanceScore - a.relevanceScore
      return a.level === 'Pemula' ? -1 : 1
    })
  }

  if (sortBy.value === 'short') {
    return items.sort((a, b) => parseDuration(a.duration) - parseDuration(b.duration))
  }

  return items.sort((a, b) => b.relevanceScore - a.relevanceScore)
})

const parseDuration = (duration) => {
  const hourMatch = duration.match(/(\d+)\s*jam/)
  const minuteMatch = duration.match(/(\d+)\s*menit/)
  const hours = hourMatch ? Number(hourMatch[1]) : 0
  const minutes = minuteMatch ? Number(minuteMatch[1]) : 0

  return hours * 60 + minutes
}
</script>
