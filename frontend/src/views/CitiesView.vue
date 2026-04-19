<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted, watch } from 'vue'
import { normalize } from '@/utils/search'
import { useRouter } from 'vue-router'
import { useConfirm } from 'primevue/useconfirm'
import { useToast } from 'primevue/usetoast'
import DataTable from 'primevue/datatable'
import Column from 'primevue/column'
import InputText from 'primevue/inputtext'
import Select from 'primevue/select'
import AutoComplete from 'primevue/autocomplete'
import Button from 'primevue/button'
import IconField from 'primevue/iconfield'
import InputIcon from 'primevue/inputicon'
import ProgressSpinner from 'primevue/progressspinner'

import { cityService } from '@/services/cityService'
import { countryService } from '@/services/countryService'
import { eventService } from '@/services/eventService'
import type { Country } from '@/models/Country'
import { useListState } from '@/composables/useListState'

const router = useRouter()
const confirm = useConfirm()
const toast = useToast()

interface EventEntry { id: number; date: string; venue: string; artists: string; festival: string | null }
interface CityRow {
  id: number; name: string; country_id: number; country: Country | null; countryName: string
  events: number; venues: number; artists: number
  firstVisit: string | null; lastVisit: string | null
  eventList: EventEntry[]; _editing: boolean
}

const { initialSearch, initialExpandedIds, syncToUrl } = useListState()

const loading = ref(true)
const countries = ref<Country[]>([])
const cityRows = ref<CityRow[]>([])
const expandedRows = ref<any[]>([])
const expandedCards = ref<number[]>([])
const editingRows = ref<any[]>([])
const editData = ref<Record<number, any>>({})
const search = ref(initialSearch)
const addingCity = ref(false)
const newCity = ref({ name: '', countryInput: null as Country | null })

onMounted(async () => {
  try {
    const [cities, events, ctrs] = await Promise.all([cityService.getAll(), eventService.getAll(), countryService.getAll()])
    countries.value = ctrs.sort((a, b) => a.name.localeCompare(b.name))

    const statsMap = new Map<number, { events: number; venueIds: Set<number>; artistIds: Set<number>; first: string; last: string; eventList: EventEntry[] }>()
    for (const event of events) {
      const cid = event.venue?.city?.id
      if (!cid) continue
      if (!statsMap.has(cid)) statsMap.set(cid, { events: 0, venueIds: new Set(), artistIds: new Set(), first: event.event_date, last: event.event_date, eventList: [] })
      const s = statsMap.get(cid)!
      s.events++
      if (event.venue_id) s.venueIds.add(event.venue_id)
      event.concerts.forEach(c => { if (c.artist_id) s.artistIds.add(c.artist_id) })
      if (event.event_date < s.first) s.first = event.event_date
      if (event.event_date > s.last) s.last = event.event_date
      s.eventList.push({ id: event.id, date: event.event_date, venue: event.venue?.name ?? '—', artists: event.concerts.map(c => c.artist?.name ?? '').filter(Boolean).join(', '), festival: event.festival?.name ?? null })
    }

    cityRows.value = cities.map(c => {
      const s = statsMap.get(c.id)
      return { id: c.id, name: c.name, country_id: c.country_id, country: c.country ?? null, countryName: c.country?.name ?? '', events: s?.events ?? 0, venues: s?.venueIds.size ?? 0, artists: s?.artistIds.size ?? 0, firstVisit: s?.first ?? null, lastVisit: s?.last ?? null, eventList: s?.eventList.sort((a, b) => a.date.localeCompare(b.date)) ?? [], _editing: false }
    })
    expandedRows.value = cityRows.value.filter(r => initialExpandedIds.includes(r.id))
    expandedCards.value = initialExpandedIds.filter(id => cityRows.value.some(r => r.id === id))
  } finally { loading.value = false }
})

watch([search, expandedRows, expandedCards], () => {
  const ids = [...new Set([...expandedRows.value.map((r: any) => r.id), ...expandedCards.value])]
  syncToUrl(search.value, ids)
}, { deep: true })

function formatDate(d: string | null) {
  if (!d) return '—'
  return new Date(d + 'T00:00:00').toLocaleDateString('en-GB', { day: '2-digit', month: 'short', year: 'numeric' })
}

const filtered = computed(() => {
  const q = normalize(search.value)
  return q ? cityRows.value.filter(c => normalize(c.name).includes(q) || normalize(c.countryName).includes(q)) : cityRows.value
})

// ── Infinite scroll ───────────────────────────────────────────────────────────
const PAGE_SIZE = 30
const displayCount = ref(PAGE_SIZE)
const sentinelRef  = ref<HTMLElement | null>(null)
const displayedRows = computed(() => filtered.value.slice(0, displayCount.value))
watch(filtered, () => { displayCount.value = PAGE_SIZE }, { flush: 'sync' })
let _scrollObserver: IntersectionObserver | null = null
watch(sentinelRef, (el) => {
  _scrollObserver?.disconnect()
  if (!el) return
  _scrollObserver = new IntersectionObserver(([entry]) => {
    if (entry?.isIntersecting) displayCount.value += PAGE_SIZE
  }, { rootMargin: '600px' })
  _scrollObserver.observe(el)
})
onUnmounted(() => _scrollObserver?.disconnect())

function startEdit(row: CityRow) {
  editData.value[row.id] = { name: row.name, country_id: row.country_id }
  row._editing = true
}
function cancelEdit(row: CityRow) {
  delete editData.value[row.id]
  row._editing = false
}
async function saveRow(data: CityRow) {
  try {
    await onSave({ newData: { ...data, ...editData.value[data.id] } })
    delete editData.value[data.id]
  } catch (e) {
    toast.add({ severity: 'error', summary: 'Error', detail: e instanceof Error ? e.message : 'An error occurred.', life: 5000 })
  }
}

async function onSave(event: any) {
  const { newData } = event
  await cityService.update(newData.id, newData.name, newData.country_id)
  const country = countries.value.find(c => c.id === newData.country_id) ?? null
  const idx = cityRows.value.findIndex(c => c.id === newData.id)
  if (idx !== -1) cityRows.value[idx] = { ...cityRows.value[idx]!, name: newData.name, country_id: newData.country_id, country, countryName: country?.name ?? '', _editing: false }
}

function onDelete(row: CityRow) {
  confirm.require({ message: `Delete "${row.name}"?`, header: 'Confirm deletion', icon: 'pi pi-exclamation-triangle', acceptLabel: 'Delete', rejectLabel: 'Cancel',
    accept: async () => {
      try {
        await cityService.delete(row.id)
        cityRows.value = cityRows.value.filter(c => c.id !== row.id)
      } catch (e) {
        toast.add({ severity: 'error', summary: 'Error', detail: e instanceof Error ? e.message : 'An error occurred.', life: 5000 })
      }
    } })
}

async function resolveCountry(input: Country | string | null): Promise<number | null> {
  if (!input) return null
  const name = typeof input === 'string' ? input.trim() : input.name
  if (!name) return null
  const c = await countryService.findOrCreate(name)
  if (!countries.value.find(x => x.id === c.id)) countries.value.push(c)
  return c.id
}

async function createCity() {
  if (!newCity.value.name.trim() || !newCity.value.countryInput) return
  try {
    const country_id = await resolveCountry(newCity.value.countryInput)
    if (!country_id) return
    const created = await cityService.create(newCity.value.name.trim(), country_id)
    const country = countries.value.find(c => c.id === created.country_id) ?? null
    cityRows.value.push({ id: created.id, name: created.name, country_id: created.country_id, country, countryName: country?.name ?? '', events: 0, venues: 0, artists: 0, firstVisit: null, lastVisit: null, eventList: [], _editing: false })
    newCity.value = { name: '', countryInput: null }
    addingCity.value = false
  } catch (e) {
    toast.add({ severity: 'error', summary: 'Error', detail: e instanceof Error ? e.message : 'An error occurred.', life: 5000 })
  }
}

// AutoComplete suggestions
const newCityCountrySuggestions = ref<Country[]>([])
function searchNewCityCountry(event: { query: string }) {
  const q = normalize(event.query)
  newCityCountrySuggestions.value = countries.value.filter(c => normalize(c.name).includes(q))
}

const cardCountrySuggestions = ref<Country[]>([])
function searchCardCountry(event: { query: string }) {
  const q = normalize(event.query)
  cardCountrySuggestions.value = countries.value.filter(c => normalize(c.name).includes(q))
}

// Mobile card helpers
const cardEditData = ref<Record<number, any>>({})

function isExpanded(id: number) { return expandedCards.value.includes(id) }
function toggleExpand(id: number) {
  const idx = expandedCards.value.indexOf(id)
  if (idx === -1) expandedCards.value.push(id)
  else expandedCards.value.splice(idx, 1)
}
function isEditingCard(id: number) { return editingRows.value.some((r: any) => r.id === id) }
function startCardEdit(row: CityRow) {
  cardEditData.value[row.id] = { name: row.name, countryInput: row.country ?? null }
  editingRows.value = [...editingRows.value, row]
}
function cancelCardEdit(row: CityRow) {
  delete cardEditData.value[row.id]
  editingRows.value = editingRows.value.filter((r: any) => r.id !== row.id)
}
async function saveCardEdit(row: CityRow) {
  const d = cardEditData.value[row.id]
  const country_id = await resolveCountry(d.countryInput)
  if (!country_id) return
  await saveRow({ ...row, name: d.name, country_id })
  delete cardEditData.value[row.id]
}
function deleteFromCard(row: CityRow) {
  cancelCardEdit(row)
  onDelete(row)
}
</script>

<template>
  <div class="space-y-4">
    <div v-if="loading" class="flex justify-center py-16"><ProgressSpinner style="width:40px;height:40px" /></div>
    <template v-else>
      <div class="flex gap-2">
        <IconField class="flex-1"><InputIcon class="pi pi-search" /><InputText v-model="search" placeholder="Search cities…" class="w-full" /></IconField>
        <span class="text-xs text-gray-400 self-center whitespace-nowrap">{{ filtered.length }} cit{{ filtered.length !== 1 ? 'ies' : 'y' }}</span>
        <Button icon="pi pi-plus" label="Add" size="small" class="ml-3" @click="addingCity = !addingCity" />
      </div>
      <div v-if="addingCity" class="flex gap-2 p-3 bg-gray-50 dark:bg-gray-800 rounded-lg">
        <InputText v-model="newCity.name" placeholder="Name *" class="flex-1" @keyup.enter="createCity" />
        <AutoComplete v-model="newCity.countryInput" :suggestions="newCityCountrySuggestions" optionLabel="name" placeholder="Country *" @complete="searchNewCityCountry" class="w-40" inputClass="w-full" />
        <Button icon="pi pi-check" size="small" @click="createCity" :disabled="!newCity.name.trim() || !newCity.countryInput" />
        <Button icon="pi pi-times" size="small" severity="secondary" text @click="addingCity = false" />
      </div>

      <!-- Mobile card list -->
      <div class="sm:hidden space-y-2">
        <div v-for="row in displayedRows" :key="row.id"
             class="rounded-xl border border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-900 overflow-hidden">

          <!-- Edit mode -->
          <div v-if="isEditingCard(row.id)" class="p-3 space-y-2 bg-gray-50 dark:bg-gray-800/50">
            <InputText v-model="cardEditData[row.id].name" placeholder="Name *" class="w-full" />
            <AutoComplete v-model="cardEditData[row.id].countryInput" :suggestions="cardCountrySuggestions" optionLabel="name" placeholder="Country *" @complete="searchCardCountry" class="w-full" inputClass="w-full" />
            <div class="flex gap-2 pt-1">
              <Button icon="pi pi-check" label="Save" size="small" severity="success" @click="saveCardEdit(row)" class="flex-1" />
              <Button icon="pi pi-times" size="small" severity="secondary" text rounded @click="cancelCardEdit(row)" />
              <Button icon="pi pi-trash" size="small" severity="danger" text rounded @click="deleteFromCard(row)" />
            </div>
          </div>

          <!-- Normal mode -->
          <template v-else>
            <div class="flex items-start p-3 gap-2">
              <div class="flex-1 min-w-0 cursor-pointer" @click="toggleExpand(row.id)">
                <div class="font-medium text-sm">{{ row.name }}</div>
                <div v-if="row.country" class="text-xs text-gray-500 mt-0.5">{{ row.country.name }}</div>
                <div class="flex flex-wrap gap-1.5 mt-2">
                  <span class="inline-flex items-center gap-1 bg-gray-100 dark:bg-gray-800 px-2 py-0.5 rounded-full text-xs">
                    <span class="font-semibold text-d-green">{{ row.events }}</span><span class="text-gray-500">shows</span>
                  </span>
                  <span class="inline-flex items-center gap-1 bg-gray-100 dark:bg-gray-800 px-2 py-0.5 rounded-full text-xs">
                    <span class="font-semibold text-d-green">{{ row.venues }}</span><span class="text-gray-500">venues</span>
                  </span>
                  <span class="inline-flex items-center gap-1 bg-gray-100 dark:bg-gray-800 px-2 py-0.5 rounded-full text-xs">
                    <span class="font-semibold text-d-green">{{ row.artists }}</span><span class="text-gray-500">artists</span>
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
                  <div class="text-sm truncate">{{ e.venue }}</div>
                  <div class="text-xs text-gray-400 truncate">{{ e.artists || '—' }}</div>
                </div>
                <i class="pi pi-arrow-right text-xs text-gray-300 shrink-0" />
              </div>
            </div>
          </template>
        </div>
      </div>

      <!-- Sentinel infinite scroll -->
      <div ref="sentinelRef" class="h-1" />

      <!-- Desktop table -->
      <div class="hidden sm:block">
        <DataTable :value="displayedRows" dataKey="id" sortField="events" :sortOrder="-1" size="small"
          v-model:expandedRows="expandedRows"
          class="rounded-xl overflow-hidden border border-gray-200 dark:border-gray-700" rowHover>
          <Column expander style="width:3rem" />
          <Column field="name" header="City" sortable>
            <template #body="{ data }">
              <InputText v-if="data._editing" v-model="editData[data.id].name" class="w-full" @keyup.enter="saveRow(data)" @keyup.esc="cancelEdit(data)" />
              <span v-else>{{ data.name }}</span>
            </template>
          </Column>
          <Column field="countryName" header="Country" sortable style="width:150px">
            <template #body="{ data }">
              <Select v-if="data._editing" v-model="editData[data.id].country_id" :options="countries" optionLabel="name" optionValue="id" placeholder="Country" class="w-full" />
              <span v-else>{{ data.country?.name ?? '—' }}</span>
            </template>
          </Column>
          <Column field="events" header="Shows" sortable style="width:75px">
            <template #body="{ data }"><span class="font-semibold" :class="data.events > 0 ? 'text-d-green' : 'text-gray-400'">{{ data.events || '—' }}</span></template>
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
                  <span class="font-semibold text-d-green">{{ data.events }}</span><span class="text-gray-500">events</span>
                </span>
                <span class="inline-flex items-center gap-1.5 bg-gray-100 dark:bg-gray-800 px-3 py-1 rounded-full text-sm">
                  <span class="font-semibold text-d-green">{{ data.venues }}</span><span class="text-gray-500">venues</span>
                </span>
                <span class="inline-flex items-center gap-1.5 bg-gray-100 dark:bg-gray-800 px-3 py-1 rounded-full text-sm">
                  <span class="font-semibold text-d-green">{{ data.artists }}</span><span class="text-gray-500">artists</span>
                </span>
              </div>
              <p v-if="data.eventList.length === 0" class="text-sm text-gray-400">No events recorded.</p>
              <table v-else class="w-full text-sm">
                <thead><tr class="text-xs text-gray-400 uppercase tracking-wide border-b border-gray-100 dark:border-gray-800">
                  <th class="text-left pb-2 font-medium">Date</th><th class="text-left pb-2 font-medium">Venue</th><th class="text-left pb-2 font-medium">Artists</th><th class="text-left pb-2 font-medium">Festival</th><th class="pb-2"></th>
                </tr></thead>
                <tbody>
                  <tr v-for="e in data.eventList" :key="e.id" class="border-b border-gray-50 dark:border-gray-800/50 hover:bg-gray-50 dark:hover:bg-gray-800/30 cursor-pointer" @click="router.push(`/event/${e.id}`)">
                    <td class="py-1.5 pr-4 text-gray-500 whitespace-nowrap">{{ formatDate(e.date) }}</td>
                    <td class="py-1.5 pr-4">{{ e.venue }}</td>
                    <td class="py-1.5 pr-4 text-gray-600 dark:text-gray-400">{{ e.artists || '—' }}</td>
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
