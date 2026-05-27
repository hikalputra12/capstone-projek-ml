<template>
  <BaseCard :selected="highlight" :interactive="interactive" padding="lg" class="h-full min-h-[220px]">
    <div class="flex h-full flex-col">
      <IconBox
        v-if="icon"
        :icon="icon"
        :color="iconColor"
        size="xl"
      />

      <div class="mt-5">
        <p v-if="eyebrow" class="text-sm font-black uppercase tracking-wide text-blue-600">
          {{ eyebrow }}
        </p>
        <h3 class="text-xl font-black leading-7 text-slate-950">{{ title }}</h3>
        <p v-if="description" class="mt-3 text-base font-medium leading-7 text-slate-500">
          {{ description }}
        </p>
      </div>
    </div>

    <div v-if="value || $slots.footer" class="mt-4 flex items-end justify-between gap-3">
      <p v-if="value" class="text-2xl font-black text-slate-950">{{ value }}</p>
      <slot name="footer" />
    </div>
  </BaseCard>
</template>

<script setup>
import BaseCard from '@/components/common/BaseCard.vue'
import IconBox from '@/components/common/IconBox.vue'

defineProps({
  eyebrow: {
    type: String,
    default: '',
  },
  title: {
    type: String,
    required: true,
  },
  description: {
    type: String,
    default: '',
  },
  value: {
    type: [String, Number],
    default: '',
  },
  icon: {
    type: [Object, Function],
    default: null,
  },
  iconColor: {
    type: String,
    default: 'blue',
  },
  highlight: {
    type: Boolean,
    default: false,
  },
  interactive: {
    type: Boolean,
    default: false,
  },
})
</script>
