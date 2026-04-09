<script setup lang="ts">
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import Button from 'primevue/button'
import type { Event } from '@/models/Event'

const props = defineProps<{ events: Event[] }>()
const router = useRouter()

// Start on the most recent month that has an event, or today
function latestEventMonth(): Date {
  if (props.events.length === 0) return new Date()
  const latest = props.events.reduce((a, b) => a.event_date > b.event_date ? a : b)
  const d = new Date(latest.event_date + 'T00:00:00')
  return new Date(d.getFullYear(), d.getMonth(), 1)
}

const currentMonth = ref<Date>(latestEventMonth())

const prevMonth = () => currentMonth.value = new Date(currentMonth.value.getFullYear(), currentMonth.value.getMonth() - 1, 1)
const nextMonth = () => currentMonth.value = new Date(currentMonth.value.getFullYear(), currentMonth.value.getMonth() + 1, 1)

const monthLabel = computed(() =>
  currentMonth.value.toLocaleDateString('en-GB', { month: 'long', year: 'numeric' })
)

// Map date string → events
const eventsByDate = computed(() => {
  const map = new Map<string, Event[]>()
  for (const e of props.events) {
    const list = map.get(e.event_date) ?? []
    list.push(e)
    map.set(e.event_date, list)
  }
  return map
})

// Build the 6×7 grid (Mon-first, European style)
const calendarGrid = computed(() => {
  const year = currentMonth.value.getFullYear()
  const month = currentMonth.value.getMonth()
  const firstDay = new Date(year, month, 1)
  const lastDay = new Date(year, month + 1, 0)
  // Mon=0 … Sun=6
  const startPad = (firstDay.getDay() + 6) % 7
  const totalCells = Math.ceil((startPad + lastDay.getDate()) / 7) * 7

  const cells: Array<{ dateStr: string; day: number; inMonth: boolean }> = []
  for (let i = 0; i < totalCells; i++) {
    const d = new Date(year, month, 1 - startPad + i)
    const dateStr = d.toISOString().slice(0, 10)
    cells.push({ dateStr, day: d.getDate(), inMonth: d.getMonth() === month })
  }
  return cells
})

const todayStr = new Date().toISOString().slice(0, 10)
const selectedDay = ref<string | null>(null)

const selectedEvents = computed(() =>
  selectedDay.value ? (eventsByDate.value.get(selectedDay.value) ?? []) : []
)

function selectDay(dateStr: string) {
  if (!eventsByDate.value.has(dateStr)) return
  selectedDay.value = selectedDay.value === dateStr ? null : dateStr
}

function artistNames(event: Event): string {
  return event.concerts.map(c => c.artist?.name ?? '—').join(', ')
}

function formatDate(dateStr: string): string {
  return new Date(dateStr + 'T00:00:00').toLocaleDateString('en-GB', {
    weekday: 'long', day: 'numeric', month: 'long', year: 'numeric',
  })
}

// Stats for current month
const monthStats = computed(() => {
  const year = currentMonth.value.getFullYear()
  const month = currentMonth.value.getMonth()
  const count = props.events.filter(e => {
    const d = new Date(e.event_date + 'T00:00:00')
    return d.getFullYear() === year && d.getMonth() === month
  }).length
  return count
})

// Year strip: one dot per month with events for quick navigation
const yearStrip = computed(() => {
  const year = currentMonth.value.getFullYear()
  return Array.from({ length: 12 }, (_, m) => {
    const key = `${year}-${String(m + 1).padStart(2, '0')}`
    const count = props.events.filter(e => e.event_date.startsWith(key)).length
    return { month: m, count, label: new Date(year, m, 1).toLocaleDateString('en-GB', { month: 'short' }) }
  })
})

function jumpToMonth(m: number) {
  currentMonth.value = new Date(currentMonth.value.getFullYear(), m, 1)
  selectedDay.value = null
}

function prevYear() {
  currentMonth.value = new Date(currentMonth.value.getFullYear() - 1, currentMonth.value.getMonth(), 1)
  selectedDay.value = null
}
function nextYear() {
  currentMonth.value = new Date(currentMonth.value.getFullYear() + 1, currentMonth.value.getMonth(), 1)
  selectedDay.value = null
}
</script>

<template>
  <div class="space-y-4">

    <!-- Year strip -->
    <div class="bg-white dark:bg-gray-900 rounded-xl border border-gray-200 dark:border-gray-700 p-3">
      <div class="flex items-center gap-1 mb-2">
        <Button icon="pi pi-chevron-left" text rounded size="small" severity="secondary" @click="prevYear" />
        <span class="text-sm font-semibold text-gray-700 dark:text-gray-300 flex-1 text-center">{{ currentMonth.getFullYear() }}</span>
        <Button icon="pi pi-chevron-right" text rounded size="small" severity="secondary" @click="nextYear" />
      </div>
      <div class="grid grid-cols-12 gap-0.5">
        <button
          v-for="item in yearStrip"
          :key="item.month"
          class="flex flex-col items-center py-1 rounded-lg text-xs transition-colors"
          :class="item.month === currentMonth.getMonth()
            ? 'bg-violet-100 dark:bg-violet-900/40 text-violet-700 dark:text-violet-300 font-semibold'
            : item.count > 0
              ? 'text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-800 cursor-pointer'
              : 'text-gray-300 dark:text-gray-600 cursor-default'"
          @click="item.count > 0 ? jumpToMonth(item.month) : undefined"
        >
          <span>{{ item.label }}</span>
          <span v-if="item.count > 0" class="text-violet-500 dark:text-violet-400 font-bold leading-none mt-0.5">{{ item.count }}</span>
          <span v-else class="leading-none mt-0.5 opacity-0">0</span>
        </button>
      </div>
    </div>

    <!-- Month grid -->
    <div class="bg-white dark:bg-gray-900 rounded-xl border border-gray-200 dark:border-gray-700 overflow-hidden">
      <!-- Month navigation -->
      <div class="flex items-center justify-between px-4 py-3 border-b border-gray-100 dark:border-gray-800">
        <Button icon="pi pi-chevron-left" text rounded size="small" severity="secondary" @click="prevMonth" />
        <div class="text-center">
          <span class="font-semibold text-gray-900 dark:text-gray-100 capitalize">{{ monthLabel }}</span>
          <span v-if="monthStats > 0" class="ml-2 text-xs text-violet-500 dark:text-violet-400">{{ monthStats }} show{{ monthStats !== 1 ? 's' : '' }}</span>
        </div>
        <Button icon="pi pi-chevron-right" text rounded size="small" severity="secondary" @click="nextMonth" />
      </div>

      <!-- Day headers -->
      <div class="grid grid-cols-7 border-b border-gray-100 dark:border-gray-800">
        <div v-for="d in ['Mo','Tu','We','Th','Fr','Sa','Su']" :key="d"
             class="text-center text-xs font-medium text-gray-400 dark:text-gray-500 py-2">
          {{ d }}
        </div>
      </div>

      <!-- Day cells -->
      <div class="grid grid-cols-7">
        <button
          v-for="cell in calendarGrid"
          :key="cell.dateStr"
          class="relative min-h-[2.75rem] flex flex-col items-center justify-start pt-1.5 pb-1 border-b border-r border-gray-50 dark:border-gray-800/60 transition-colors last-of-type:border-r-0"
          :class="[
            !cell.inMonth ? 'opacity-25 cursor-default' : '',
            eventsByDate.has(cell.dateStr) && cell.inMonth ? 'cursor-pointer hover:bg-violet-50 dark:hover:bg-violet-950/30' : 'cursor-default',
            selectedDay === cell.dateStr ? 'bg-violet-100 dark:bg-violet-900/40' : '',
            cell.dateStr === todayStr && cell.inMonth ? 'font-bold' : '',
          ]"
          @click="cell.inMonth ? selectDay(cell.dateStr) : undefined"
        >
          <!-- Day number -->
          <span
            class="text-xs w-6 h-6 flex items-center justify-center rounded-full leading-none"
            :class="[
              cell.dateStr === todayStr && cell.inMonth
                ? 'bg-violet-600 text-white font-bold'
                : cell.inMonth ? 'text-gray-700 dark:text-gray-200' : 'text-gray-400',
            ]"
          >
            {{ cell.day }}
          </span>

          <!-- Event dot(s) -->
          <div v-if="eventsByDate.has(cell.dateStr) && cell.inMonth" class="flex items-center gap-0.5 mt-0.5">
            <template v-if="(eventsByDate.get(cell.dateStr)?.length ?? 0) <= 3">
              <span
                v-for="i in (eventsByDate.get(cell.dateStr)?.length ?? 0)"
                :key="i"
                class="w-1.5 h-1.5 rounded-full bg-violet-500 dark:bg-violet-400"
              />
            </template>
            <template v-else>
              <span class="text-[10px] font-semibold text-violet-600 dark:text-violet-400">
                {{ eventsByDate.get(cell.dateStr)?.length }}
              </span>
            </template>
          </div>
        </button>
      </div>
    </div>

    <!-- Selected day event list -->
    <Transition name="slide-down">
      <div v-if="selectedDay && selectedEvents.length > 0"
           class="bg-white dark:bg-gray-900 rounded-xl border border-violet-200 dark:border-violet-800 overflow-hidden">
        <div class="px-4 py-3 border-b border-violet-100 dark:border-violet-900 bg-violet-50 dark:bg-violet-950/30 flex items-center justify-between">
          <span class="text-sm font-semibold text-violet-700 dark:text-violet-300 capitalize">{{ formatDate(selectedDay) }}</span>
          <button class="text-violet-400 hover:text-violet-600" @click="selectedDay = null">
            <i class="pi pi-times text-xs" />
          </button>
        </div>
        <div
          v-for="event in selectedEvents"
          :key="event.id"
          class="flex items-center gap-3 px-4 py-3 border-b border-gray-50 dark:border-gray-800/50 last:border-0 cursor-pointer hover:bg-gray-50 dark:hover:bg-gray-800/30 active:opacity-70"
          @click="router.push(`/event/${event.id}`)"
        >
          <div class="flex-1 min-w-0">
            <div class="font-medium text-sm text-gray-900 dark:text-gray-100 truncate">
              {{ artistNames(event) || event.name || '—' }}
            </div>
            <div class="text-xs text-gray-500 dark:text-gray-400 mt-0.5 truncate">
              {{ event.venue?.name }}<span v-if="event.venue?.city"> — {{ event.venue.city.name }}</span>
            </div>
            <span v-if="event.festival" class="inline-block mt-1 text-xs bg-violet-100 dark:bg-violet-900/40 text-violet-700 dark:text-violet-300 px-2 py-0.5 rounded-full">
              {{ event.festival.name }}
            </span>
          </div>
          <i class="pi pi-arrow-right text-xs text-gray-300 shrink-0" />
        </div>
      </div>
    </Transition>

  </div>
</template>

<style scoped>
.slide-down-enter-active,
.slide-down-leave-active {
  transition: opacity 0.15s ease, transform 0.15s ease;
}
.slide-down-enter-from,
.slide-down-leave-to {
  opacity: 0;
  transform: translateY(-6px);
}
</style>
