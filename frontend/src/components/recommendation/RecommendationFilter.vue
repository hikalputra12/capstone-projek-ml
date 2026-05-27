<template>
  <div class="rounded-2xl border border-slate-200 bg-white p-4 shadow-sm">
    <div class="flex flex-col gap-4 lg:flex-row lg:items-center lg:justify-between">
      <div class="flex gap-2 overflow-x-auto pb-1">
        <button
          v-for="category in categories"
          :key="category"
          type="button"
          class="shrink-0 rounded-full px-4 py-2 text-sm font-black transition"
          :class="
            category === activeCategory
              ? 'bg-blue-600 text-white shadow-sm'
              : 'bg-slate-50 text-slate-600 ring-1 ring-slate-200 hover:bg-blue-50 hover:text-blue-700'
          "
          @click="$emit('update:activeCategory', category)"
        >
          <component :is="categoryIcon(category)" class="mr-1.5 inline h-3.5 w-3.5 align-[-2px]" />
          {{ category }}
        </button>
      </div>

      <label class="flex shrink-0 flex-col gap-2 text-sm font-bold text-slate-700 sm:flex-row sm:items-center">
        Urutkan
        <select
          :value="sortBy"
          class="h-11 rounded-xl border border-slate-200 bg-white px-4 text-sm font-bold text-slate-700 outline-none transition focus:border-blue-500 focus:ring-4 focus:ring-blue-100"
          @change="$emit('update:sortBy', $event.target.value)"
        >
          <option v-for="option in sortOptions" :key="option.value" :value="option.value">
            {{ option.label }}
          </option>
        </select>
      </label>
    </div>
  </div>
</template>

<script setup>
import { BarChart3, Brain, Layers, Monitor, Server, Tag } from 'lucide-vue-next'

defineEmits(['update:activeCategory', 'update:sortBy'])

defineProps({
  categories: {
    type: Array,
    default: () => ['Semua', 'Frontend', 'Backend', 'Data', 'AI', 'General IT'],
  },
  activeCategory: {
    type: String,
    default: 'Semua',
  },
  sortBy: {
    type: String,
    default: 'relevance',
  },
  sortOptions: {
    type: Array,
    default: () => [
      { label: 'Paling Relevan', value: 'relevance' },
      { label: 'Pemula', value: 'beginner' },
      { label: 'Durasi Singkat', value: 'short' },
    ],
  },
})

const categoryIcon = (category) =>
  ({
    Semua: Layers,
    Frontend: Monitor,
    Backend: Server,
    Data: BarChart3,
    AI: Brain,
    'General IT': Tag,
  })[category] ?? Tag
</script>
