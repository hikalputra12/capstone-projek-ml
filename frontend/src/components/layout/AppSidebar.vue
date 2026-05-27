<template>
  <aside class="sticky top-0 hidden h-screen w-[224px] shrink-0 border-r border-slate-200 bg-white md:flex md:flex-col">
    <RouterLink
      :to="brandTo"
      class="flex h-14 items-center gap-2.5 border-b border-slate-200 px-4"
    >
      <span
        class="grid h-8 w-8 place-items-center rounded-xl bg-gradient-to-br from-blue-600 to-violet-600 text-xs font-black text-white shadow-sm"
        aria-hidden="true"
      >
        BP
      </span>
      <span class="text-base font-extrabold tracking-tight text-blue-700">{{ brand }}</span>
    </RouterLink>

    <nav class="min-h-0 flex-1 overflow-y-auto px-2.5 py-4">
      <RouterLink
        v-for="item in items"
        :key="item.path"
        :to="item.path"
        class="mb-1.5 flex h-9 items-center gap-2.5 rounded-[11px] px-2.5 text-xs font-bold transition"
        :class="
          isActive(item)
            ? 'bg-blue-600 text-white shadow-sm'
            : 'text-slate-500 hover:bg-slate-50 hover:text-slate-800'
        "
      >
        <component :is="icons[item.icon]" class="h-4 w-4 shrink-0" />
        <span>{{ item.label }}</span>
      </RouterLink>
    </nav>

    <div class="shrink-0 border-t border-slate-200 px-2.5 py-2.5">
      <RouterLink
        v-if="canAccessAdmin"
        to="/admin/resources"
        class="mb-2 flex h-9 items-center justify-center gap-2 rounded-xl border border-blue-100 bg-white text-xs font-black text-blue-700 shadow-sm transition hover:bg-blue-50"
      >
        <component :is="icons.admin" class="h-4 w-4" />
        Admin Resource
      </RouterLink>

      <button
        type="button"
        class="mb-2 flex h-9 w-full items-center justify-center gap-2 rounded-xl border border-slate-200 bg-white text-xs font-black text-slate-600 shadow-sm transition hover:bg-slate-50 hover:text-slate-950"
        @click="handleLogout"
      >
        <component :is="icons.logout" class="h-4 w-4" />
        Logout
      </button>

      <div v-if="helperTitle || helperText" class="rounded-2xl bg-blue-50 px-3 py-2.5">
        <div class="flex items-center gap-2">
          <component :is="icons.chat" class="h-4 w-4 text-blue-700" />
          <p class="text-xs font-extrabold text-blue-700">{{ helperTitle }}</p>
        </div>
        <p class="mt-1 text-[11px] leading-4 text-slate-500">
          {{ helperText }}
        </p>
      </div>
    </div>
  </aside>
</template>

<script setup>
import { h } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { getCurrentUser, logoutUser } from '@/lib/auth'

const route = useRoute()
const router = useRouter()
const currentUser = getCurrentUser()
const canAccessAdmin = currentUser?.role === 'admin'

const handleLogout = () => {
  logoutUser()
  router.push('/')
}

defineProps({
  brand: {
    type: String,
    default: 'Brainpath',
  },
  brandTo: {
    type: [String, Object],
    default: '/dashboard',
  },
  items: {
    type: Array,
    default: () => [
      { label: 'Dashboard', path: '/dashboard', icon: 'dashboard', match: ['/dashboard'] },
      { label: 'Recommendation', path: '/recommendation', icon: 'sparkle', match: ['/recommendation'] },
      { label: 'Riwayat', path: '/history', icon: 'progress', match: ['/history'] },
      { label: 'Profile', path: '/profile', icon: 'profile', match: ['/profile'] },
    ],
  },
  helperTitle: {
    type: String,
    default: 'Tanya AI',
  },
  helperText: {
    type: String,
    default: 'Asisten belajar siap membantu memilih resource yang cocok.',
  },
})

const isActive = (item) => item.match.some((path) => route.path.startsWith(path))

const createIcon = (paths) =>
  ({
    render() {
      return h(
        'svg',
        {
          viewBox: '0 0 24 24',
          fill: 'none',
          stroke: 'currentColor',
          'stroke-width': 1.9,
          'stroke-linecap': 'round',
          'stroke-linejoin': 'round',
          'aria-hidden': 'true',
        },
        paths.map((attrs) => h(attrs.tag ?? 'path', attrs)),
      )
    },
  })

const icons = {
  dashboard: createIcon([
    { tag: 'rect', x: 4, y: 4, width: 6, height: 6, rx: 1 },
    { tag: 'rect', x: 14, y: 4, width: 6, height: 6, rx: 1 },
    { tag: 'rect', x: 4, y: 14, width: 6, height: 6, rx: 1 },
    { tag: 'rect', x: 14, y: 14, width: 6, height: 6, rx: 1 },
  ]),
  courses: createIcon([
    { d: 'M4 5.5h7a3 3 0 0 1 3 3v10a3 3 0 0 0-3-3H4z' },
    { d: 'M20 5.5h-7a3 3 0 0 0-3 3v10a3 3 0 0 1 3-3h7z' },
  ]),
  sparkle: createIcon([
    { d: 'M12 3l1.35 4.15L17.5 8.5l-4.15 1.35L12 14l-1.35-4.15L6.5 8.5l4.15-1.35z' },
    { d: 'M18 13l.75 2.25L21 16l-2.25.75L18 19l-.75-2.25L15 16l2.25-.75z' },
    { d: 'M5.5 13.5l.5 1.5 1.5.5-1.5.5-.5 1.5-.5-1.5-1.5-.5 1.5-.5z' },
  ]),
  progress: createIcon([
    { d: 'M5 19V9' },
    { d: 'M12 19V5' },
    { d: 'M19 19v-7' },
    { d: 'M4 19h16' },
  ]),
  profile: createIcon([
    { tag: 'circle', cx: 12, cy: 8, r: 3.25 },
    { d: 'M6.5 19a5.5 5.5 0 0 1 11 0' },
  ]),
  admin: createIcon([
    { tag: 'rect', x: 4, y: 4, width: 16, height: 16, rx: 3 },
    { d: 'M8 9h8' },
    { d: 'M8 13h5' },
    { d: 'M8 17h8' },
  ]),
  chat: createIcon([
    { d: 'M5 6.5A3.5 3.5 0 0 1 8.5 3h7A3.5 3.5 0 0 1 19 6.5v5A3.5 3.5 0 0 1 15.5 15H11l-4 4v-4.2A3.5 3.5 0 0 1 5 11.5z' },
    { d: 'M9 8h6' },
    { d: 'M9 11h4' },
  ]),
  logout: createIcon([
    { d: 'M10 17l5-5-5-5' },
    { d: 'M15 12H3' },
    { d: 'M14 4h4a3 3 0 0 1 3 3v10a3 3 0 0 1-3 3h-4' },
  ]),
}
</script>
