<template>
  <main class="min-h-screen bg-slate-50 text-slate-950">
    <AdminTopNavbar />

    <section class="mx-auto max-w-7xl px-5 py-6 lg:px-8">
      <div class="mb-7">
        <h1 class="text-3xl font-bold tracking-tight text-slate-950">Settings</h1>
        <p class="mt-2 max-w-2xl text-sm leading-6 text-slate-600">
          Pengaturan dummy untuk preferensi admin Brainpath.
        </p>
      </div>

      <div class="grid gap-5 lg:grid-cols-2">
        <BaseCard padding="lg" class="rounded-3xl">
          <h2 class="text-lg font-semibold text-slate-950">Recommendation Rules</h2>
          <div class="mt-5 space-y-4">
            <label
              v-for="item in rules"
              :key="item"
              class="flex items-center justify-between rounded-2xl bg-slate-50 px-4 py-3 text-sm"
            >
              <span class="font-medium text-slate-700">{{ item }}</span>
              <input type="checkbox" checked class="h-4 w-4 accent-blue-600" />
            </label>
          </div>
        </BaseCard>

        <BaseCard padding="lg" class="rounded-3xl">
          <h2 class="text-lg font-semibold text-slate-950">Admin Profile</h2>
          <div class="mt-5 space-y-4">
            <div>
              <label class="mb-2 block text-sm font-medium text-slate-700">Nama Admin</label>
              <input class="h-10 w-full rounded-xl border border-slate-200 px-4 text-sm outline-none focus:border-blue-500 focus:ring-4 focus:ring-blue-100" value="Admin Brainpath" />
            </div>
            <div>
              <label class="mb-2 block text-sm font-medium text-slate-700">Email</label>
              <input class="h-10 w-full rounded-xl border border-slate-200 px-4 text-sm outline-none focus:border-blue-500 focus:ring-4 focus:ring-blue-100" value="admin@brainpath.dev" />
            </div>
            <button class="h-10 rounded-xl bg-blue-600 px-5 text-sm font-semibold text-white hover:bg-blue-700">
              Simpan
            </button>
          </div>
        </BaseCard>
      </div>
    </section>
  </main>
</template>

<script setup>
import AdminTopNavbar from '@/components/admin/AdminTopNavbar.vue'
import BaseCard from '@/components/common/BaseCard.vue'

const rules = [
  'Prioritaskan resource pemula',
  'Tampilkan hanya external link aktif',
  'Gunakan AI summary pada preview materi',
]
</script>
