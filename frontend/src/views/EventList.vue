<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import InputText from 'primevue/inputtext'
import IconField from 'primevue/iconfield'
import InputIcon from 'primevue/inputicon'
import Button from 'primevue/button'
import ProgressSpinner from 'primevue/progressspinner'
import DataTable from 'primevue/datatable'
import Column from 'primevue/column'
import { eventService } from '@/services/eventService'
import { useAuth } from '@/composables/useAuth'
import type { Event } from '@/models/Event'
import { useListState } from '@/composables/useListState'

const router = useRouter()
const { isAdmin } = useAuth()
const { initialSearch, initialExpandedIds, syncToUrl } = useListState()

const events = ref<Event[]>([])
const loading = ref(true)
const search = ref(initialSearch)
const expandedRows = ref<any[]>([])
const expandedCards = ref<Set<number>>(new Set(initialExpandedIds))

onMounted(async () => {
  try {
    events.value = await eventService.getAll()
    expandedRows.value = events.value.filter(e => initialExpandedIds.includes(e.id))
    expandedCards.value = new Set(initialExpandedIds.filter(id => events.value.some(e => e.id === id)))
  } finally {
    loading.value = false
  }
})

watch([search, expandedRows, expandedCards], () => {
  const ids = [...new Set([...expandedRows.value.map((r: any) => r.id), ...expandedCards.value])]
  syncToUrl(search.value, ids)
}, { deep: true })

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
  const result = q ? events.value.filter((e) => fuzzyMatch(q, e)) : [...events.value]
  return result.sort((a, b) => a.event_date.localeCompare(b.event_date))
})

function toggleCard(id: number) {
  if (expandedCards.value.has(id)) expandedCards.value.delete(id)
  else expandedCards.value.add(id)
  // trigger reactivity
  expandedCards.value = new Set(expandedCards.value)
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
      <span v-if="!loading" class="text-xs text-gray-400 shrink-0 whitespace-nowrap">
        {{ filtered.length }} event{{ filtered.length !== 1 ? 's' : '' }}
      </span>
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
      <div class="md:hidden space-y-2">
        <div
          v-for="event in filtered"
          :key="event.id"
          class="bg-white dark:bg-gray-900 rounded-xl border border-gray-200 dark:border-gray-700 overflow-hidden"
        >
          <!-- Card header row -->
          <div class="flex items-start gap-2 p-4">
            <button
              class="flex-1 min-w-0 text-left"
              @click="toggleCard(event.id)"
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
                <div class="flex items-center gap-1 shrink-0 pt-0.5">
                  <span class="text-xs text-gray-400 dark:text-gray-500">
                    {{ formatDate(event.event_date) }}
                  </span>
                  <i :class="['pi text-gray-400 text-xs ml-1', expandedCards.has(event.id) ? 'pi-chevron-up' : 'pi-chevron-down']" />
                </div>
              </div>
            </button>
            <div class="flex shrink-0 -mr-1 -mt-1">
              <Button
                icon="pi pi-eye"
                text
                rounded
                size="small"
                severity="secondary"
                aria-label="View"
                @click="router.push(`/event/${event.id}`)"
              />
              <Button
                v-if="isAdmin"
                icon="pi pi-pencil"
                text
                rounded
                size="small"
                severity="secondary"
                aria-label="Edit"
                @click="router.push(`/event/${event.id}?edit=true`)"
              />
            </div>
          </div>

          <!-- Card expansion -->
          <div
            v-if="expandedCards.has(event.id)"
            class="border-t border-gray-100 dark:border-gray-800 px-4 py-3 space-y-3"
          >
            <!-- Concerts -->
            <div v-if="event.concerts.length" class="space-y-2">
              <div
                v-for="concert in event.concerts"
                :key="concert.id"
                class="space-y-1"
              >
                <p class="text-sm font-medium text-gray-800 dark:text-gray-200">
                  {{ concert.artist?.name ?? '—' }}
                </p>
                <p v-if="concert.comments" class="text-xs text-gray-500 dark:text-gray-400 italic">
                  {{ concert.comments }}
                </p>
                <div v-if="concert.setlist" class="text-xs text-gray-500 dark:text-gray-400 font-mono whitespace-pre-line bg-gray-50 dark:bg-gray-800 rounded px-2 py-1">{{ concert.setlist }}</div>
              </div>
            </div>
            <!-- Venue full -->
            <p class="text-xs text-gray-500 dark:text-gray-400">
              {{ event.venue?.name }}
              <span v-if="event.venue?.city?.name"> · {{ event.venue.city.name }}</span>
              <span v-if="event.venue?.city?.country?.name"> · {{ event.venue.city.country.name }}</span>
            </p>
            <!-- Event comments -->
            <p v-if="event.comments" class="text-xs text-gray-500 dark:text-gray-400 italic">{{ event.comments }}</p>
            <!-- Attendees -->
            <div v-if="event.attendees?.length" class="flex flex-wrap gap-1">
              <span
                v-for="a in event.attendees"
                :key="a.id"
                class="text-xs bg-yellow-100 dark:bg-yellow-900/30 text-yellow-700 dark:text-yellow-300 px-2 py-0.5 rounded-full"
              >
                {{ a.firstname }} {{ a.lastname }}
              </span>
            </div>
          </div>
        </div>
      </div>

      <!-- Desktop table (>= md) -->
      <div class="hidden md:block">
        <DataTable
          :value="filtered"
          v-model:expandedRows="expandedRows"
          row-hover
          size="small"
          sortField="event_date"
          :sortOrder="1"
          class="rounded-xl overflow-hidden border border-gray-200 dark:border-gray-700"
          dataKey="id"
        >
          <Column expander style="width: 2.5rem" />

          <Column field="event_date" header="Date" sortable style="width: 120px">
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

          <Column style="width: 5rem">
            <template #body="{ data }">
              <div class="flex">
                <Button
                  icon="pi pi-eye"
                  text
                  rounded
                  size="small"
                  severity="secondary"
                  aria-label="View"
                  @click="router.push(`/event/${data.id}`)"
                />
                <Button
                  v-if="isAdmin"
                  icon="pi pi-pencil"
                  text
                  rounded
                  size="small"
                  severity="secondary"
                  aria-label="Edit"
                  @click="router.push(`/event/${data.id}?edit=true`)"
                />
              </div>
            </template>
          </Column>

          <template #expansion="{ data }">
            <div class="px-4 py-3 bg-gray-50 dark:bg-gray-800/50 space-y-3">
              <!-- Concerts -->
              <div v-if="data.concerts.length" class="space-y-2">
                <div
                  v-for="concert in data.concerts"
                  :key="concert.id"
                >
                  <span class="text-sm font-medium text-gray-800 dark:text-gray-200">
                    {{ concert.artist?.name ?? '—' }}
                  </span>
                  <span v-if="concert.comments" class="ml-2 text-xs text-gray-500 dark:text-gray-400 italic">{{ concert.comments }}</span>
                  <div v-if="concert.setlist" class="mt-1 text-xs text-gray-500 dark:text-gray-400 font-mono whitespace-pre-line bg-white dark:bg-gray-900 rounded px-2 py-1 border border-gray-100 dark:border-gray-700">{{ concert.setlist }}</div>
                </div>
              </div>

              <!-- Venue + country -->
              <p class="text-xs text-gray-500 dark:text-gray-400">
                <i class="pi pi-map-marker mr-1" />
                {{ data.venue?.name }}
                <span v-if="data.venue?.city?.name"> · {{ data.venue.city.name }}</span>
                <span v-if="data.venue?.city?.country?.name"> · {{ data.venue.city.country.name }}</span>
              </p>

              <!-- Event comments -->
              <p v-if="data.comments" class="text-xs text-gray-500 dark:text-gray-400 italic">
                <i class="pi pi-comment mr-1" />{{ data.comments }}
              </p>

              <!-- Attendees -->
              <div v-if="data.attendees?.length" class="flex flex-wrap gap-1">
                <span
                  v-for="a in data.attendees"
                  :key="a.id"
                  class="text-xs bg-yellow-100 dark:bg-yellow-900/30 text-yellow-700 dark:text-yellow-300 px-2 py-0.5 rounded-full"
                >
                  {{ a.firstname }} {{ a.lastname }}
                </span>
              </div>
            </div>
          </template>
        </DataTable>
      </div>
    </template>
  </div>
</template>
