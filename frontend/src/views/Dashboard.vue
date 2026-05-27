<template>
  <main class="flex min-h-screen bg-slate-50 text-slate-950">
    <AppSidebar />

    <section class="flex-1 px-5 py-5 md:px-6">
      <div class="mx-auto max-w-6xl">
        <div class="mb-5 flex flex-col gap-2 lg:flex-row lg:items-end lg:justify-between">
          <div>
            <p class="text-xs font-black uppercase tracking-wide text-blue-600">Dashboard</p>
            <h1 class="mt-1 text-2xl font-black tracking-tight text-slate-950">Halo, User!</h1>
            <p class="mt-1.5 max-w-2xl text-sm leading-6 text-slate-500">
              Temukan resource belajar IT terbaik berdasarkan minatmu dan mulai onboarding baru saat minat belajarmu berubah.
            </p>
          </div>
        </div>

        <div class="mb-5 grid gap-4 md:grid-cols-3">
          <BaseCard
            v-for="summary in summaries"
            :key="summary.title"
            padding="sm"
            class="min-h-[104px] rounded-2xl"
          >
            <div class="flex h-full items-center justify-between gap-4">
              <div class="min-w-0">
                <p class="text-sm font-medium text-slate-600">{{ summary.title }}</p>
                <p class="mt-1.5 truncate text-2xl font-black tracking-tight text-slate-950">{{ summary.value }}</p>
              </div>
              <span
                class="grid h-11 w-11 shrink-0 place-items-center rounded-2xl text-white shadow-sm"
                :class="summary.iconClass"
              >
                <component :is="summary.icon" class="h-5 w-5" />
              </span>
            </div>
          </BaseCard>
        </div>

        <BaseCard padding="none" class="mb-6 overflow-hidden rounded-2xl border-0 bg-gradient-to-r from-blue-500 to-violet-600 text-white shadow-sm">
          <div class="flex flex-col gap-5 px-6 py-6 lg:flex-row lg:items-center lg:justify-between">
            <div class="max-w-xl">
              <p class="text-sm font-medium text-blue-50">Mulai Cari Rekomendasi</p>
              <h2 class="mt-1.5 text-2xl font-black tracking-tight">Belum tahu mau belajar apa?</h2>
              <p class="mt-2 text-sm font-medium leading-6 text-blue-50">
                Isi form minat belajar singkat. AI Brainpath akan menyarankan resource paling relevan.
              </p>
            </div>

            <RouterLink
              to="/onboarding"
              class="inline-flex h-10 w-full items-center justify-center gap-2 rounded-xl bg-white/90 px-5 text-sm font-black text-slate-950 shadow-sm transition hover:bg-white sm:w-auto"
            >
              <Sparkles class="h-4 w-4 text-slate-700" />
              Isi Minat Belajar
            </RouterLink>
          </div>
        </BaseCard>

        <section>
          <div class="mb-3 flex flex-col gap-2 sm:flex-row sm:items-end sm:justify-between">
            <div>
              <h2 class="text-lg font-black text-slate-950">Rekomendasi Terakhir</h2>
              <p class="mt-1 text-sm text-slate-500">
                Dummy resource untuk tampilan awal sebelum integrasi API.
              </p>
            </div>
            <RouterLink to="/recommendation" class="text-sm font-black text-blue-600 hover:text-violet-600">
              Lihat semua
            </RouterLink>
          </div>

          <div class="grid gap-4 lg:grid-cols-3">
            <BaseCard
              v-for="resource in recentRecommendations"
              :key="resource.title"
              interactive
              padding="sm"
              class="flex min-h-[178px] flex-col rounded-2xl"
            >
              <div class="flex items-start justify-between gap-4">
                <span
                  class="grid h-10 w-10 shrink-0 place-items-center rounded-xl text-xs font-black"
                  :class="resource.accent"
                >
                  {{ resource.initial }}
                </span>
                <span class="rounded-full bg-blue-50 px-3 py-1 text-xs font-black text-blue-700">
                  Match {{ resource.match }}%
                </span>
              </div>
              <h3 class="mt-3 text-base font-black text-slate-950">{{ resource.title }}</h3>
              <p class="mt-2 flex-1 text-sm leading-6 text-slate-500">{{ resource.description }}</p>
              <div class="mt-4 flex items-center justify-between gap-4">
                <span class="text-xs font-bold text-slate-400">{{ resource.platform }}</span>
                <RouterLink
                  :to="`/resources/${resource.id}`"
                  class="text-sm font-black text-blue-600 hover:text-violet-600"
                >
                  Preview
                </RouterLink>
              </div>
            </BaseCard>
          </div>
        </section>
      </div>
    </section>
  </main>
</template>

<script setup>
import AppSidebar from '@/components/layout/AppSidebar.vue'
import BaseCard from '@/components/common/BaseCard.vue'
import { ExternalLink, Layers, Sparkles, Tag } from 'lucide-vue-next'

const summaries = [
  {
    title: 'Total Rekomendasi',
    value: '6',
    icon: Layers,
    iconClass: 'bg-blue-600',
  },
  {
    title: 'Kategori Terakhir',
    value: 'Frontend',
    icon: Tag,
    iconClass: 'bg-violet-600',
  },
  {
    title: 'Resource Terakhir Dibuka',
    value: 'HTML & CSS Dasar',
    icon: ExternalLink,
    iconClass: 'bg-slate-700',
  },
]

const recentRecommendations = [
  {
    id: 1,
    title: 'Responsive Web Design',
    platform: 'freeCodeCamp',
    initial: 'FCC',
    match: 96,
    accent: 'bg-blue-100 text-blue-700',
    description: 'Latihan HTML dan CSS dasar untuk membangun halaman web responsif.',
  },
  {
    id: 2,
    title: 'Learn Web Development',
    platform: 'MDN',
    initial: 'MDN',
    match: 91,
    accent: 'bg-violet-100 text-violet-700',
    description: 'Panduan konsep web fundamental dari dokumentasi Mozilla Developer Network.',
  },
  {
    id: 3,
    title: 'Frontend Developer Roadmap',
    platform: 'roadmap.sh',
    initial: 'MAP',
    match: 86,
    accent: 'bg-slate-100 text-slate-700',
    description: 'Urutan topik belajar frontend agar perjalanan belajar lebih terarah.',
  },
]
</script>
