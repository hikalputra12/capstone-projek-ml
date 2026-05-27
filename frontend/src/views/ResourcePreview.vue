<template>
  <main class="min-h-screen bg-slate-50 px-5 py-8 text-slate-950 sm:px-6 lg:py-10">
    <section class="mx-auto max-w-6xl">
      <nav class="mb-6 flex flex-wrap items-center gap-2 text-sm font-bold text-slate-500">
        <RouterLink to="/dashboard" class="hover:text-blue-700">Dashboard</RouterLink>
        <span>/</span>
        <RouterLink to="/recommendation" class="hover:text-blue-700">Rekomendasi</RouterLink>
        <span>/</span>
        <span class="text-slate-950">{{ resource.title }}</span>
      </nav>

      <BaseCard padding="lg" class="mb-6">
        <div class="flex flex-col gap-5 lg:flex-row lg:items-start lg:justify-between">
          <div>
            <p class="text-sm font-black uppercase tracking-wide text-blue-600">Resource Preview</p>
            <h1 class="mt-3 text-3xl font-black tracking-tight text-slate-950 sm:text-4xl">
              {{ resource.title }}
            </h1>

            <div class="mt-5 flex flex-wrap gap-2">
              <span
                v-for="meta in metadata"
                :key="meta"
                class="rounded-full bg-slate-100 px-3 py-1 text-xs font-black text-slate-600"
              >
                {{ meta }}
              </span>
            </div>
          </div>

          <div class="flex w-full flex-col gap-3 sm:w-auto sm:flex-row lg:pt-2">
            <BaseButton :href="resource.externalUrl" external>
              <ExternalLink class="h-4 w-4" />
              Buka Sumber
            </BaseButton>
            <BaseButton to="/recommendation" variant="secondary">
              <ArrowLeft class="h-4 w-4" />
              Kembali ke Rekomendasi
            </BaseButton>
          </div>
        </div>
      </BaseCard>

      <div class="grid gap-6 lg:grid-cols-[1.25fr_0.75fr]">
        <div class="space-y-6">
          <VideoPreview :title="resource.title" :source="resource.source" />

          <BaseCard padding="lg">
            <h2 class="flex items-center gap-3 text-xl font-black text-slate-950">
              <Info class="h-5 w-5 text-blue-700" />
              About This Topic
            </h2>
            <p class="mt-3 text-sm leading-7 text-slate-600">{{ resource.description }}</p>
          </BaseCard>

          <BaseCard padding="lg">
            <h2 class="flex items-center gap-3 text-xl font-black text-slate-950">
              <ListChecks class="h-5 w-5 text-blue-700" />
              Apa yang Akan Dibahas?
            </h2>
            <div class="mt-4 grid gap-3 sm:grid-cols-2">
              <div
                v-for="topic in discussedTopics"
                :key="topic"
                class="rounded-2xl bg-slate-50 p-4 text-sm font-bold text-slate-700 ring-1 ring-slate-100"
              >
                {{ topic }}
              </div>
            </div>
          </BaseCard>

          <AISummarySection :summary="resource.aiSummary" />
        </div>

        <aside class="space-y-6">
          <BaseCard padding="lg">
            <h2 class="flex items-center gap-3 text-xl font-black text-slate-950">
              <Users class="h-5 w-5 text-blue-700" />
              Untuk Siapa Materi Ini?
            </h2>
            <ul class="mt-4 space-y-3 text-sm leading-6 text-slate-600">
              <li v-for="audience in resource.targetLearners" :key="audience" class="rounded-2xl bg-slate-50 p-4">
                {{ audience }}
              </li>
            </ul>
          </BaseCard>

          <BaseCard padding="lg">
            <h2 class="flex items-center gap-3 text-xl font-black text-slate-950">
              <Map class="h-5 w-5 text-blue-700" />
              Roadmap Isi Video
            </h2>
            <div class="mt-5 space-y-4">
              <div v-for="(item, index) in resource.videoRoadmap" :key="item.title" class="flex gap-3">
                <span class="grid h-8 w-8 shrink-0 place-items-center rounded-full bg-blue-100 text-xs font-black text-blue-700">
                  {{ index + 1 }}
                </span>
                <div>
                  <p class="text-sm font-black text-slate-950">{{ item.title }}</p>
                  <p class="mt-1 text-xs font-bold text-slate-500">{{ item.time }}</p>
                </div>
              </div>
            </div>
          </BaseCard>
        </aside>
      </div>
    </section>
  </main>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import BaseButton from '@/components/common/BaseButton.vue'
import BaseCard from '@/components/common/BaseCard.vue'
import AISummarySection from '@/components/resource/AISummarySection.vue'
import VideoPreview from '@/components/resource/VideoPreview.vue'
import { getResourceById, resources } from '@/data/resources'
import { ArrowLeft, ExternalLink, Info, ListChecks, Map, Users } from 'lucide-vue-next'

const route = useRoute()
const resource = computed(() => getResourceById(route.params.id) ?? resources[0])

const metadata = computed(() => [
  resource.value.source,
  resource.value.category,
  resource.value.level,
  resource.value.duration,
])

const discussedTopics = computed(() => resource.value.learningPoints)
</script>
