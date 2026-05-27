<template>
  <main class="min-h-screen bg-slate-50 px-5 py-8 text-slate-950 sm:px-6 lg:py-10">
    <section class="mx-auto max-w-6xl">
      <RouterLink to="/" class="mb-8 inline-flex items-center gap-3">
        <span class="grid h-10 w-10 place-items-center rounded-2xl bg-gradient-to-br from-blue-600 to-violet-600 text-sm font-black text-white shadow-sm">
          BP
        </span>
        <span class="text-lg font-black tracking-tight text-slate-950">Brainpath</span>
      </RouterLink>

      <StepProgress :current="2" :labels="steps" />

      <div class="mt-8 rounded-3xl border border-slate-200 bg-white p-5 shadow-sm sm:p-6">
        <div class="mx-auto mb-8 max-w-3xl text-center">
          <p class="text-xs font-black uppercase tracking-wide text-blue-600">Langkah 2</p>
          <h1 class="mt-3 text-3xl font-black tracking-tight text-slate-950 sm:text-4xl">
            Yuk, Kenali Dunia IT Lebih Dulu
          </h1>
          <p class="mt-4 text-sm font-medium leading-7 text-slate-500 sm:text-base">
            Dunia IT bukan hanya tentang mengetik kode. Ada banyak bidang yang bisa kamu pilih
            sesuai cara berpikir, minat, dan aktivitas yang kamu sukai.
          </p>
        </div>

        <div class="grid gap-4 lg:grid-cols-2">
          <BaseCard
            v-for="field in fields"
            :key="field.title"
            interactive
            padding="lg"
            class="h-full"
          >
            <div class="flex items-start gap-4">
              <IconBox :icon="field.icon" :color="field.iconColor" size="lg" />
              <div>
                <h2 class="text-lg font-black text-slate-950">{{ field.title }}</h2>
                <p class="mt-2 text-sm leading-6 text-slate-600">{{ field.description }}</p>
              </div>
            </div>

            <div class="mt-5 grid gap-4 sm:grid-cols-2">
              <div>
                <h3 class="text-xs font-black uppercase tracking-wide text-blue-600">
                  Cocok untuk kamu jika
                </h3>
                <ul class="mt-3 space-y-2 text-sm leading-6 text-slate-600">
                  <li v-for="item in field.suitableFor" :key="item" class="flex gap-2">
                    <span class="mt-2 h-1.5 w-1.5 shrink-0 rounded-full bg-blue-500" />
                    <span>{{ item }}</span>
                  </li>
                </ul>
              </div>

              <div class="space-y-4">
                <div>
                  <h3 class="text-xs font-black uppercase tracking-wide text-violet-600">
                    Contoh yang dipelajari
                  </h3>
                  <p class="mt-2 text-sm leading-6 text-slate-600">{{ field.learningExamples }}</p>
                </div>
                <div>
                  <h3 class="text-xs font-black uppercase tracking-wide text-violet-600">
                    Contoh hasil kerja
                  </h3>
                  <p class="mt-2 text-sm leading-6 text-slate-600">{{ field.workExamples }}</p>
                </div>
              </div>
            </div>
          </BaseCard>
        </div>

        <BaseCard padding="lg" class="mt-6 bg-gradient-to-br from-blue-50 to-violet-50">
          <div class="flex flex-col gap-4 lg:flex-row lg:items-center lg:justify-between">
            <div class="max-w-3xl">
              <h2 class="text-xl font-black text-slate-950">Masih bingung menentukan minat?</h2>
              <p class="mt-2 text-sm leading-6 text-slate-600">
                Tidak perlu langsung memilih bidang IT sekarang. Kamu bisa mulai dari aktivitas
                yang paling kamu sukai, lalu Brainpath akan membantu mencocokkannya dengan
                rekomendasi kursus yang sesuai.
              </p>
            </div>

            <BaseButton to="/interest-form" size="lg" class="shrink-0">
              Lanjut ke Kuis Minat
            </BaseButton>
          </div>
        </BaseCard>
      </div>
    </section>
  </main>
</template>

<script setup>
import BaseButton from '@/components/common/BaseButton.vue'
import BaseCard from '@/components/common/BaseCard.vue'
import IconBox from '@/components/common/IconBox.vue'
import StepProgress from '@/components/common/StepProgress.vue'
import { BarChart3, Brain, Monitor, Server } from 'lucide-vue-next'

const steps = ['Pemahaman IT', 'Reframing', 'Minat', 'Rekomendasi']

const fields = [
  {
    title: 'Frontend Development',
    icon: Monitor,
    iconColor: 'blue',
    description:
      'Bidang yang berfokus pada tampilan dan pengalaman pengguna dalam website atau aplikasi.',
    suitableFor: [
      'Suka desain visual',
      'Tertarik membuat tampilan website',
      'Suka memperhatikan warna, layout, dan interaksi pengguna',
    ],
    learningExamples: 'HTML, CSS, JavaScript, Vue.js',
    workExamples: 'Landing page, dashboard aplikasi, tampilan website',
  },
  {
    title: 'Backend Development',
    icon: Server,
    iconColor: 'purple',
    description:
      'Bidang yang berfokus pada sistem di balik aplikasi, seperti server, database, autentikasi, dan proses pengolahan data.',
    suitableFor: [
      'Suka logika dan struktur sistem',
      'Tertarik memahami cara kerja aplikasi di balik layar',
      'Suka mengatur data dan alur proses',
    ],
    learningExamples: 'PHP, Laravel, API, Database',
    workExamples: 'REST API, login system, manajemen data aplikasi',
  },
  {
    title: 'Data Analysis',
    icon: BarChart3,
    iconColor: 'blue',
    description:
      'Bidang yang berfokus pada pengolahan data untuk menemukan pola, insight, dan informasi yang berguna.',
    suitableFor: [
      'Suka membaca pola dari data',
      'Tertarik membuat grafik atau laporan',
      'Suka mengambil keputusan berdasarkan angka',
    ],
    learningExamples: 'SQL, Python, Pandas, visualisasi data',
    workExamples: 'Dashboard laporan, analisis tren, insight pengguna',
  },
  {
    title: 'AI / Machine Learning',
    icon: Brain,
    iconColor: 'slate',
    description:
      'Bidang yang berfokus pada pembuatan sistem cerdas yang dapat memberikan prediksi, rekomendasi, atau memahami pola dari data.',
    suitableFor: [
      'Tertarik dengan sistem pintar',
      'Suka eksperimen dengan data',
      'Penasaran dengan chatbot, rekomendasi, dan prediksi',
    ],
    learningExamples: 'Python, Machine Learning, NLP, Recommendation System',
    workExamples: 'Sistem rekomendasi, chatbot, prediksi data',
  },
]
</script>
