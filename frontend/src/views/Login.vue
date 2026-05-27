<template>
  <main class="flex min-h-screen items-center justify-center bg-gradient-to-br from-blue-50 via-white to-violet-50 px-5 py-10 text-slate-950">
    <section class="w-full max-w-md">
      <RouterLink to="/" class="mb-8 flex items-center justify-center gap-3">
        <span class="grid h-10 w-10 place-items-center rounded-2xl bg-gradient-to-br from-blue-600 to-violet-600 text-sm font-black text-white shadow-sm">
          BP
        </span>
        <span class="text-xl font-black tracking-tight text-slate-950">Brainpath</span>
      </RouterLink>

      <BaseCard padding="lg" class="shadow-xl shadow-blue-100/70">
        <div class="mb-8 text-center">
          <p class="text-sm font-black uppercase tracking-wide text-blue-600">Masuk</p>
          <h1 class="mt-2 text-3xl font-black tracking-tight">Selamat datang kembali</h1>
          <p class="mt-2 text-sm font-medium leading-6 text-slate-500">
            Lanjutkan rekomendasi kursus IT yang sesuai dengan profil belajarmu.
          </p>
        </div>

        <form class="space-y-5" @submit.prevent="goToDashboard">
          <div>
            <label for="email" class="mb-2 block text-sm font-bold text-slate-800">Email</label>
            <input
              id="email"
              v-model="email"
              type="email"
              autocomplete="email"
              required
              class="h-12 w-full rounded-xl border border-slate-200 bg-white px-4 text-slate-900 shadow-sm outline-none transition placeholder:text-slate-400 focus:border-blue-500 focus:ring-4 focus:ring-blue-100"
              placeholder="user@brainpath.dev"
            />
          </div>

          <div>
            <label for="password" class="mb-2 block text-sm font-bold text-slate-800">Password</label>
            <input
              id="password"
              v-model="password"
              type="password"
              autocomplete="current-password"
              required
              class="h-12 w-full rounded-xl border border-slate-200 bg-white px-4 text-slate-900 shadow-sm outline-none transition placeholder:text-slate-400 focus:border-blue-500 focus:ring-4 focus:ring-blue-100"
              placeholder="Masukkan password"
            />
          </div>

          <BaseButton type="submit" full-width size="lg">
            Masuk
          </BaseButton>
        </form>

        <div class="mt-5 rounded-2xl bg-slate-50 p-4 text-xs leading-5 text-slate-500">
          <p><span class="font-black text-slate-700">User:</span> gunakan email bebas.</p>
          <p><span class="font-black text-slate-700">Admin:</span> admin@brainpath.dev</p>
        </div>
      </BaseCard>
    </section>
  </main>
</template>

<script setup>
import { ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import BaseButton from '@/components/common/BaseButton.vue'
import BaseCard from '@/components/common/BaseCard.vue'
import { loginUser } from '@/lib/auth'

const router = useRouter()
const route = useRoute()
const email = ref('')
const password = ref('')

const goToDashboard = () => {
  const user = loginUser(email.value)
  const redirectPath = typeof route.query.redirect === 'string' ? route.query.redirect : ''

  if (redirectPath) {
    router.push(redirectPath)
    return
  }

  router.push(user.role === 'admin' ? '/admin/resources' : '/dashboard')
}
</script>
