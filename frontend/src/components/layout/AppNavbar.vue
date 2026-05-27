<template>
  <header class="sticky top-0 z-40 border-b border-slate-200 bg-white/90 backdrop-blur">
    <div class="mx-auto flex h-16 max-w-7xl items-center justify-between px-4 sm:px-5 lg:px-6">
      <RouterLink :to="brandTo" class="flex items-center gap-2.5">
        <span
          class="grid h-9 w-9 place-items-center rounded-xl bg-gradient-to-br from-blue-600 to-violet-600 text-sm font-black text-white shadow-sm"
          aria-hidden="true"
        >
          BP
        </span>
        <span class="text-lg font-black tracking-tight text-slate-950">{{ brand }}</span>
      </RouterLink>

      <nav class="hidden items-center gap-2 md:flex" :aria-label="navLabel">
        <RouterLink
          v-for="item in items"
          :key="item.label"
          :to="item.to"
          class="rounded-xl px-3.5 py-2 text-sm font-bold text-slate-600 transition hover:bg-slate-100 hover:text-blue-700"
          active-class="bg-blue-50 text-blue-700"
        >
          {{ item.label }}
        </RouterLink>
      </nav>

      <RouterLink
        v-if="ctaLabel"
        :to="ctaTo"
        class="hidden h-10 items-center rounded-xl bg-blue-600 px-5 text-sm font-black text-white shadow-sm transition hover:bg-blue-700 sm:inline-flex"
      >
        {{ ctaLabel }}
      </RouterLink>
    </div>
  </header>
</template>

<script setup>
defineProps({
  brand: {
    type: String,
    default: 'Brainpath',
  },
  brandTo: {
    type: [String, Object],
    default: '/',
  },
  navLabel: {
    type: String,
    default: 'Navigasi utama',
  },
  items: {
    type: Array,
    default: () => [
      { label: 'Beranda', to: '/' },
      { label: 'Dashboard', to: '/dashboard' },
      { label: 'Rekomendasi', to: '/recommendation' },
    ],
  },
  ctaLabel: {
    type: String,
    default: 'Login',
  },
  ctaTo: {
    type: [String, Object],
    default: '/login',
  },
})
</script>
