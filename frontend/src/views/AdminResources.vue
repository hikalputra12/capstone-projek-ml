<template>
  <main class="min-h-screen bg-slate-50 text-slate-950">
    <AdminTopNavbar />

    <section class="mx-auto max-w-7xl px-5 py-6 lg:px-8">
      <div class="mb-7">
        <div>
          <h1 class="text-3xl font-bold tracking-tight text-slate-950">Resource Management</h1>
          <p class="mt-2 max-w-2xl text-sm leading-6 text-slate-600">
            Kelola resource belajar eksternal yang akan direkomendasikan oleh Brainpath.
          </p>
        </div>
      </div>

      <div class="mb-7 grid gap-5 md:grid-cols-3">
        <BaseCard
          v-for="stat in stats"
          :key="stat.title"
          padding="lg"
          class="rounded-3xl"
        >
          <div class="flex items-center justify-between gap-4">
            <div>
              <p class="text-sm font-medium text-slate-600">{{ stat.title }}</p>
              <p class="mt-2 text-3xl font-semibold tracking-tight text-slate-950">{{ stat.value }}</p>
            </div>
            <span class="grid h-12 w-12 place-items-center rounded-2xl bg-gradient-to-br from-blue-500 to-violet-600 text-white shadow-sm">
              <component :is="stat.icon" class="h-5 w-5" />
            </span>
          </div>
        </BaseCard>
      </div>

      <AdminResourceTable :resources="adminResources" @add="showForm = true" />
    </section>

    <div
      v-if="showForm"
      class="fixed inset-0 z-50 flex items-center justify-center bg-slate-950/50 px-5 py-8"
    >
      <BaseCard padding="lg" class="max-h-[90vh] w-full max-w-3xl overflow-y-auto">
        <div class="mb-6 flex items-start justify-between gap-4">
          <div>
            <p class="text-sm font-semibold uppercase tracking-wide text-blue-600">Form Statis</p>
            <h2 class="mt-2 text-2xl font-semibold text-slate-950">Tambah Resource</h2>
            <p class="mt-2 text-sm leading-6 text-slate-500">
              Form ini hanya UI dummy, belum terhubung ke backend.
            </p>
          </div>
          <button
            type="button"
            class="rounded-xl bg-slate-100 px-3 py-2 text-sm font-medium text-slate-600 hover:bg-slate-200"
            @click="showForm = false"
          >
            Tutup
          </button>
        </div>

        <form class="grid gap-5 md:grid-cols-2" @submit.prevent="showForm = false">
          <div>
            <label class="mb-2 block text-sm font-medium text-slate-800" for="title">Title</label>
            <input id="title" :class="inputClass" placeholder="Contoh: HTML & CSS Dasar" />
          </div>

          <div>
            <label class="mb-2 block text-sm font-medium text-slate-800" for="url">External URL</label>
            <input id="url" :class="inputClass" placeholder="https://youtube.com/..." />
          </div>

          <div class="md:col-span-2">
            <label class="mb-2 block text-sm font-medium text-slate-800" for="description">Description</label>
            <textarea id="description" rows="3" :class="textareaClass" placeholder="Deskripsi singkat resource" />
          </div>

          <div>
            <label class="mb-2 block text-sm font-medium text-slate-800" for="category">Category</label>
            <select id="category" :class="inputClass">
              <option>Frontend</option>
              <option>Backend</option>
              <option>Data</option>
              <option>AI</option>
              <option>General IT</option>
            </select>
          </div>

          <div>
            <label class="mb-2 block text-sm font-medium text-slate-800" for="level">Level</label>
            <select id="level" :class="inputClass">
              <option>Pemula</option>
              <option>Menengah</option>
              <option>Lanjutan</option>
            </select>
          </div>

          <div>
            <label class="mb-2 block text-sm font-medium text-slate-800" for="duration">Duration</label>
            <input id="duration" :class="inputClass" placeholder="45 menit" />
          </div>

          <div>
            <label class="mb-2 block text-sm font-medium text-slate-800" for="tags">Tags</label>
            <input id="tags" :class="inputClass" placeholder="HTML, CSS, Pemula" />
          </div>

          <div class="md:col-span-2">
            <label class="mb-2 block text-sm font-medium text-slate-800" for="summary">AI Summary</label>
            <textarea id="summary" rows="3" :class="textareaClass" placeholder="Ringkasan AI singkat" />
          </div>

          <div class="md:col-span-2">
            <label class="mb-2 block text-sm font-medium text-slate-800" for="points">Learning Points</label>
            <textarea id="points" rows="3" :class="textareaClass" placeholder="Poin belajar, pisahkan dengan koma atau baris baru" />
          </div>

          <div class="flex flex-col gap-3 md:col-span-2 sm:flex-row sm:justify-end">
            <BaseButton type="button" variant="secondary" @click="showForm = false">
              Batal
            </BaseButton>
            <BaseButton type="submit">
              Simpan Dummy
            </BaseButton>
          </div>
        </form>
      </BaseCard>
    </div>
  </main>
</template>

<script setup>
import { ref } from 'vue'
import AdminResourceTable from '@/components/admin/AdminResourceTable.vue'
import AdminTopNavbar from '@/components/admin/AdminTopNavbar.vue'
import BaseButton from '@/components/common/BaseButton.vue'
import BaseCard from '@/components/common/BaseCard.vue'
import { resources } from '@/data/resources'
import { BarChart3, Layers, MousePointerClick } from 'lucide-vue-next'

const showForm = ref(false)
const inputClass =
  'h-12 w-full rounded-xl border border-slate-200 bg-white px-4 text-sm font-medium text-slate-800 shadow-sm outline-none transition placeholder:text-slate-400 focus:border-blue-500 focus:ring-4 focus:ring-blue-100'
const textareaClass =
  'w-full resize-none rounded-xl border border-slate-200 bg-white px-4 py-3 text-sm font-medium text-slate-800 shadow-sm outline-none transition placeholder:text-slate-400 focus:border-blue-500 focus:ring-4 focus:ring-blue-100'

const normalizeSource = (source) => source.split(' - ')[0]

const adminResources = resources.map((resource) => ({
  ...resource,
  source: normalizeSource(resource.source),
}))

const stats = [
  { title: 'Total Resource', value: adminResources.length, icon: Layers },
  { title: 'Total Klik Rekomendasi', value: '1,284', icon: MousePointerClick },
  { title: 'Kategori Terpopuler', value: 'Frontend', icon: BarChart3 },
]
</script>
