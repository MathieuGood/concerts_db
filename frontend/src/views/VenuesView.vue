<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import { useConfirm } from 'primevue/useconfirm'
import DataTable from 'primevue/datatable'
import Column from 'primevue/column'
import InputText from 'primevue/inputtext'
import Select from 'primevue/select'
import AutoComplete from 'primevue/autocomplete'
import Button from 'primevue/button'
import IconField from 'primevue/iconfield'
import InputIcon from 'primevue/inputicon'
import ProgressSpinner from 'primevue/progressspinner'

import { venueService } from '@/services/venueService'
import { cityService } from '@/services/cityService'
import { countryService } from '@/services/countryService'
import { eventService } from '@/services/eventService'
import type { City } from '@/models/City'
import type { Country } from '@/models/Country'

const router = useRouter()
const confirm = useConfirm()

interface EventEntry { id: number; date: string; artists: string; festival: string | null }
interface VenueRow {
  id: number; name: string; city_id: number; city: City | null
  cityName: string; countryName: string
  events: number; artists: number
  firstVisit: string | null; lastVisit: string | null
  eventList: EventEntry[]; _editing: boolean
}

const loading = ref(true)
const cities = ref<City[]>([])
const countries = ref<Country[]>([])
const venueRows = ref<VenueRow[]>([])
const expandedRows = ref<any[]>([])
const editingRows = ref<any[]>([])
const editData = ref<Record<number, any>>({})
const search = ref('')
const addingVenue = ref(false)
const newVenue = ref({ name: '', countryInput: null as Country | null, cityInput: null as City | null })

onMounted(async () => {
  try {
    const [venues, events, cs, ctrs] = await Promise.all([
      venueService.getAll(),
      eventService.getAll(),
      cityService.getAll(),
      countryService.getAll(),
    ])
    cities.value = cs.sort((a, b) => a.name.localeCompare(b.name))
    countries.value = ctrs.sort((a, b) => a.name.localeCompare(b.name))

    const statsMap = new Map<number, { events: number; artistIds: Set<number>; first: string; last: string; eventList: EventEntry[] }>()
    for (const event of events) {
      const vid = event.venue_id
      if (!statsMap.has(vid)) statsMap.set(vid, { events: 0, artistIds: new Set(), first: event.event_date, last: event.event_date, eventList: [] })
      const s = statsMap.get(vid)!
      s.events++
      event.concerts.forEach(c => { if (c.artist_id) s.artistIds.add(c.artist_id) })
      if (event.event_date < s.first) s.first = event.event_date
      if (event.event_date > s.last) s.last = event.event_date
      s.eventList.push({ id: event.id, date: event.event_date, artists: event.concerts.map(c => c.artist?.name ?? '').filter(Boolean).join(', '), festival: event.festival?.name ?? null })
    }

    venueRows.value = venues.map(v => {
      const s = statsMap.get(v.id)
      return {
        id: v.id, name: v.name, city_id: v.city_id, city: v.city ?? null,
        cityName: v.city?.name ?? '', countryName: v.city?.country?.name ?? '',
        events: s?.events ?? 0, artists: s?.artistIds.size ?? 0,
        firstVisit: s?.first ?? null, lastVisit: s?.last ?? null,
        eventList: s?.eventList.sort((a, b) => a.date.localeCompare(b.date)) ?? [],
        _editing: false,
      }
    })
  } finally { loading.value = false }
})

function formatDate(d: string | null) {
  if (!d) return '—'
  return new Date(d + 'T00:00:00').toLocaleDateString('en-GB', { day: '2-digit', month: 'short', year: 'numeric' })
}

const filtered = computed(() => {
  const q = search.value.toLowerCase()
  return q ? venueRows.value.filter(v => v.name.toLowerCase().includes(q) || v.cityName.toLowerCase().includes(q) || v.countryName.toLowerCase().includes(q)) : venueRows.value
})

function startEdit(row: VenueRow) {
  editData.value[row.id] = { name: row.name, city_id: row.city_id }
  row._editing = true
}
function cancelEdit(row: VenueRow) {
  delete editData.value[row.id]
  row._editing = false
}
async function saveRow(data: VenueRow) {
  await onSave({ newData: { ...data, ...editData.value[data.id] } })
  delete editData.value[data.id]
}

async function onSave(event: any) {
  const { newData } = event
  await venueService.update(newData.id, newData.name, newData.city_id)
  const city = cities.value.find(c => c.id === newData.city_id) ?? null
  const idx = venueRows.value.findIndex(v => v.id === newData.id)
  if (idx !== -1) venueRows.value[idx] = { ...venueRows.value[idx]!, name: newData.name, city_id: newData.city_id, city, cityName: city?.name ?? '', countryName: city?.country?.name ?? '', _editing: false }
}

function onDelete(row: VenueRow) {
  confirm.require({ message: `Delete "${row.name}"?`, header: 'Confirm deletion', icon: 'pi pi-exclamation-triangle', acceptLabel: 'Delete', rejectLabel: 'Cancel',
    accept: async () => { await venueService.delete(row.id); venueRows.value = venueRows.value.filter(v => v.id !== row.id) } })
}

// resolve helpers
async function resolveCountry(input: Country | string | null): Promise<number | null> {
  if (!input) return null
  const name = typeof input === 'string' ? input.trim() : input.name
  if (!name) return null
  const c = await countryService.findOrCreate(name)
  if (!countries.value.find(x => x.id === c.id)) countries.value.push(c)
  return c.id
}

async function resolveCity(cityInput: City | string | null, countryId: number | null): Promise<number | null> {
  if (!cityInput) return null
  if (typeof cityInput === 'object' && 'id' in cityInput) return cityInput.id
  const name = (cityInput as string).trim()
  if (!name || !countryId) return null
  const c = await cityService.findOrCreate(name, countryId)
  if (!cities.value.find(x => x.id === c.id)) cities.value.push(c)
  return c.id
}

// Add form — country → city cascade
const newVenueCities = ref<City[]>([])
const newVenueCountrySuggestions = ref<Country[]>([])
const newVenueCitySuggestions = ref<City[]>([])

watch(() => newVenue.value.countryInput, async (val) => {
  newVenue.value.cityInput = null
  if (val && typeof val === 'object' && 'id' in val) {
    newVenueCities.value = (await cityService.getAll(val.id)).sort((a, b) => a.name.localeCompare(b.name))
  } else {
    newVenueCities.value = cities.value
  }
})

function searchNewVenueCountry(event: { query: string }) {
  const q = event.query.toLowerCase()
  newVenueCountrySuggestions.value = countries.value.filter(c => c.name.toLowerCase().includes(q))
}

function searchNewVenueCity(event: { query: string }) {
  const q = event.query.toLowerCase()
  const pool = newVenueCities.value.length ? newVenueCities.value : cities.value
  newVenueCitySuggestions.value = pool.filter(c => c.name.toLowerCase().includes(q))
}

async function createVenue() {
  if (!newVenue.value.name.trim() || !newVenue.value.cityInput) return
  const countryId = await resolveCountry(newVenue.value.countryInput)
  const cityId = await resolveCity(newVenue.value.cityInput, countryId)
  if (!cityId) return
  const created = await venueService.create(newVenue.value.name.trim(), cityId)
  const city = cities.value.find(c => c.id === created.city_id) ?? null
  venueRows.value.push({ id: created.id, name: created.name, city_id: created.city_id, city, cityName: city?.name ?? '', countryName: city?.country?.name ?? '', events: 0, artists: 0, firstVisit: null, lastVisit: null, eventList: [], _editing: false })
  newVenue.value = { name: '', countryInput: null, cityInput: null }
  newVenueCities.value = []
  addingVenue.value = false
}

// Mobile card helpers
const expandedCards = ref<number[]>([])

const activeCardEdit = ref<{ id: number; name: string; countryInput: Country | null; cityInput: City | null; cities: City[] } | null>(null)
const cardCountrySuggestions = ref<Country[]>([])
const cardCitySuggestions = ref<City[]>([])

watch(() => activeCardEdit.value?.countryInput, async (val) => {
  if (!activeCardEdit.value) return
  activeCardEdit.value.cityInput = null
  activeCardEdit.value.cities = []
  if (val && typeof val === 'object' && 'id' in val) {
    activeCardEdit.value.cities = (await cityService.getAll(val.id)).sort((a, b) => a.name.localeCompare(b.name))
  }
})

function searchCardCountry(event: { query: string }) {
  const q = event.query.toLowerCase()
  cardCountrySuggestions.value = countries.value.filter(c => c.name.toLowerCase().includes(q))
}
function searchCardCity(event: { query: string }) {
  if (!activeCardEdit.value) return
  const q = event.query.toLowerCase()
  cardCitySuggestions.value = activeCardEdit.value.cities.filter(c => c.name.toLowerCase().includes(q))
}

function isExpanded(id: number) { return expandedCards.value.includes(id) }
function toggleExpand(id: number) {
  const idx = expandedCards.value.indexOf(id)
  if (idx === -1) expandedCards.value.push(id)
  else expandedCards.value.splice(idx, 1)
}
function isEditingCard(id: number) { return activeCardEdit.value?.id === id }
function startCardEdit(row: VenueRow) {
  activeCardEdit.value = {
    id: row.id, name: row.name,
    countryInput: row.city?.country ?? null,
    cityInput: row.city ?? null,
    cities: []
  }
  // Pre-load cities for current country
  if (row.city?.country?.id) {
    cityService.getAll(row.city.country.id).then(cs => {
      if (activeCardEdit.value?.id === row.id) activeCardEdit.value.cities = cs.sort((a, b) => a.name.localeCompare(b.name))
    })
  }
  editingRows.value = [...editingRows.value.filter((r: any) => r.id !== row.id), row]
}
function cancelCardEdit(row: VenueRow) {
  activeCardEdit.value = null
  editingRows.value = editingRows.value.filter((r: any) => r.id !== row.id)
}
async function saveCardEdit(row: VenueRow) {
  if (!activeCardEdit.value) return
  const countryId = await resolveCountry(activeCardEdit.value.countryInput)
  const cityId = await resolveCity(activeCardEdit.value.cityInput, countryId)
  if (!cityId) return
  await saveRow({ ...row, name: activeCardEdit.value.name, city_id: cityId })
  activeCardEdit.value = null
}
function deleteFromCard(row: VenueRow) {
  cancelCardEdit(row)
  onDelete(row)
}
</script>

<template>
  <div class="space-y-4">
    <div v-if="loading" class="flex justify-center py-16"><ProgressSpinner style="width:40px;height:40px" /></div>
    <template v-else>
      <div class="flex gap-2">
        <IconField class="flex-1"><InputIcon class="pi pi-search" /><InputText v-model="search" placeholder="Search venues…" class="w-full" /></IconField>
        <span class="text-xs text-gray-400 self-center whitespace-nowrap">{{ filtered.length }} venue{{ filtered.length !== 1 ? 's' : '' }}</span>
        <Button icon="pi pi-plus" label="Add" size="small" class="ml-3" @click="addingVenue = !addingVenue" />
      </div>
      <div v-if="addingVenue" class="flex flex-col gap-2 p-3 bg-gray-50 dark:bg-gray-800 rounded-lg">
        <div class="flex gap-2">
          <InputText v-model="newVenue.name" placeholder="Name *" class="flex-1" @keyup.enter="createVenue" />
        </div>
        <div class="flex gap-2">
          <AutoComplete v-model="newVenue.countryInput" :suggestions="newVenueCountrySuggestions" optionLabel="name" placeholder="Country *" @complete="searchNewVenueCountry" class="flex-1" inputClass="w-full" />
          <AutoComplete v-model="newVenue.cityInput" :suggestions="newVenueCitySuggestions" optionLabel="name" placeholder="City *" @complete="searchNewVenueCity" class="flex-1" inputClass="w-full" />
        </div>
        <div class="flex justify-end gap-2">
          <Button icon="pi pi-check" size="small" @click="createVenue" :disabled="!newVenue.name.trim() || !newVenue.cityInput" />
          <Button icon="pi pi-times" size="small" severity="secondary" text @click="addingVenue = false" />
        </div>
      </div>

      <!-- Mobile card list -->
      <div class="sm:hidden space-y-2">
        <div v-for="row in filtered" :key="row.id"
             class="rounded-xl border border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-900 overflow-hidden">

          <!-- Edit mode -->
          <div v-if="isEditingCard(row.id)" class="p-3 space-y-2 bg-gray-50 dark:bg-gray-800/50">
            <InputText v-model="activeCardEdit!.name" placeholder="Name *" class="w-full" />
            <AutoComplete v-model="activeCardEdit!.countryInput" :suggestions="cardCountrySuggestions" optionLabel="name" placeholder="Country *" @complete="searchCardCountry" class="w-full" inputClass="w-full" />
            <AutoComplete v-model="activeCardEdit!.cityInput" :suggestions="cardCitySuggestions" optionLabel="name" placeholder="City *" :disabled="!activeCardEdit?.countryInput" @complete="searchCardCity" class="w-full" inputClass="w-full" />
            <div class="flex gap-2 pt-1">
              <Button icon="pi pi-check" label="Save" size="small" severity="success" @click="saveCardEdit(row)" class="flex-1" :disabled="!activeCardEdit?.cityInput" />
              <Button icon="pi pi-times" size="small" severity="secondary" text rounded @click="cancelCardEdit(row)" />
              <Button icon="pi pi-trash" size="small" severity="danger" text rounded @click="deleteFromCard(row)" />
            </div>
          </div>

          <!-- Normal mode -->
          <template v-else>
            <div class="flex items-start p-3 gap-2">
              <div class="flex-1 min-w-0 cursor-pointer" @click="toggleExpand(row.id)">
                <div class="font-medium text-sm">{{ row.name }}</div>
                <div class="text-xs text-gray-500 mt-0.5">{{ row.cityName }}<span v-if="row.countryName">, {{ row.countryName }}</span></div>
                <div class="flex flex-wrap gap-1.5 mt-2">
                  <span class="inline-flex items-center gap-1 bg-gray-100 dark:bg-gray-800 px-2 py-0.5 rounded-full text-xs">
                    <span class="font-semibold text-d-cyan">{{ row.events }}</span><span class="text-gray-500">shows</span>
                  </span>
                  <span class="inline-flex items-center gap-1 bg-gray-100 dark:bg-gray-800 px-2 py-0.5 rounded-full text-xs">
                    <span class="font-semibold text-d-cyan">{{ row.artists }}</span><span class="text-gray-500">artists</span>
                  </span>
                </div>
                <div v-if="row.firstVisit" class="text-xs text-gray-400 mt-1.5">
                  {{ formatDate(row.firstVisit) }} → {{ formatDate(row.lastVisit) }}
                </div>
              </div>
              <div class="flex items-center gap-0.5 shrink-0 mt-0.5">
                <Button icon="pi pi-pencil" text rounded size="small" severity="secondary" @click.stop="startCardEdit(row)" />
                <i class="pi text-xs text-gray-400 w-5 text-center" :class="isExpanded(row.id) ? 'pi-chevron-up' : 'pi-chevron-down'" />
              </div>
            </div>

            <div v-if="isExpanded(row.id)" class="border-t border-gray-100 dark:border-gray-800">
              <p v-if="row.eventList.length === 0" class="text-sm text-gray-400 px-4 py-3">No events recorded.</p>
              <div v-for="e in row.eventList" :key="e.id"
                   class="flex items-center gap-2 px-4 py-2.5 border-b border-gray-50 dark:border-gray-800/50 cursor-pointer active:bg-gray-50 dark:active:bg-gray-800/30 last:border-0"
                   @click="router.push(`/event/${e.id}`)">
                <div class="flex-1 min-w-0">
                  <div class="flex items-center gap-2">
                    <span class="text-xs text-gray-500 whitespace-nowrap">{{ formatDate(e.date) }}</span>
                    <span v-if="e.festival" class="text-xs badge-d-red px-1.5 py-0.5 rounded-full truncate">{{ e.festival }}</span>
                  </div>
                  <div class="text-sm truncate text-gray-600 dark:text-gray-300">{{ e.artists || '—' }}</div>
                </div>
                <i class="pi pi-arrow-right text-xs text-gray-300 shrink-0" />
              </div>
            </div>
          </template>
        </div>
      </div>

      <!-- Desktop table -->
      <div class="hidden sm:block">
        <DataTable :value="filtered" dataKey="id" sortField="events" :sortOrder="-1" size="small"
          v-model:expandedRows="expandedRows"
          class="rounded-xl overflow-hidden border border-gray-200 dark:border-gray-700" rowHover>
          <Column expander style="width:3rem" />
          <Column field="name" header="Venue" sortable>
            <template #body="{ data }">
              <InputText v-if="data._editing" v-model="editData[data.id].name" class="w-full" @keyup.enter="saveRow(data)" @keyup.esc="cancelEdit(data)" />
              <span v-else>{{ data.name }}</span>
            </template>
          </Column>
          <Column field="cityName" header="City" sortable style="width:140px">
            <template #body="{ data }">
              <Select v-if="data._editing" v-model="editData[data.id].city_id" :options="cities" optionLabel="name" optionValue="id" filter placeholder="City" class="w-full" />
              <span v-else>{{ data.city?.name ?? '—' }}</span>
            </template>
          </Column>
          <Column field="countryName" header="Country" sortable style="width:130px">
            <template #body="{ data }">{{ data.city?.country?.name ?? '—' }}</template>
          </Column>
          <Column field="events" header="Shows" sortable style="width:75px">
            <template #body="{ data }"><span class="font-semibold" :class="data.events > 0 ? 'text-d-cyan' : 'text-gray-400'">{{ data.events || '—' }}</span></template>
          </Column>
          <Column field="firstVisit" header="First visit" sortable style="width:115px">
            <template #body="{ data }"><span class="text-xs text-gray-500">{{ formatDate(data.firstVisit) }}</span></template>
          </Column>
          <Column field="lastVisit" header="Last visit" sortable style="width:115px">
            <template #body="{ data }"><span class="text-xs text-gray-500">{{ formatDate(data.lastVisit) }}</span></template>
          </Column>
          <Column style="width:5.5rem">
            <template #body="{ data }">
              <div v-if="data._editing" class="flex gap-0.5">
                <Button icon="pi pi-check" text rounded size="small" severity="success" @click="saveRow(data)" />
                <Button icon="pi pi-times" text rounded size="small" severity="secondary" @click="cancelEdit(data)" />
                <Button icon="pi pi-trash" text rounded size="small" severity="danger" @click="onDelete(data)" />
              </div>
              <Button v-else icon="pi pi-pencil" text rounded size="small" severity="secondary" @click="startEdit(data)" />
            </template>
          </Column>
          <template #expansion="{ data }">
            <div class="px-4 py-4">
              <div class="flex flex-wrap gap-2 mb-4">
                <span class="inline-flex items-center gap-1.5 bg-gray-100 dark:bg-gray-800 px-3 py-1 rounded-full text-sm">
                  <span class="font-semibold text-d-cyan">{{ data.events }}</span><span class="text-gray-500">events</span>
                </span>
                <span class="inline-flex items-center gap-1.5 bg-gray-100 dark:bg-gray-800 px-3 py-1 rounded-full text-sm">
                  <span class="font-semibold text-d-cyan">{{ data.artists }}</span><span class="text-gray-500">artists</span>
                </span>
              </div>
              <p v-if="data.eventList.length === 0" class="text-sm text-gray-400">No events recorded.</p>
              <table v-else class="w-full text-sm">
                <thead><tr class="text-xs text-gray-400 uppercase tracking-wide border-b border-gray-100 dark:border-gray-800">
                  <th class="text-left pb-2 font-medium">Date</th><th class="text-left pb-2 font-medium">Artists</th><th class="text-left pb-2 font-medium">Festival</th><th class="pb-2"></th>
                </tr></thead>
                <tbody>
                  <tr v-for="e in data.eventList" :key="e.id" class="border-b border-gray-50 dark:border-gray-800/50 hover:bg-gray-50 dark:hover:bg-gray-800/30 cursor-pointer" @click="router.push(`/event/${e.id}`)">
                    <td class="py-1.5 pr-4 text-gray-500 whitespace-nowrap">{{ formatDate(e.date) }}</td>
                    <td class="py-1.5 pr-4">{{ e.artists || '—' }}</td>
                    <td class="py-1.5 pr-4"><span v-if="e.festival" class="text-xs badge-d-red px-2 py-0.5 rounded-full">{{ e.festival }}</span></td>
                    <td class="py-1.5"><i class="pi pi-arrow-right text-xs text-gray-300" /></td>
                  </tr>
                </tbody>
              </table>
            </div>
          </template>
        </DataTable>
      </div>
    </template>
  </div>
</template>
