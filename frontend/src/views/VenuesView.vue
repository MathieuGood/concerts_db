<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useConfirm } from 'primevue/useconfirm'
import DataTable from 'primevue/datatable'
import Column from 'primevue/column'
import InputText from 'primevue/inputtext'
import Select from 'primevue/select'
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
  eventList: EventEntry[]
}

const loading = ref(true)
const cities = ref<City[]>([])
const countries = ref<Country[]>([])
const venueRows = ref<VenueRow[]>([])
const expandedRows = ref<any[]>([])
const editingRows = ref<any[]>([])
const search = ref('')
const addingVenue = ref(false)
const newVenue = ref({ name: '', city_id: null as number | null })

onMounted(async () => {
  try {
    const [venues, events, cs, ctrs] = await Promise.all([
      venueService.getAll(),
      eventService.getAll(),
      cityService.getAll(),
      countryService.getAll(),
    ])
    cities.value = cs
    countries.value = ctrs

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

function startEdit(row: VenueRow) { editingRows.value = [...editingRows.value, row] }
function cancelEdit(row: VenueRow) { editingRows.value = editingRows.value.filter(r => r.id !== row.id) }
async function saveRow(data: VenueRow) { await onSave({ newData: data }); editingRows.value = editingRows.value.filter(r => r.id !== data.id) }

async function onSave(event: any) {
  const { newData } = event
  await venueService.update(newData.id, newData.name, newData.city_id)
  const city = cities.value.find(c => c.id === newData.city_id) ?? null
  const idx = venueRows.value.findIndex(v => v.id === newData.id)
  if (idx !== -1) venueRows.value[idx] = { ...venueRows.value[idx]!, name: newData.name, city_id: newData.city_id, city, cityName: city?.name ?? '', countryName: city?.country?.name ?? '' }
}

function onDelete(row: VenueRow) {
  confirm.require({ message: `Delete "${row.name}"?`, header: 'Confirm deletion', icon: 'pi pi-exclamation-triangle', acceptLabel: 'Delete', rejectLabel: 'Cancel',
    accept: async () => { await venueService.delete(row.id); venueRows.value = venueRows.value.filter(v => v.id !== row.id) } })
}

async function createVenue() {
  if (!newVenue.value.name.trim() || !newVenue.value.city_id) return
  const created = await venueService.create(newVenue.value.name.trim(), newVenue.value.city_id)
  const city = cities.value.find(c => c.id === created.city_id) ?? null
  venueRows.value.push({ id: created.id, name: created.name, city_id: created.city_id, city, cityName: city?.name ?? '', countryName: city?.country?.name ?? '', events: 0, artists: 0, firstVisit: null, lastVisit: null, eventList: [] })
  newVenue.value = { name: '', city_id: null }
  addingVenue.value = false
}

// Mobile card helpers
const expandedCards = ref<number[]>([])
const cardEditData = ref<Record<number, any>>({})

function isExpanded(id: number) { return expandedCards.value.includes(id) }
function toggleExpand(id: number) {
  const idx = expandedCards.value.indexOf(id)
  if (idx === -1) expandedCards.value.push(id)
  else expandedCards.value.splice(idx, 1)
}
function isEditingCard(id: number) { return editingRows.value.some((r: any) => r.id === id) }
function startCardEdit(row: VenueRow) {
  cardEditData.value[row.id] = { name: row.name, city_id: row.city_id }
  editingRows.value = [...editingRows.value, row]
}
function cancelCardEdit(row: VenueRow) {
  delete cardEditData.value[row.id]
  editingRows.value = editingRows.value.filter((r: any) => r.id !== row.id)
}
async function saveCardEdit(row: VenueRow) {
  const d = cardEditData.value[row.id]
  await saveRow({ ...row, ...d })
  delete cardEditData.value[row.id]
}
function deleteFromCard(row: VenueRow) {
  cancelCardEdit(row)
  onDelete(row)
}
</script>

<template>
  <div>
    <div v-if="loading" class="flex justify-center py-16"><ProgressSpinner style="width:40px;height:40px" /></div>
    <template v-else>
      <div class="flex gap-2 mb-3">
        <IconField class="flex-1"><InputIcon class="pi pi-search" /><InputText v-model="search" placeholder="Search venues…" class="w-full" /></IconField>
        <span class="text-xs text-gray-400 self-center whitespace-nowrap">{{ filtered.length }} venue{{ filtered.length !== 1 ? 's' : '' }}</span>
        <Button icon="pi pi-plus" label="Add" size="small" class="ml-3" @click="addingVenue = !addingVenue" />
      </div>
      <div v-if="addingVenue" class="flex gap-2 mb-3 p-3 bg-gray-50 dark:bg-gray-800 rounded-lg">
        <InputText v-model="newVenue.name" placeholder="Name *" class="flex-1" @keyup.enter="createVenue" />
        <Select v-model="newVenue.city_id" :options="cities" optionLabel="name" optionValue="id" showClear placeholder="City *" filter class="w-48">
          <template #option="{ option }">{{ option.name }}<span class="text-gray-400 text-xs ml-1">({{ option.country?.name }})</span></template>
        </Select>
        <Button icon="pi pi-check" size="small" @click="createVenue" :disabled="!newVenue.name.trim() || !newVenue.city_id" />
        <Button icon="pi pi-times" size="small" severity="secondary" text @click="addingVenue = false" />
      </div>

      <!-- Mobile card list -->
      <div class="sm:hidden space-y-2">
        <div v-for="row in filtered" :key="row.id"
             class="rounded-xl border border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-900 overflow-hidden">

          <!-- Edit mode -->
          <div v-if="isEditingCard(row.id)" class="p-3 space-y-2 bg-gray-50 dark:bg-gray-800/50">
            <InputText v-model="cardEditData[row.id].name" placeholder="Name *" class="w-full" />
            <Select v-model="cardEditData[row.id].city_id" :options="cities" optionLabel="name" optionValue="id" filter placeholder="City *" class="w-full">
              <template #option="{ option }">{{ option.name }}<span class="text-gray-400 text-xs ml-1">({{ option.country?.name }})</span></template>
            </Select>
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
                <div class="text-xs text-gray-500 mt-0.5">{{ row.cityName }}<span v-if="row.countryName">, {{ row.countryName }}</span></div>
                <div class="flex flex-wrap gap-1.5 mt-2">
                  <span class="inline-flex items-center gap-1 bg-gray-100 dark:bg-gray-800 px-2 py-0.5 rounded-full text-xs">
                    <span class="font-semibold text-violet-600 dark:text-violet-400">{{ row.events }}</span><span class="text-gray-500">shows</span>
                  </span>
                  <span class="inline-flex items-center gap-1 bg-gray-100 dark:bg-gray-800 px-2 py-0.5 rounded-full text-xs">
                    <span class="font-semibold text-violet-600 dark:text-violet-400">{{ row.artists }}</span><span class="text-gray-500">artists</span>
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
                    <span v-if="e.festival" class="text-xs bg-violet-100 dark:bg-violet-900/40 text-violet-700 dark:text-violet-300 px-1.5 py-0.5 rounded-full truncate">{{ e.festival }}</span>
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
          v-model:expandedRows="expandedRows" editMode="row" v-model:editingRows="editingRows"
          class="rounded-xl overflow-hidden border border-gray-200 dark:border-gray-700" rowHover>
          <Column expander style="width:3rem" />
          <Column field="name" header="Venue" sortable>
            <template #editor="{ data, field }"><InputText v-model="data[field]" class="w-full" /></template>
          </Column>
          <Column field="cityName" header="City" sortable style="width:140px">
            <template #body="{ data }">{{ data.city?.name ?? '—' }}</template>
            <template #editor="{ data }">
              <Select v-model="data.city_id" :options="cities" optionLabel="name" optionValue="id" filter placeholder="City" class="w-full" />
            </template>
          </Column>
          <Column field="countryName" header="Country" sortable style="width:130px">
            <template #body="{ data }">{{ data.city?.country?.name ?? '—' }}</template>
          </Column>
          <Column field="events" header="Shows" sortable style="width:75px">
            <template #body="{ data }"><span class="font-semibold" :class="data.events > 0 ? 'text-violet-600 dark:text-violet-400' : 'text-gray-400'">{{ data.events || '—' }}</span></template>
          </Column>
          <Column field="firstVisit" header="First visit" sortable style="width:115px">
            <template #body="{ data }"><span class="text-xs text-gray-500">{{ formatDate(data.firstVisit) }}</span></template>
          </Column>
          <Column field="lastVisit" header="Last visit" sortable style="width:115px">
            <template #body="{ data }"><span class="text-xs text-gray-500">{{ formatDate(data.lastVisit) }}</span></template>
          </Column>
          <Column style="width:5.5rem">
            <template #body="{ data }">
              <Button icon="pi pi-pencil" text rounded size="small" severity="secondary" @click="startEdit(data)" />
            </template>
            <template #editor="{ data }">
              <div class="flex gap-0.5">
                <Button icon="pi pi-check" text rounded size="small" severity="success" @click="saveRow(data)" />
                <Button icon="pi pi-times" text rounded size="small" severity="secondary" @click="cancelEdit(data)" />
                <Button icon="pi pi-trash" text rounded size="small" severity="danger" @click="onDelete(data)" />
              </div>
            </template>
          </Column>
          <template #expansion="{ data }">
            <div class="px-4 py-4">
              <div class="flex flex-wrap gap-2 mb-4">
                <span class="inline-flex items-center gap-1.5 bg-gray-100 dark:bg-gray-800 px-3 py-1 rounded-full text-sm">
                  <span class="font-semibold text-violet-600 dark:text-violet-400">{{ data.events }}</span><span class="text-gray-500">events</span>
                </span>
                <span class="inline-flex items-center gap-1.5 bg-gray-100 dark:bg-gray-800 px-3 py-1 rounded-full text-sm">
                  <span class="font-semibold text-violet-600 dark:text-violet-400">{{ data.artists }}</span><span class="text-gray-500">artists</span>
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
                    <td class="py-1.5 pr-4"><span v-if="e.festival" class="text-xs bg-violet-100 dark:bg-violet-900/40 text-violet-700 dark:text-violet-300 px-2 py-0.5 rounded-full">{{ e.festival }}</span></td>
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
