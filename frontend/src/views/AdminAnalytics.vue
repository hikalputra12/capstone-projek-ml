<template>
  <main class="min-h-screen bg-slate-50 text-slate-950">
    <AdminTopNavbar />

    <section class="mx-auto max-w-7xl px-5 py-6 lg:px-8">
      <div class="mb-7">
        <h1 class="text-3xl font-bold tracking-tight text-slate-950">Analytics</h1>
        <p class="mt-2 max-w-2xl text-sm leading-6 text-slate-600">
          Pantau performa resource eksternal dan interaksi rekomendasi pengguna.
        </p>
      </div>

      <div class="grid gap-5 md:grid-cols-3">
        <BaseCard
          v-for="stat in stats"
          :key="stat.title"
          padding="lg"
          class="rounded-3xl"
        >
          <p class="text-sm font-medium text-slate-600">{{ stat.title }}</p>
          <p class="mt-2 text-3xl font-semibold tracking-tight text-slate-950">{{ stat.value }}</p>
          <p class="mt-2 text-xs text-slate-500">{{ stat.description }}</p>
        </BaseCard>
      </div>

      <BaseCard padding="lg" class="mt-6 rounded-3xl">
        <h2 class="text-lg font-semibold text-slate-950">Kategori dengan engagement tertinggi</h2>
        <div class="mt-5 space-y-4">
          <div v-for="item in categories" :key="item.label">
            <div class="mb-2 flex justify-between text-sm">
              <span class="font-medium text-slate-700">{{ item.label }}</span>
              <span class="text-slate-500">{{ item.value }}%</span>
            </div>
            <div class="h-2 rounded-full bg-slate-100">
              <div class="h-2 rounded-full bg-blue-600" :style="{ width: `${item.value}%` }" />
            </div>
          </div>
        </div>
      </BaseCard>
    </section>
  </main>
</template>

<script setup>
import AdminTopNavbar from '@/components/admin/AdminTopNavbar.vue'
import BaseCard from '@/components/common/BaseCard.vue'

const stats = [
  { title: 'Total Klik', value: '1,284', description: 'Klik menuju external resource.' },
  { title: 'Preview Dibuka', value: '842', description: 'User membuka halaman preview materi.' },
  { title: 'Avg. Relevance', value: '88%', description: 'Rata-rata skor rekomendasi dummy.' },
]

const categories = [
  { label: 'Frontend', value: 76 },
  { label: 'Backend', value: 54 },
  { label: 'Data', value: 41 },
  { label: 'AI', value: 38 },
]
</script>
