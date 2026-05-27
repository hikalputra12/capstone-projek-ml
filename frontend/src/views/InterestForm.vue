<template>
  <main class="min-h-screen bg-slate-50 px-5 py-8 text-slate-950 sm:px-6 lg:py-10">
    <section class="mx-auto max-w-5xl">
      <RouterLink to="/" class="mb-8 inline-flex items-center gap-3">
        <span class="grid h-10 w-10 place-items-center rounded-2xl bg-gradient-to-br from-blue-600 to-violet-600 text-sm font-black text-white shadow-sm">
          BP
        </span>
        <span class="text-lg font-black tracking-tight text-slate-950">Brainpath</span>
      </RouterLink>

      <StepProgress :current="3" :labels="steps" />

      <BaseCard padding="lg" class="mt-8">
        <div class="flex flex-col gap-5 lg:flex-row lg:items-end lg:justify-between">
          <div>
            <p class="text-sm font-black uppercase tracking-wide text-blue-600">Langkah 3</p>
            <h1 class="mt-3 text-3xl font-black tracking-tight text-slate-950 sm:text-4xl">
              Cari Tahu Minat Belajarmu
            </h1>
            <p class="mt-4 max-w-2xl text-sm font-medium leading-6 text-slate-500 sm:text-base">
              Jawab beberapa pertanyaan sederhana agar Brainpath dapat memberikan rekomendasi
              kursus yang lebih sesuai.
            </p>
          </div>

          <div class="rounded-2xl bg-blue-50 px-4 py-3 text-sm font-bold text-slate-600">
            Terjawab: <span class="text-blue-700">{{ answeredCount }}/{{ questions.length }}</span>
          </div>
        </div>

        <form class="mt-8 space-y-8" @submit.prevent="goToRecommendation">
          <div class="space-y-5">
            <BaseCard
              v-for="(question, index) in questions"
              :key="question.id"
              padding="md"
              class="bg-slate-50"
            >
              <div class="flex flex-col gap-4 lg:flex-row lg:items-start">
                <div class="flex min-w-0 flex-1 gap-3">
                  <span class="grid h-8 w-8 shrink-0 place-items-center rounded-xl bg-blue-600 text-xs font-black text-white">
                    {{ index + 1 }}
                  </span>
                  <div>
                    <h2 class="text-base font-black text-slate-950">{{ question.title }}</h2>
                    <p class="mt-1 text-xs leading-5 text-slate-500">
                      Pilih jawaban yang paling mendekati aktivitas yang kamu sukai.
                    </p>
                  </div>
                </div>

                <div class="grid gap-3 sm:grid-cols-2 lg:w-[560px]">
                  <button
                    v-for="option in question.options"
                    :key="option.value"
                    type="button"
                    class="rounded-2xl border bg-white p-4 text-left text-sm font-bold leading-5 shadow-sm transition hover:-translate-y-0.5 hover:border-blue-300 hover:bg-blue-50"
                    :class="
                      answers[question.id] === option.value
                        ? 'border-blue-500 bg-blue-50 text-blue-700 ring-2 ring-blue-100'
                        : 'border-slate-200 text-slate-700'
                    "
                    @click="answers[question.id] = option.value"
                  >
                    <span class="flex items-center gap-3">
                      <IconBox :icon="option.icon" :color="option.color" size="sm" />
                      <span>{{ option.label }}</span>
                    </span>
                  </button>
                </div>
              </div>
            </BaseCard>
          </div>

          <div class="grid gap-5 lg:grid-cols-2">
            <div>
              <label for="learning-goal" class="mb-2 block text-sm font-black text-slate-950">
                Tujuan belajar
              </label>
              <select
                id="learning-goal"
                v-model="learningGoal"
                class="h-12 w-full rounded-xl border border-slate-200 bg-white px-4 text-sm font-medium text-slate-800 shadow-sm outline-none transition focus:border-blue-500 focus:ring-4 focus:ring-blue-100"
              >
                <option v-for="goal in goals" :key="goal" :value="goal">{{ goal }}</option>
              </select>
            </div>

            <div>
              <label for="learning-note" class="mb-2 block text-sm font-black text-slate-950">
                Ceritakan tujuan belajarmu
                <span class="font-semibold text-slate-400">(opsional)</span>
              </label>
              <textarea
                id="learning-note"
                v-model="learningNote"
                rows="4"
                class="w-full resize-none rounded-xl border border-slate-200 bg-white px-4 py-3 text-sm font-medium text-slate-800 shadow-sm outline-none transition placeholder:text-slate-400 focus:border-blue-500 focus:ring-4 focus:ring-blue-100"
                placeholder="Contoh: Saya ingin belajar web agar bisa membuat portofolio pribadi."
              />
            </div>
          </div>

          <BaseButton type="submit" full-width size="lg">
            Lihat Rekomendasi
          </BaseButton>
        </form>
      </BaseCard>
    </section>
  </main>
</template>

<script setup>
import { computed, ref } from 'vue'
import { useRouter } from 'vue-router'
import BaseButton from '@/components/common/BaseButton.vue'
import BaseCard from '@/components/common/BaseCard.vue'
import IconBox from '@/components/common/IconBox.vue'
import StepProgress from '@/components/common/StepProgress.vue'
import { BarChart3, Bot, Monitor, Palette, Puzzle } from 'lucide-vue-next'

const router = useRouter()
const steps = ['Pemahaman IT', 'Reframing', 'Minat', 'Rekomendasi']

const questions = [
  {
    id: 'project_part',
    title: 'Saat membuat sebuah proyek digital, bagian mana yang paling menarik untukmu?',
    options: [
      { label: 'Membuat tampilan yang menarik', value: 'frontend', icon: Palette, color: 'purple' },
      { label: 'Mengatur sistem di balik aplikasi', value: 'backend', icon: Puzzle, color: 'blue' },
      { label: 'Membaca data dan menemukan pola', value: 'data', icon: BarChart3, color: 'blue' },
      { label: 'Membuat fitur pintar berbasis AI', value: 'ai', icon: Bot, color: 'slate' },
    ],
  },
  {
    id: 'learning_activity',
    title: 'Kamu lebih nyaman belajar dengan aktivitas seperti apa?',
    options: [
      { label: 'Mendesain halaman atau layout', value: 'frontend', icon: Palette, color: 'purple' },
      { label: 'Menyusun alur logika', value: 'backend', icon: Puzzle, color: 'blue' },
      { label: 'Menganalisis angka atau data', value: 'data', icon: BarChart3, color: 'blue' },
      { label: 'Mencoba eksperimen teknologi baru', value: 'ai', icon: Bot, color: 'slate' },
    ],
  },
  {
    id: 'curiosity',
    title: 'Jika melihat sebuah aplikasi, hal apa yang paling membuatmu penasaran?',
    options: [
      { label: 'Bagaimana tampilannya dibuat', value: 'frontend', icon: Monitor, color: 'purple' },
      { label: 'Bagaimana data disimpan dan diproses', value: 'backend', icon: Puzzle, color: 'blue' },
      { label: 'Bagaimana data pengguna dianalisis', value: 'data', icon: BarChart3, color: 'blue' },
      { label: 'Bagaimana aplikasi bisa memberi rekomendasi', value: 'ai', icon: Bot, color: 'slate' },
    ],
  },
  {
    id: 'final_output',
    title: 'Hasil akhir seperti apa yang ingin kamu buat?',
    options: [
      { label: 'Website atau tampilan aplikasi', value: 'frontend', icon: Monitor, color: 'purple' },
      { label: 'Sistem login, API, atau database', value: 'backend', icon: Puzzle, color: 'blue' },
      { label: 'Dashboard data atau laporan analitik', value: 'data', icon: BarChart3, color: 'blue' },
      { label: 'Chatbot atau sistem rekomendasi', value: 'ai', icon: Bot, color: 'slate' },
    ],
  },
]

const goals = [
  'Mencari pekerjaan IT',
  'Membangun project pribadi',
  'Upgrade skill',
  'Sekadar penasaran',
]

const answers = ref({})
const learningGoal = ref(goals[0])
const learningNote = ref('')

const answeredCount = computed(() => Object.keys(answers.value).length)

const goToRecommendation = () => {
  router.push('/recommendation')
}
</script>
