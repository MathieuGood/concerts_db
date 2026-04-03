<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import InputText from 'primevue/inputtext'
import IconField from 'primevue/iconfield'
import InputIcon from 'primevue/inputicon'
import Button from 'primevue/button'
import ProgressSpinner from 'primevue/progressspinner'
import DataTable from 'primevue/datatable'
import Column from 'primevue/column'
import { eventService } from '@/services/eventService'
import type { Event } from '@/models/Event'

const router = useRouter()
const events = ref<Event[]>([])
const loading = ref(true)
const search = ref('')

onMounted(async () => {
  try {
    events.value = await eventService.getAll()
  } finally {
    loading.value = false
  }
})

function artistNames(event: Event): string {
  return event.concerts.map((c) => c.artist?.name ?? '—').join(', ')
}

function formatDate(dateStr: string): string {
  return new Date(dateStr + 'T00:00:00').toLocaleDateString('en-GB', {
    day: '2-digit',
    month: 'short',
    year: 'numeric',
  })
}

function fuzzy(query: string, target: string): boolean {
  let ti = 0
  for (let qi = 0; qi < query.length; qi++) {
    while (ti < target.length && target[ti] !== query[qi]) ti++
    if (ti === target.length) return false
    ti++
  }
  return true
}

function fuzzyMatch(q: string, e: Event): boolean {
  const artists = e.concerts.map((c) => c.artist?.name ?? '').join(' ')
  const fields = [
    e.name ?? '',
    e.event_date,
    e.venue?.name ?? '',
    e.venue?.city?.name ?? '',
    e.venue?.city?.country?.name ?? '',
    e.festival?.name ?? '',
    artists,
  ]
  return fields.some((f) => fuzzy(q, f.toLowerCase()))
}

const filtered = computed(() => {
  const q = search.value.trim().toLowerCase()
  if (!q) return events.value
  return events.value.filter((e) => fuzzyMatch(q, e))
})

function goToEvent(id: number) {
  router.push(`/event/${id}`)
}
</script>

<template>
  <div class="space-y-4">
    <!-- Header row -->
    <div class="flex items-center gap-3">
      <IconField class="flex-1">
        <InputIcon class="pi pi-search" />
        <InputText
          v-model="search"
          placeholder="Search by artist, venue, festival, date…"
          class="w-full"
        />
      </IconField>
      <Button
        icon="pi pi-plus"
        label="New"
        size="small"
        class="shrink-0"
        @click="router.push('/event/new')"
      />
    </div>

    <!-- Loading -->
    <div v-if="loading" class="flex justify-center py-16">
      <ProgressSpinner style="width: 40px; height: 40px" />
    </div>

    <!-- Empty state -->
    <div v-else-if="filtered.length === 0" class="text-center py-16 text-gray-400">
      <i class="pi pi-music text-4xl mb-3 block" />
      <p>{{ search ? 'No events match your search.' : 'No events yet. Add your first one!' }}</p>
    </div>

    <template v-else>
      <!-- Mobile cards (< md) -->
      <div class="md:hidden space-y-3">
        <div
          v-for="event in filtered"
          :key="event.id"
          class="bg-white dark:bg-gray-900 rounded-xl border border-gray-200 dark:border-gray-700 p-4 cursor-pointer active:opacity-70 transition-opacity"
          @click="goToEvent(event.id)"
        >
          <div class="flex items-start justify-between gap-2">
            <div class="min-w-0">
              <p class="font-semibold text-gray-900 dark:text-gray-100 truncate">
                {{ artistNames(event) || event.name || '—' }}
              </p>
              <p class="text-sm text-gray-500 dark:text-gray-400 mt-0.5">
                {{ event.venue?.name }}
                <span v-if="event.venue?.city?.name"> — {{ event.venue.city.name }}</span>
              </p>
              <span
                v-if="event.festival"
                class="inline-block mt-1 text-xs bg-violet-100 dark:bg-violet-900/40 text-violet-700 dark:text-violet-300 px-2 py-0.5 rounded-full"
              >
                {{ event.festival.name }}
              </span>
            </div>
            <span class="text-xs text-gray-400 dark:text-gray-500 shrink-0 pt-0.5">
              {{ formatDate(event.event_date) }}
            </span>
          </div>
        </div>
      </div>

      <!-- Desktop table (>= md) -->
      <div class="hidden md:block">
        <DataTable
          :value="filtered"
          row-hover
          class="rounded-xl overflow-hidden border border-gray-200 dark:border-gray-700"
          @row-click="(e) => goToEvent(e.data.id)"
          style="cursor: pointer"
        >
          <Column field="event_date" header="Date" style="width: 120px">
            <template #body="{ data }">
              {{ formatDate(data.event_date) }}
            </template>
          </Column>
          <Column header="Artists">
            <template #body="{ data }">
              {{ artistNames(data) || data.name || '—' }}
            </template>
          </Column>
          <Column header="Venue">
            <template #body="{ data }">
              {{ data.venue?.name }}
            </template>
          </Column>
          <Column header="City">
            <template #body="{ data }">
              {{ data.venue?.city?.name }}
            </template>
          </Column>
          <Column header="Festival">
            <template #body="{ data }">
              <span
                v-if="data.festival"
                class="text-xs bg-violet-100 dark:bg-violet-900/40 text-violet-700 dark:text-violet-300 px-2 py-0.5 rounded-full"
              >
                {{ data.festival.name }}
              </span>
            </template>
          </Column>
        </DataTable>
        <p class="text-xs text-gray-400 mt-2 text-right">{{ filtered.length }} event{{ filtered.length !== 1 ? 's' : '' }}</p>
      </div>
    </template>
  </div>
</template>
