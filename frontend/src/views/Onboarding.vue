<template>
  <main class="min-h-screen bg-slate-50 px-5 py-8 text-slate-950 sm:px-6 lg:py-10">
    <section class="mx-auto max-w-5xl">
      <RouterLink to="/" class="mb-8 inline-flex items-center gap-3">
        <span class="grid h-10 w-10 place-items-center rounded-2xl bg-gradient-to-br from-blue-600 to-violet-600 text-sm font-black text-white shadow-sm">
          BP
        </span>
        <span class="text-lg font-black tracking-tight text-slate-950">Brainpath</span>
      </RouterLink>

      <StepProgress :current="1" :labels="steps" />

      <BaseCard padding="lg" class="mt-8 text-center">
        <p class="text-sm font-black uppercase tracking-wide text-blue-600">Langkah 1</p>
        <h1 class="mx-auto mt-3 max-w-3xl text-3xl font-black tracking-tight text-slate-950 sm:text-4xl">
          Apakah kamu sudah memahami dunia IT?
        </h1>
        <p class="mx-auto mt-4 max-w-2xl text-sm font-medium leading-6 text-slate-500 sm:text-base">
          Jawaban ini membantu Brainpath menentukan apakah kamu perlu pengenalan bidang IT dulu
          atau bisa langsung memilih minat belajar.
        </p>

        <div class="mt-9 grid gap-5 md:grid-cols-2">
          <RouterLink to="/interest-form" class="block">
            <KnowledgeOptionCard
              :icon="CheckCircle"
              title="Sudah Paham"
              description="Saya sudah familiar dengan dunia IT dan ingin langsung memilih minat."
            />
          </RouterLink>

          <RouterLink to="/reframing" class="block">
            <KnowledgeOptionCard
              :icon="HelpCircle"
              title="Belum Paham"
              description="Saya ingin melihat gambaran singkat bidang-bidang IT terlebih dahulu."
            />
          </RouterLink>
        </div>
      </BaseCard>
    </section>
  </main>
</template>

<script setup>
import BaseCard from '@/components/common/BaseCard.vue'
import StepProgress from '@/components/common/StepProgress.vue'
import KnowledgeOptionCard from '@/components/onboarding/KnowledgeOptionCard.vue'
import { CheckCircle, HelpCircle } from 'lucide-vue-next'

const steps = ['Pemahaman IT', 'Reframing', 'Minat', 'Rekomendasi']
</script>
