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
    loading.value = false
  }
})

// ── Band colors ───────────────────────────────────────────────────────────────

const BAND_PALETTE = ['#f59e0b', '#10b981', '#ef4444', '#3b82f6', '#ec4899']

const allBandNames = computed(() => {
  const names = new Set<string>()
  for (const e of events.value) {
    for (const c of e.concerts) {
      if (c.i_played && c.artist?.name) names.add(c.artist.name)
    }
  }
  return Array.from(names).sort()
})

function bandColor(name: string): string {
  const idx = allBandNames.value.indexOf(name)
  return BAND_PALETTE[idx % BAND_PALETTE.length] ?? BAND_PALETTE[0] ?? '#f59e0b'
}

// ── Year stats ────────────────────────────────────────────────────────────────

const yearStats = computed(() => {
  const map = new Map<number, Map<string, number>>()
  for (const e of events.value) {
    const y = parseInt(e.event_date.slice(0, 4))
    if (!map.has(y)) map.set(y, new Map())
    const bandMap = map.get(y)!
    const playedConcert = e.concerts.find(c => c.i_played)
    const key = playedConcert?.artist?.name ?? '__attended__'
    bandMap.set(key, (bandMap.get(key) ?? 0) + 1)
  }
  return Array.from(map.entries())
    .map(([year, bandMap]) => {
      const count = Array.from(bandMap.values()).reduce((a, b) => a + b, 0)
      const bands = Array.from(bandMap.entries())
        .filter(([k]) => k !== '__attended__')
        .map(([name, count]) => ({ name, count }))
      const attended = bandMap.get('__attended__') ?? 0
      return { year, count, bands, attended }
    })
    .sort((a, b) => a.year - b.year)
})

const maxYearCount = computed(() => Math.max(...yearStats.value.map(y => y.count), 1))

// ── Month breakdown for selected year ────────────────────────────────────────

const MONTHS = [
  'January', 'February', 'March', 'April', 'May', 'June',
  'July', 'August', 'September', 'October', 'November', 'December',
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

function playedBand(event: Event): string | null {
  return event.concerts.find(c => c.i_played)?.artist?.name ?? null
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
            <!-- Count label -->
            <span
              class="text-[10px] leading-none transition-colors"
              :class="selectedYear === stat.year ? 'text-d-purple font-semibold' : 'text-gray-400'"
            >
              {{ stat.count }}
            </span>
            <!-- Bar (stacked segments) -->
            <div
              class="w-full rounded-t cursor-pointer overflow-hidden"
              :style="{ height: `${Math.max((stat.count / maxYearCount) * 80, 4)}px` }"
              @click="selectedYear = stat.year"
            >
              <div class="h-full flex flex-col">
                <!-- Played segments — one per band, at the top -->
                <div
                  v-for="band in stat.bands"
                  :key="band.name"
                  class="transition-opacity"
                  :style="{
                    height: `${(band.count / stat.count) * 100}%`,
                    background: bandColor(band.name),
                    opacity: selectedYear === stat.year ? 1 : 0.65,
                  }"
                />
                <!-- Attended segment — at the bottom -->
                <div
                  v-if="stat.attended > 0"
                  class="transition-colors"
                  :style="{
                    height: `${(stat.attended / stat.count) * 100}%`,
                    background: selectedYear === stat.year
                      ? 'var(--d-purple)'
                      : 'color-mix(in srgb, var(--d-purple) 25%, transparent)',
                  }"
                />
              </div>
            </div>
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

        <!-- Legend -->
        <div v-if="allBandNames.length > 0" class="flex flex-wrap items-center gap-x-4 gap-y-1.5 mt-3 pt-3 border-t border-gray-100 dark:border-gray-800">
          <div v-for="name in allBandNames" :key="name" class="flex items-center gap-1.5">
            <span class="w-2.5 h-2.5 rounded-sm shrink-0" :style="{ background: bandColor(name) }" />
            <span class="text-xs text-gray-600 dark:text-gray-400">{{ name }}</span>
          </div>
          <div class="flex items-center gap-1.5">
            <span class="w-2.5 h-2.5 rounded-sm shrink-0" style="background: color-mix(in srgb, var(--d-purple) 40%, transparent)" />
            <span class="text-xs text-gray-600 dark:text-gray-400">Attending</span>
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
                <div class="flex flex-wrap gap-1.5 mt-1">
                  <span
                    v-if="event.festival"
                    class="inline-block text-[10px] badge-d-red px-1.5 py-0.5 rounded-full leading-none"
                  >
                    {{ event.festival.name }}
                  </span>
                  <span
                    v-if="playedBand(event)"
                    class="inline-flex items-center gap-1 text-[10px] px-1.5 py-0.5 rounded-full leading-none font-medium text-white"
                    :style="{ background: bandColor(playedBand(event)!) }"
                  >
                    <i class="pi pi-microphone" style="font-size: 0.55rem" />
                    {{ playedBand(event) }}
                  </span>
                </div>
              </div>

              <i class="pi pi-arrow-right text-xs text-gray-300 shrink-0 mt-1" />
            </div>
          </div>
        </div>
      </div>

    </template>
  </div>
</template>
