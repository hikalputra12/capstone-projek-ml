<template>
  <header class="sticky top-0 z-40 border-b border-slate-200 bg-white/95 backdrop-blur">
    <div class="mx-auto flex h-16 max-w-7xl items-center justify-between px-5 lg:px-8">
      <div class="flex items-center gap-8">
        <RouterLink to="/admin/resources" class="flex items-center gap-2.5">
          <span
            class="grid h-9 w-9 place-items-center rounded-xl bg-gradient-to-br from-blue-600 to-violet-600 text-sm font-semibold text-white shadow-sm"
            aria-hidden="true"
          >
            BP
          </span>
          <span class="text-lg font-extrabold tracking-tight text-slate-950">Brainpath</span>
        </RouterLink>

        <nav class="hidden items-center gap-1 md:flex" aria-label="Admin navigation">
          <RouterLink
            v-for="item in menu"
            :key="item.label"
            :to="item.to"
            class="rounded-xl px-3.5 py-2 text-sm font-medium transition"
            :class="
              isActive(item.to)
                ? 'bg-blue-50 text-blue-700'
                : 'text-slate-500 hover:bg-slate-100 hover:text-slate-950'
            "
          >
            {{ item.label }}
          </RouterLink>
        </nav>
      </div>

      <div class="flex items-center gap-4">
        <RouterLink
          to="/"
          class="hidden text-sm font-medium text-slate-500 transition hover:text-blue-700 sm:inline"
        >
          Kembali ke App
        </RouterLink>
        <span
          class="grid h-10 w-10 place-items-center rounded-full bg-slate-950 text-sm font-semibold text-white shadow-sm"
          aria-label="Admin avatar"
        >
          A
        </span>
      </div>
    </div>
  </header>
</template>

<script setup>
import { useRoute } from 'vue-router'

const route = useRoute()

const menu = [
  { label: 'Resources', to: '/admin/resources' },
  { label: 'Analytics', to: '/admin/analytics' },
  { label: 'Settings', to: '/admin/settings' },
]

const isActive = (path) => route.path === path
</script>
