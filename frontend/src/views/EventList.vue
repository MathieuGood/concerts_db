<script setup lang="ts">
import { ref, shallowRef, computed, onMounted, watch } from 'vue'
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
import { normalize } from '@/utils/search'

const route = useRoute()
const router = useRouter()
const { user, isAdmin } = useAuth()

function canEdit(event: Event): boolean {
  return isAdmin.value || event.user_id === user.value?.id
}
const { initialSearch, initialExpandedIds, syncToUrl } = useListState()

// ── Smart search ──────────────────────────────────────────────────────────────
type FilterType = 'festival' | 'artist' | 'city' | 'attendee'
interface ActiveFilter { type: FilterType; id: number; label: string }
interface Suggestion   { id: number; label: string }

const FILTER_CONFIG: Record<FilterType, { icon: string; label: string }> = {
  festival: { icon: 'pi pi-ticket',      label: 'Festival' },
  artist:   { icon: 'pi pi-music',       label: 'Artiste'  },
  city:     { icon: 'pi pi-map-marker',  label: 'Ville'    },
  attendee: { icon: 'pi pi-user',        label: 'Personne' },
}

const activeFilter   = ref<ActiveFilter | null>(null)
const showSuggestions = ref(false)

const suggestions = computed(() => {
  const q = normalize(searchDebounced.value.trim())
  if (q.length < 2) return []

  const festivals = new Map<number, string>()
  const artists   = new Map<number, string>()
  const cities    = new Map<number, string>()
  const attendees = new Map<number, string>()

  for (const event of events.value) {
    if (event.festival) {
      const label = event.festival.name + (event.festival.year ? ` ${event.festival.year}` : '')
      if (normalize(label).includes(q)) festivals.set(event.festival.id, label)
    }
    for (const concert of event.concerts) {
      if (concert.artist?.name && normalize(concert.artist.name).includes(q))
        artists.set(concert.artist.id, concert.artist.name)
    }
    if (event.venue?.city?.name && normalize(event.venue.city.name).includes(q))
      cities.set(event.venue.city.id, event.venue.city.name)
    if (user.value) {
      for (const a of event.attendees ?? []) {
        const label = `${a.firstname} ${a.lastname}`.trim()
        if (normalize(label).includes(q)) attendees.set(a.id, label)
      }
    }
  }

  const toItems = (m: Map<number, string>): Suggestion[] =>
    [...m.entries()].map(([id, label]) => ({ id, label }))

  return ([
    { type: 'festival' as FilterType, items: toItems(festivals) },
    { type: 'artist'   as FilterType, items: toItems(artists)   },
    { type: 'city'     as FilterType, items: toItems(cities)    },
    { type: 'attendee' as FilterType, items: toItems(attendees) },
  ] as { type: FilterType; items: Suggestion[] }[]).filter(g => g.items.length > 0)
})

function applyFilter(type: FilterType, id: number, label: string) {
  activeFilter.value = { type, id, label }
  search.value = ''
  showSuggestions.value = false
}

function onSearchBlur() {
  setTimeout(() => { showSuggestions.value = false }, 150)
}

// ─────────────────────────────────────────────────────────────────────────────

const eventFormRef = ref<InstanceType<typeof EventForm> | null>(null)

// shallowRef : Vue ne proxy pas les objets imbriqués (event→concerts→artist…)
// On ne mutate jamais les events individuellement, on remplace toujours le tableau entier.
const events = shallowRef<Event[]>([])
const loading = ref(true)
const search = ref(initialSearch)
const searchDebounced = ref(initialSearch)

let _debounceTimer: ReturnType<typeof setTimeout> | null = null
watch(search, (val) => {
  if (_debounceTimer) clearTimeout(_debounceTimer)
  _debounceTimer = setTimeout(() => { searchDebounced.value = val }, 200)
})
type PlayedFilter = 'all' | 'played' | 'not_played'
const playedFilter = ref<PlayedFilter>('all')
const playedOptions: { icon: string; label: string; value: PlayedFilter }[] = [
  { icon: 'pi pi-bars', label: 'All shows', value: 'all' },
  { icon: 'pi pi-microphone', label: 'I played', value: 'played' },
  { icon: 'pi pi-eye', label: 'Watched', value: 'not_played' },
]
// PrimeVue v4: expandedRows is Record<string, boolean>, not an array of objects
const expandedRows = ref<Record<string, boolean>>(
  Object.fromEntries(initialExpandedIds.map(id => [String(id), true]))
)
const expandedCards = ref<Set<number>>(new Set(initialExpandedIds))

async function fetchEvents() {
  const list = await eventService.getAll()
  events.value = list
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
  set: (v: boolean) => {
    if (!v) {
      // Block dismiss when EventForm is in edit mode (avoid losing unsaved changes)
      if (eventFormRef.value?.isEditMode) return
      router.push('/')
    }
  },
})

// When closing the modal (returning to '/'), refetch to pick up any create/update/delete.
watch(() => route.path, (to, from) => {
  if (from && from !== '/' && to === '/') fetchEvents()
})

// Reset expansion state when navigating to '/' without expanded param (e.g. navbar click).
watch(() => route.query.expanded, (expanded) => {
  if (!expanded) {
    expandedRows.value = {}
    expandedCards.value = new Set()
  }
})

watch([search, expandedRows, expandedCards], () => {
  const tableIds = Object.entries(expandedRows.value).filter(([, v]) => v).map(([k]) => Number(k))
  const ids = [...new Set([...tableIds, ...expandedCards.value])]
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

// "2011-04-15" → "15042011" pour la recherche par date compacte (ddmmyyyy ou ddmmyy)
function toCompactDate(dateStr: string): string {
  const [y, m, d] = dateStr.split('-')
  return `${d}${m}${y}`
}

function matchesTerm(term: string, e: Event): boolean {
  const artists = e.concerts.map((c) => c.artist?.name ?? '').join(' ')
  const fields = [
    e.name ?? '',
    e.event_date,
    formatDate(e.event_date),
    toCompactDate(e.event_date),
    e.venue?.name ?? '',
    e.venue?.city?.name ?? '',
    e.venue?.city?.country?.name ?? '',
    e.festival?.name ?? '',
    artists,
  ]
  return fields.some((f) => normalize(f).includes(term))
}

// Chaque mot doit être une sous-chaîne d'au moins un champ (ET logique entre mots)
function fuzzyMatch(q: string, e: Event): boolean {
  const terms = normalize(q).split(/\s+/).filter(Boolean)
  return terms.every((term) => matchesTerm(term, e))
}

const filtered = computed(() => {
  let result = [...events.value]

  // Filtre entité exact (festival, artiste, ville, personne)
  if (activeFilter.value) {
    const f = activeFilter.value
    if      (f.type === 'festival') result = result.filter(e => e.festival?.id === f.id)
    else if (f.type === 'artist')   result = result.filter(e => e.concerts.some(c => c.artist?.id === f.id))
    else if (f.type === 'city')     result = result.filter(e => e.venue?.city?.id === f.id)
    else if (f.type === 'attendee') result = result.filter(e => e.attendees?.some(a => a.id === f.id))
  }

  // Recherche texte libre (en plus du filtre actif)
  const q = searchDebounced.value.trim().toLowerCase()
  if (q) result = result.filter(e => fuzzyMatch(q, e))

  if (playedFilter.value === 'played')     result = result.filter(e => e.concerts.some(c => c.i_played))
  else if (playedFilter.value === 'not_played') result = result.filter(e => !e.concerts.some(c => c.i_played))

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
  const id = String(ev.data.id)
  const next = { ...expandedRows.value }
  if (next[id]) delete next[id]
  else next[id] = true
  expandedRows.value = next
}
</script>

<template>
  <div class="space-y-4">
    <!-- Header -->
    <div class="flex flex-col gap-2">
      <!-- Row 1: search + suggestions dropdown -->
      <!-- @focusin/@focusout sur le div : plus fiable que @focus/@blur sur le composant PrimeVue -->
      <div class="relative" @focusin="showSuggestions = true" @focusout="onSearchBlur" @keydown.escape="showSuggestions = false">
        <IconField>
          <InputIcon class="pi pi-search" />
          <InputText
            v-model="search"
            :placeholder="activeFilter ? 'Affiner la recherche…' : 'Rechercher artiste, festival, ville, date…'"
            class="w-full"
          />
        </IconField>

        <!-- Suggestions dropdown -->
        <div
          v-if="showSuggestions && suggestions.length"
          class="absolute z-50 top-full left-0 right-0 mt-1 bg-white dark:bg-gray-900 border border-gray-200 dark:border-gray-700 rounded-xl shadow-lg overflow-hidden"
        >
          <template v-for="group in suggestions" :key="group.type">
            <div class="px-3 py-1.5 text-xs font-semibold text-gray-400 uppercase tracking-wide bg-gray-50 dark:bg-gray-800/50 border-b border-gray-100 dark:border-gray-800">
              <i :class="FILTER_CONFIG[group.type].icon" class="mr-1.5" />{{ FILTER_CONFIG[group.type].label }}
            </div>
            <button
              v-for="item in group.items.slice(0, 4)"
              :key="item.id"
              class="w-full flex items-center px-4 py-2 text-sm text-left hover:bg-gray-50 dark:hover:bg-gray-800 text-gray-800 dark:text-gray-200 transition-colors"
              @mousedown.prevent
              @click="applyFilter(group.type, item.id, item.label)"
            >
              {{ item.label }}
            </button>
          </template>
        </div>
      </div>

      <!-- Row 2: played filter + active filter chip + count + new -->
      <div class="flex items-center gap-2">
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

        <!-- Active filter chip -->
        <span
          v-if="activeFilter"
          class="flex items-center gap-1.5 px-2.5 py-1 rounded-full bg-violet-100 dark:bg-violet-900/40 text-violet-700 dark:text-violet-300 text-xs font-medium shrink-0 max-w-[180px]"
        >
          <i :class="FILTER_CONFIG[activeFilter.type].icon" class="text-xs shrink-0" />
          <span class="truncate">{{ activeFilter.label }}</span>
          <button class="shrink-0 hover:opacity-70" @click="activeFilter = null">
            <i class="pi pi-times text-xs" />
          </button>
        </span>

        <span v-if="!loading" class="flex-1 text-xs text-gray-400 whitespace-nowrap">
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
                  {{ event.festival.name }}{{ event.festival.year ? ` ${event.festival.year}` : '' }}
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
          <Column expander style="width: 2.5rem">
            <template #body="{ data }">
              <i
                :class="['pi text-gray-400 text-xs', expandedRows[String(data.id)] ? 'pi-chevron-down' : 'pi-chevron-right']"
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
                {{ data.festival.name }}{{ data.festival.year ? ` ${data.festival.year}` : '' }}
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
      :style="{ width: '900px', maxHeight: '90vh' }"
      :breakpoints="{ '960px': '100vw' }"
      :pt="{
        root: { class: 'event-dialog' },
        content: { class: 'p-4 md:p-6' },
      }"
    >
      <EventForm ref="eventFormRef" :key="route.fullPath" />
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
