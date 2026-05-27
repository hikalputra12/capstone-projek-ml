<template>
  <main class="min-h-screen bg-slate-50 text-slate-950">
    <AppNavbar :items="landingNavItems" />

    <section id="home" class="overflow-hidden bg-gradient-to-b from-blue-50/70 via-slate-50 to-white">
      <div class="mx-auto flex min-h-[calc(100vh-4rem)] max-w-6xl flex-col items-center justify-center px-5 py-10 text-center sm:px-6 lg:px-8">
        <p class="inline-flex items-center gap-2 rounded-full border border-slate-200 bg-white px-5 py-2 text-sm font-bold text-slate-700 shadow-sm">
          <span class="text-lg leading-none text-blue-600">✦</span>
          AI-powered course recommendations
        </p>

        <h1 class="mt-10 max-w-6xl text-4xl font-black leading-tight tracking-tight text-slate-950 sm:text-5xl lg:text-6xl">
          Temukan Rekomendasi Kursus IT yang
            <span class="bg-gradient-to-r from-blue-600 to-violet-600 bg-clip-text text-transparent">
              Sesuai Untukmu
            </span>
        </h1>

        <p class="mt-6 max-w-3xl text-base font-medium leading-8 text-slate-600 sm:text-lg">
          Brainpath menggunakan AI untuk merekomendasikan resource belajar IT —
          terutama video YouTube — berdasarkan minat dan jawaban onboarding kamu.
        </p>

        <div class="mt-10 flex flex-col items-center justify-center gap-4 sm:flex-row">
          <RouterLink
            to="/login"
            class="inline-flex h-12 min-w-64 items-center justify-center gap-3 rounded-xl bg-gradient-to-r from-blue-600 to-violet-600 px-8 text-base font-black text-white shadow-lg shadow-blue-200 transition hover:-translate-y-0.5 hover:shadow-blue-300"
          >
            Mulai Rekomendasi
            <span aria-hidden="true">→</span>
          </RouterLink>
        </div>

        <div class="mt-10 flex flex-wrap items-center justify-center gap-x-8 gap-y-3 text-sm font-medium text-slate-600 sm:text-base">
          <p
            v-for="benefit in benefits"
            :key="benefit"
            class="flex items-center gap-2"
          >
            <span class="grid h-5 w-5 place-items-center rounded-full border border-blue-500 text-xs font-black text-blue-600">
              ✓
            </span>
            {{ benefit }}
          </p>
        </div>
      </div>
    </section>

    <section id="features" class="scroll-mt-32 bg-white py-20 sm:py-24">
      <div class="mx-auto max-w-6xl px-5 sm:px-6 lg:px-8">
        <div class="mx-auto mb-10 max-w-3xl text-center">
          <p class="text-sm font-black uppercase tracking-wide text-blue-600">Fitur utama</p>
          <h2 class="mt-3 text-3xl font-black tracking-tight text-slate-950 sm:text-4xl">
            Rekomendasi belajar yang ringkas, personal, dan mudah dimulai.
          </h2>
          <p class="mt-4 text-sm font-medium leading-6 text-slate-500 sm:text-base">
            Brainpath membantu kamu memilih resource eksternal yang relevan tanpa harus bingung
            membandingkan terlalu banyak sumber belajar.
          </p>
        </div>

        <div class="grid gap-6 md:grid-cols-2 lg:grid-cols-4">
          <SummaryCard
            v-for="feature in features"
            :key="feature.title"
            :title="feature.title"
            :description="feature.description"
            :icon="feature.icon"
            :icon-color="feature.iconColor"
            interactive
          />
        </div>
      </div>
    </section>

    <section id="about" class="scroll-mt-32 bg-blue-50 px-5 py-24 sm:px-6 lg:px-8">
      <div class="mx-auto grid max-w-6xl gap-8 lg:grid-cols-[1.05fr_0.95fr] lg:items-center">
        <div>
          <p class="text-sm font-black uppercase tracking-wide text-blue-600">Tentang</p>
          <h2 class="mt-3 text-3xl font-black tracking-tight text-slate-950 sm:text-4xl">
            Tentang Brainpath
          </h2>
          <p class="mt-5 max-w-3xl text-base font-medium leading-8 text-slate-600">
            Brainpath adalah platform rekomendasi kursus IT berbasis AI yang membantu pengguna
            menemukan sumber belajar yang sesuai dengan minat, tingkat pemahaman, dan tujuan belajarnya.
          </p>
          <p class="mt-4 max-w-3xl text-base font-medium leading-8 text-slate-600">
            Melalui proses onboarding dan kuis minat, Brainpath merekomendasikan resource belajar
            eksternal seperti video, artikel, atau course online yang relevan, sehingga pengguna
            dapat memulai belajar dari sumber yang lebih sesuai.
          </p>
        </div>

        <div class="rounded-3xl border border-blue-100 bg-white p-5 shadow-sm">
          <div class="rounded-2xl bg-slate-50 p-5">
            <p class="text-sm font-black uppercase tracking-wide text-blue-700">
              Fokus Brainpath
            </p>
            <div class="mt-5 grid gap-3">
              <div
                v-for="point in aboutPoints"
                :key="point"
                class="flex items-center gap-3 rounded-2xl bg-white px-4 py-3 text-sm font-bold text-slate-700 shadow-sm"
              >
                <span class="grid h-7 w-7 shrink-0 place-items-center rounded-full bg-blue-100 text-xs font-black text-blue-700">
                  ✓
                </span>
                {{ point }}
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <section class="bg-white px-5 py-20 sm:px-6 lg:px-8">
      <div class="mx-auto max-w-6xl rounded-3xl bg-gradient-to-r from-blue-600 to-violet-600 px-6 py-16 text-center text-white shadow-sm sm:px-10">
        <h2 class="text-3xl font-black tracking-tight sm:text-4xl">
          Siap menemukan resource belajar yang tepat?
        </h2>
        <p class="mx-auto mt-5 max-w-2xl text-base font-medium leading-7 text-blue-50">
          Isi onboarding singkat, dan Brainpath akan merekomendasikan video & kursus IT yang paling cocok untukmu.
        </p>
        <RouterLink
          to="/login"
          class="mt-8 inline-flex h-11 items-center justify-center rounded-xl bg-white/90 px-8 text-sm font-black text-slate-950 shadow-sm transition hover:bg-white"
        >
          Mulai Rekomendasi
        </RouterLink>
      </div>
    </section>

    <footer class="border-t border-slate-200 bg-slate-50 px-5 py-8 text-center text-sm text-slate-500">
      © 2026 Brainpath. AI Course Recommender.
    </footer>
  </main>
</template>

<script setup>
import AppNavbar from '@/components/layout/AppNavbar.vue'
import SummaryCard from '@/components/common/SummaryCard.vue'
import { BookOpen, Brain, Target, Video } from 'lucide-vue-next'

const benefits = [
  'Resource gratis dari YouTube',
  'Ringkasan AI per materi',
  'Cocok untuk pemula',
]

const aboutPoints = [
  'Untuk pemula IT',
  'Rekomendasi berbasis minat',
  'Resource eksternal terpercaya',
  'Ringkasan materi dengan AI',
]

const landingNavItems = [
  { label: 'Beranda', to: { path: '/', hash: '#home' } },
  { label: 'Fitur', to: { path: '/', hash: '#features' } },
  { label: 'Tentang', to: { path: '/', hash: '#about' } },
]

const features = [
  {
    icon: Brain,
    iconColor: 'blue',
    title: 'AI Course Recommendation',
    description: 'Rekomendasi resource IT berdasarkan minat, onboarding, dan tujuan belajar.',
  },
  {
    icon: Target,
    iconColor: 'purple',
    title: 'Personalized Suggestions',
    description: 'Saran belajar dibuat lebih relevan untuk level dan preferensi tiap user.',
  },
  {
    icon: BookOpen,
    iconColor: 'blue',
    title: 'Beginner-Friendly Guidance',
    description: 'Alur awal yang ramah untuk pemula agar tidak bingung memilih topik IT.',
  },
  {
    icon: Video,
    iconColor: 'purple',
    title: 'Video Summary Preview',
    description: 'Preview singkat membantu kamu menilai resource sebelum membuka sumber asli.',
  },
]
</script>
