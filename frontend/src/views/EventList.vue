<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import InputText from 'primevue/inputtext'
import IconField from 'primevue/iconfield'
import InputIcon from 'primevue/inputicon'
import Button from 'primevue/button'
import ProgressSpinner from 'primevue/progressspinner'
import DataTable, { type DataTableRowClickEvent } from 'primevue/datatable'
import Column from 'primevue/column'
import Dialog from 'primevue/dialog'
import SelectButton from 'primevue/selectbutton'
import EventForm from '@/views/EventForm.vue'
import { eventService } from '@/services/eventService'
import { useAuth } from '@/composables/useAuth'
import type { Event } from '@/models/Event'
import { useListState } from '@/composables/useListState'

const route = useRoute()
const router = useRouter()
const { user, isAdmin } = useAuth()

function canEdit(event: Event): boolean {
  return isAdmin.value || event.user_id === user.value?.id
}
const { initialSearch, initialExpandedIds, syncToUrl } = useListState()

const events = ref<Event[]>([])
const loading = ref(true)
const search = ref(initialSearch)
type PlayedFilter = 'all' | 'played' | 'not_played'
const playedFilter = ref<PlayedFilter>('all')
const playedOptions: { icon: string; label: string; value: PlayedFilter }[] = [
  { icon: 'pi pi-bars', label: 'All shows', value: 'all' },
  { icon: 'pi pi-microphone', label: 'I played', value: 'played' },
  { icon: 'pi pi-eye', label: 'Watched', value: 'not_played' },
]
const expandedRows = ref<any[]>([])
const expandedCards = ref<Set<number>>(new Set(initialExpandedIds))

async function fetchEvents() {
  const list = await eventService.getAll()
  events.value = list
  // Reconcile expansion state with the freshly fetched list (IDs may have been added/removed).
  expandedRows.value = list.filter(e => expandedRows.value.some((r: any) => r.id === e.id)
    || initialExpandedIds.includes(e.id))
}

onMounted(async () => {
  try {
    await fetchEvents()
    expandedCards.value = new Set(initialExpandedIds.filter(id => events.value.some(e => e.id === id)))
  } finally {
    loading.value = false
  }
})

// Modal open when route targets an event (/event/new or /event/:id).
const modalOpen = computed({
  get: () => route.path === '/event/new' || !!route.params.id,
  set: (v: boolean) => { if (!v) router.push('/') },
})

// When closing the modal (returning to '/'), refetch to pick up any create/update/delete.
watch(() => route.path, (to, from) => {
  if (from && from !== '/' && to === '/') fetchEvents()
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
  let result = q ? events.value.filter((e) => fuzzyMatch(q, e)) : [...events.value]
  // Keep full event (all concerts) — just gate inclusion based on presence of any played concert.
  if (playedFilter.value === 'played') result = result.filter((e) => e.concerts.some((c) => c.i_played))
  else if (playedFilter.value === 'not_played') result = result.filter((e) => !e.concerts.some((c) => c.i_played))
  return result.sort((a, b) => a.event_date.localeCompare(b.event_date))
})

function toggleCard(id: number) {
  if (expandedCards.value.has(id)) expandedCards.value.delete(id)
  else expandedCards.value.add(id)
  // trigger reactivity
  expandedCards.value = new Set(expandedCards.value)
}

function onRowClick(ev: DataTableRowClickEvent) {
  // Ignore clicks originating from buttons (view/edit action column)
  const target = ev.originalEvent.target as HTMLElement | null
  if (target?.closest('button')) return
  const id = ev.data.id
  const idx = expandedRows.value.findIndex((r: any) => r.id === id)
  if (idx >= 0) expandedRows.value = expandedRows.value.filter((r: any) => r.id !== id)
  else expandedRows.value = [...expandedRows.value, ev.data]
}
</script>

<template>
  <div class="space-y-4">
    <!-- Header row -->
    <div class="flex items-center gap-2">
      <IconField class="flex-1">
        <InputIcon class="pi pi-search" />
        <InputText
          v-model="search"
          placeholder="Search by artist, venue, festival, date…"
          class="w-full"
        />
      </IconField>
      <SelectButton
        v-model="playedFilter"
        :options="playedOptions"
        optionLabel="label"
        optionValue="value"
        :allowEmpty="false"
        size="small"
        class="shrink-0"
        :pt="{ pcToggleButton: { root: { class: '!px-2.5' } } }"
      >
        <template #option="{ option }">
          <i :class="option.icon" v-tooltip.bottom="option.label" />
        </template>
      </SelectButton>
      <span v-if="!loading" class="hidden sm:inline text-xs text-gray-400 shrink-0 whitespace-nowrap">
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
              <div class="min-w-0">
                <div class="flex items-start justify-between gap-2">
                  <p class="font-semibold text-gray-900 dark:text-gray-100 truncate min-w-0">
                    {{ artistNames(event) || event.name || '—' }}
                  </p>
                  <div class="flex items-center gap-1 shrink-0 pt-0.5">
                    <span class="text-xs text-gray-400 dark:text-gray-500">
                      {{ formatDate(event.event_date) }}
                    </span>
                    <i :class="['pi text-gray-400 text-xs ml-1', expandedCards.has(event.id) ? 'pi-chevron-up' : 'pi-chevron-down']" />
                  </div>
                </div>
                <p class="text-sm text-gray-500 dark:text-gray-400 mt-0.5 truncate">
                  {{ event.venue?.name }}<span v-if="event.venue?.city?.name"> — {{ event.venue.city.name }}</span>
                </p>
                <span
                  v-if="event.festival"
                  class="inline-block mt-1 text-xs bg-violet-100 dark:bg-violet-900/40 text-violet-700 dark:text-violet-300 px-2 py-0.5 rounded-full"
                >
                  {{ event.festival.name }}
                </span>
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
          class="rounded-xl overflow-hidden border border-gray-200 dark:border-gray-700 cursor-pointer"
          dataKey="id"
          @row-click="onRowClick"
        >
          <Column style="width: 2.5rem">
            <template #body="{ data }">
              <i
                :class="['pi text-gray-400 text-xs', expandedRows.some((r: any) => r.id === data.id) ? 'pi-chevron-down' : 'pi-chevron-right']"
              />
            </template>
          </Column>

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
                  v-if="canEdit(data)"
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

    <!-- Event view/edit/create modal -->
    <Dialog
      v-model:visible="modalOpen"
      modal
      dismissable-mask
      :draggable="false"
      :show-header="false"
      :style="{ width: '900px' }"
      :breakpoints="{ '960px': '100vw' }"
      :pt="{
        root: { class: 'event-dialog' },
        content: { class: 'p-4 md:p-6' },
      }"
    >
      <EventForm :key="route.fullPath" />
    </Dialog>
  </div>
</template>

<style>
/* Full-screen on mobile (no rounded corners, full height). */
@media (max-width: 960px) {
  .event-dialog {
    max-height: 100vh !important;
    height: 100vh !important;
    border-radius: 0 !important;
    margin: 0 !important;
  }
}
</style>
