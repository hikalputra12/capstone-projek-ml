<template>
  <nav
    class="mx-auto w-full max-w-5xl overflow-x-auto rounded-full bg-white/70 px-2.5 py-1.5 shadow-sm ring-1 ring-slate-200/70 backdrop-blur"
    :aria-label="ariaLabel"
  >
    <ol class="flex min-w-[560px] items-center">
      <li
        v-for="(step, index) in normalizedSteps"
        :key="step.key"
        class="flex flex-1 items-center"
      >
        <div class="flex shrink-0 items-center gap-2">
          <span
            class="grid h-7 w-7 place-items-center rounded-full text-[11px] font-bold transition"
            :class="
              index + 1 === current
                ? 'bg-blue-600 text-white shadow-sm'
                : index + 1 < current
                  ? 'bg-blue-50 text-blue-600'
                  : 'bg-transparent text-slate-500'
            "
          >
            {{ index + 1 }}
          </span>
          <span
            class="whitespace-nowrap text-xs font-bold"
            :class="index + 1 === current ? 'text-blue-700' : 'text-slate-600'"
          >
            {{ step.label }}
          </span>
        </div>

        <span
          v-if="index < normalizedSteps.length - 1"
          class="mx-4 h-px flex-1 rounded-full"
          :class="index + 1 < current ? 'bg-blue-300' : 'bg-slate-200'"
        />
      </li>
    </ol>
  </nav>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  current: {
    type: Number,
    required: true,
  },
  steps: {
    type: Array,
    default: () => [],
  },
  labels: {
    type: Array,
    default: () => ['IT Familiarity', 'Reframing', 'Minat', 'Rekomendasi'],
  },
  ariaLabel: {
    type: String,
    default: 'Progress onboarding',
  },
})

const normalizedSteps = computed(() => {
  const source = props.steps.length ? props.steps : props.labels

  return source.map((step, index) => {
    if (typeof step === 'string') {
      return {
        key: step,
        label: step,
      }
    }

    return {
      key: step.key ?? step.label ?? index,
      label: step.label ?? `Step ${index + 1}`,
    }
  })
})
</script>
