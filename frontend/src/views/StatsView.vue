<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import ProgressSpinner from 'primevue/progressspinner'
import { eventService } from '@/services/eventService'
import type { Event } from '@/models/Event'

const router = useRouter()
const events = ref<Event[]>([])
const loading = ref(true)
const selectedYear = ref<number | null>(null)

onMounted(async () => {
  try {
    events.value = await eventService.getAll()
    if (events.value.length > 0) {
      const years = events.value.map(e => parseInt(e.event_date.slice(0, 4)))
      selectedYear.value = Math.max(...years)
    }
  } finally {
    loading.value = false }
})

// ── Year stats ────────────────────────────────────────────────────────────────

const yearStats = computed(() => {
  const map = new Map<number, number>()
  for (const e of events.value) {
    const y = parseInt(e.event_date.slice(0, 4))
    map.set(y, (map.get(y) ?? 0) + 1)
  }
  return Array.from(map.entries())
    .map(([year, count]) => ({ year, count }))
    .sort((a, b) => a.year - b.year)
})

const maxYearCount = computed(() => Math.max(...yearStats.value.map(y => y.count), 1))

// ── Month breakdown for selected year ────────────────────────────────────────

const MONTHS = [
  'January','February','March','April','May','June',
  'July','August','September','October','November','December',
]

const monthBoxes = computed(() => {
  if (!selectedYear.value) return []
  return MONTHS.map((name, idx) => {
    const prefix = `${selectedYear.value}-${String(idx + 1).padStart(2, '0')}`
    const monthEvents = events.value
      .filter(e => e.event_date.startsWith(prefix))
      .sort((a, b) => a.event_date.localeCompare(b.event_date))
    return { name, monthIdx: idx, events: monthEvents }
  }).filter(m => m.events.length > 0)
})

const yearTotal = computed(() => monthBoxes.value.reduce((s, m) => s + m.events.length, 0))

// ── Helpers ───────────────────────────────────────────────────────────────────

function artistNames(event: Event): string {
  return event.concerts.map(c => c.artist?.name ?? '—').join(', ')
}

function dayNum(dateStr: string): string {
  return String(parseInt(dateStr.slice(8, 10)))
}
</script>

<template>
  <div class="space-y-6">
    <div v-if="loading" class="flex justify-center py-16">
      <ProgressSpinner style="width:40px;height:40px" />
    </div>

    <template v-else>

      <!-- ── Bar chart ──────────────────────────────────────────────────────── -->
      <div class="bg-white dark:bg-gray-900 rounded-xl border border-gray-200 dark:border-gray-700 p-4">
        <div class="flex items-center justify-between mb-4">
          <h2 class="font-semibold text-gray-800 dark:text-gray-100">Shows per year</h2>
          <span class="text-xs text-gray-400">{{ events.length }} total</span>
        </div>

        <!-- Bars -->
        <div class="flex items-end gap-1 h-28">
          <div
            v-for="stat in yearStats"
            :key="stat.year"
            class="flex-1 flex flex-col items-center gap-1 min-w-0"
          >
            <!-- Count label (only if bar is tall enough or selected) -->
            <span
              class="text-[10px] leading-none transition-colors"
              :class="selectedYear === stat.year ? 'text-d-purple font-semibold' : 'text-gray-400'"
            >
              {{ stat.count }}
            </span>
            <!-- Bar -->
            <div
              class="w-full rounded-t cursor-pointer transition-colors"
              :style="{
                height: `${Math.max((stat.count / maxYearCount) * 80, 4)}px`,
                background: selectedYear === stat.year
                  ? 'var(--d-purple)'
                  : 'color-mix(in srgb, var(--d-purple) 25%, transparent)',
              }"
              @click="selectedYear = stat.year"
            />
            <!-- Year label -->
            <span
              class="text-[10px] leading-none truncate w-full text-center transition-colors"
              :class="selectedYear === stat.year
                ? 'font-bold text-d-purple'
                : 'text-gray-400 dark:text-gray-500'"
            >
              {{ stat.year }}
            </span>
          </div>
        </div>
      </div>

      <!-- ── Year detail ────────────────────────────────────────────────────── -->
      <div v-if="selectedYear">
        <div class="flex items-center justify-between mb-3">
          <h2 class="font-semibold text-gray-800 dark:text-gray-100">
            {{ selectedYear }}
          </h2>
          <span class="text-xs text-gray-400">
            {{ yearTotal }} show{{ yearTotal !== 1 ? 's' : '' }}
          </span>
        </div>

        <!-- No shows this year -->
        <p v-if="monthBoxes.length === 0" class="text-sm text-gray-400 text-center py-8">
          No shows in {{ selectedYear }}.
        </p>

        <!-- Month grid -->
        <div v-else class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
          <div
            v-for="month in monthBoxes"
            :key="month.monthIdx"
            class="bg-white dark:bg-gray-900 rounded-xl border border-gray-200 dark:border-gray-700 overflow-hidden"
          >
            <!-- Month header -->
            <div class="flex items-center justify-between px-4 py-2.5 border-b border-gray-100 dark:border-gray-800 bg-gray-50 dark:bg-gray-800/50">
              <span class="text-sm font-semibold text-gray-700 dark:text-gray-200">{{ month.name }}</span>
              <span class="text-xs font-medium text-d-purple">
                {{ month.events.length }} show{{ month.events.length !== 1 ? 's' : '' }}
              </span>
            </div>

            <!-- Show list -->
            <div
              v-for="event in month.events"
              :key="event.id"
              class="flex items-start gap-3 px-4 py-2.5 border-b border-gray-50 dark:border-gray-800/50 last:border-0 cursor-pointer hover:bg-gray-50 dark:hover:bg-gray-800/30 active:opacity-70 transition-colors"
              @click="router.push(`/event/${event.id}`)"
            >
              <!-- Day number -->
              <span class="text-xs font-mono font-semibold text-d-purple w-5 shrink-0 pt-0.5">
                {{ dayNum(event.event_date) }}
              </span>

              <!-- Content -->
              <div class="flex-1 min-w-0">
                <p class="text-sm font-medium text-gray-900 dark:text-gray-100 truncate leading-snug">
                  {{ artistNames(event) || event.name || '—' }}
                </p>
                <p class="text-xs text-gray-500 dark:text-gray-400 truncate mt-0.5">
                  {{ event.venue?.name }}<span v-if="event.venue?.city?.name"> · {{ event.venue.city.name }}</span>
                </p>
                <span
                  v-if="event.festival"
                  class="inline-block mt-1 text-[10px] badge-d-red px-1.5 py-0.5 rounded-full leading-none"
                >
                  {{ event.festival.name }}
                </span>
              </div>

              <i class="pi pi-arrow-right text-xs text-gray-300 shrink-0 mt-1" />
            </div>
          </div>
        </div>
      </div>

    </template>
  </div>
</template>
