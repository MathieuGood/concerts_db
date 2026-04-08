<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useConfirm } from 'primevue/useconfirm'
import DataTable from 'primevue/datatable'
import Column from 'primevue/column'
import InputText from 'primevue/inputtext'
import Button from 'primevue/button'
import IconField from 'primevue/iconfield'
import InputIcon from 'primevue/inputicon'
import ProgressSpinner from 'primevue/progressspinner'

import { countryService } from '@/services/countryService'
import { eventService } from '@/services/eventService'

const router = useRouter()
const confirm = useConfirm()

interface EventEntry { id: number; date: string; city: string; venue: string; artists: string; festival: string | null }
interface CountryRow {
  id: number; name: string
  events: number; cities: number; venues: number; artists: number
  firstVisit: string | null; lastVisit: string | null
  eventList: EventEntry[]
}

const loading = ref(true)
const countryRows = ref<CountryRow[]>([])
const expandedRows = ref<any[]>([])
const editingRows = ref<any[]>([])
const search = ref('')
const addingCountry = ref(false)
const newCountryName = ref('')

onMounted(async () => {
  try {
    const [countries, events] = await Promise.all([countryService.getAll(), eventService.getAll()])

    const statsMap = new Map<number, { events: number; cityIds: Set<number>; venueIds: Set<number>; artistIds: Set<number>; first: string; last: string; eventList: EventEntry[] }>()
    for (const event of events) {
      const cid = event.venue?.city?.country_id
      if (!cid) continue
      if (!statsMap.has(cid)) statsMap.set(cid, { events: 0, cityIds: new Set(), venueIds: new Set(), artistIds: new Set(), first: event.event_date, last: event.event_date, eventList: [] })
      const s = statsMap.get(cid)!
      s.events++
      if (event.venue?.city?.id) s.cityIds.add(event.venue.city.id)
      if (event.venue_id) s.venueIds.add(event.venue_id)
      event.concerts.forEach(c => { if (c.artist_id) s.artistIds.add(c.artist_id) })
      if (event.event_date < s.first) s.first = event.event_date
      if (event.event_date > s.last) s.last = event.event_date
      s.eventList.push({ id: event.id, date: event.event_date, city: event.venue?.city?.name ?? '—', venue: event.venue?.name ?? '—', artists: event.concerts.map(c => c.artist?.name ?? '').filter(Boolean).join(', '), festival: event.festival?.name ?? null })
    }

    countryRows.value = countries.map(c => {
      const s = statsMap.get(c.id)
      return { id: c.id, name: c.name, events: s?.events ?? 0, cities: s?.cityIds.size ?? 0, venues: s?.venueIds.size ?? 0, artists: s?.artistIds.size ?? 0, firstVisit: s?.first ?? null, lastVisit: s?.last ?? null, eventList: s?.eventList.sort((a, b) => a.date.localeCompare(b.date)) ?? [] }
    })
  } finally { loading.value = false }
})

function formatDate(d: string | null) {
  if (!d) return '—'
  return new Date(d + 'T00:00:00').toLocaleDateString('en-GB', { day: '2-digit', month: 'short', year: 'numeric' })
}

const filtered = computed(() => {
  const q = search.value.toLowerCase()
  return q ? countryRows.value.filter(c => c.name.toLowerCase().includes(q)) : countryRows.value
})

async function onSave(event: any) {
  const { newData } = event
  await countryService.update(newData.id, newData.name)
  const idx = countryRows.value.findIndex(c => c.id === newData.id)
  if (idx !== -1) countryRows.value[idx] = { ...countryRows.value[idx]!, name: String(newData.name) }
}

function onDelete(row: CountryRow) {
  confirm.require({ message: `Delete "${row.name}"?`, header: 'Confirm deletion', icon: 'pi pi-exclamation-triangle', acceptLabel: 'Delete', rejectLabel: 'Cancel',
    accept: async () => { await countryService.delete(row.id); countryRows.value = countryRows.value.filter(c => c.id !== row.id) } })
}

async function createCountry() {
  if (!newCountryName.value.trim()) return
  const created = await countryService.create(newCountryName.value.trim())
  countryRows.value.push({ id: created.id, name: created.name, events: 0, cities: 0, venues: 0, artists: 0, firstVisit: null, lastVisit: null, eventList: [] })
  countryRows.value.sort((a, b) => a.name.localeCompare(b.name))
  newCountryName.value = ''
  addingCountry.value = false
}
</script>

<template>
  <div>
    <div class="flex items-center justify-between mb-6">
      <h2 class="text-xl font-bold text-gray-900 dark:text-gray-100">Countries</h2>
      <Button icon="pi pi-plus" label="Add country" size="small" @click="addingCountry = !addingCountry" />
    </div>
    <div v-if="loading" class="flex justify-center py-16"><ProgressSpinner style="width:40px;height:40px" /></div>
    <template v-else>
      <div class="flex gap-2 mb-3">
        <IconField class="flex-1"><InputIcon class="pi pi-search" /><InputText v-model="search" placeholder="Search countries…" class="w-full" /></IconField>
        <span class="text-xs text-gray-400 self-center whitespace-nowrap">{{ filtered.length }} countr{{ filtered.length !== 1 ? 'ies' : 'y' }}</span>
      </div>
      <div v-if="addingCountry" class="flex gap-2 mb-3 p-3 bg-gray-50 dark:bg-gray-800 rounded-lg">
        <InputText v-model="newCountryName" placeholder="Name *" class="flex-1" @keyup.enter="createCountry" />
        <Button icon="pi pi-check" size="small" @click="createCountry" :disabled="!newCountryName.trim()" />
        <Button icon="pi pi-times" size="small" severity="secondary" text @click="addingCountry = false" />
      </div>
      <DataTable :value="filtered" dataKey="id" sortField="events" :sortOrder="-1"
        v-model:expandedRows="expandedRows" editMode="row" v-model:editingRows="editingRows" @row-edit-save="onSave"
        class="rounded-xl overflow-hidden border border-gray-200 dark:border-gray-700" rowHover>
        <Column expander style="width:3rem" />
        <Column field="name" header="Country" sortable>
          <template #editor="{ data, field }"><InputText v-model="data[field]" class="w-full" /></template>
        </Column>
        <Column field="firstVisit" header="First visit" sortable style="width:115px">
          <template #body="{ data }"><span class="text-xs text-gray-500">{{ formatDate(data.firstVisit) }}</span></template>
        </Column>
        <Column field="lastVisit" header="Last visit" sortable style="width:115px">
          <template #body="{ data }"><span class="text-xs text-gray-500">{{ formatDate(data.lastVisit) }}</span></template>
        </Column>
        <Column :rowEditor="true" style="width:6rem" />
        <Column style="width:3rem">
          <template #body="{ data }">
            <Button v-if="editingRows.find(r => r.id === data.id)" icon="pi pi-trash" text rounded severity="danger" size="small" @click="onDelete(data)" />
          </template>
        </Column>
        <template #expansion="{ data }">
          <div class="px-4 py-4">
            <div class="flex flex-wrap gap-2 mb-4">
              <span class="inline-flex items-center gap-1.5 bg-gray-100 dark:bg-gray-800 px-3 py-1 rounded-full text-sm">
                <span class="font-semibold text-violet-600 dark:text-violet-400">{{ data.events }}</span><span class="text-gray-500">events</span>
              </span>
              <span class="inline-flex items-center gap-1.5 bg-gray-100 dark:bg-gray-800 px-3 py-1 rounded-full text-sm">
                <span class="font-semibold text-violet-600 dark:text-violet-400">{{ data.cities }}</span><span class="text-gray-500">cities</span>
              </span>
              <span class="inline-flex items-center gap-1.5 bg-gray-100 dark:bg-gray-800 px-3 py-1 rounded-full text-sm">
                <span class="font-semibold text-violet-600 dark:text-violet-400">{{ data.venues }}</span><span class="text-gray-500">venues</span>
              </span>
              <span class="inline-flex items-center gap-1.5 bg-gray-100 dark:bg-gray-800 px-3 py-1 rounded-full text-sm">
                <span class="font-semibold text-violet-600 dark:text-violet-400">{{ data.artists }}</span><span class="text-gray-500">artists</span>
              </span>
            </div>
            <p v-if="data.eventList.length === 0" class="text-sm text-gray-400">No events recorded.</p>
            <table v-else class="w-full text-sm">
              <thead><tr class="text-xs text-gray-400 uppercase tracking-wide border-b border-gray-100 dark:border-gray-800">
                <th class="text-left pb-2 font-medium">Date</th><th class="text-left pb-2 font-medium">City</th><th class="text-left pb-2 font-medium">Venue</th><th class="text-left pb-2 font-medium">Artists</th><th class="text-left pb-2 font-medium">Festival</th><th class="pb-2"></th>
              </tr></thead>
              <tbody>
                <tr v-for="e in data.eventList" :key="e.id" class="border-b border-gray-50 dark:border-gray-800/50 hover:bg-gray-50 dark:hover:bg-gray-800/30 cursor-pointer" @click="router.push(`/event/${e.id}`)">
                  <td class="py-1.5 pr-4 text-gray-500 whitespace-nowrap">{{ formatDate(e.date) }}</td>
                  <td class="py-1.5 pr-4">{{ e.city }}</td>
                  <td class="py-1.5 pr-4 text-gray-500">{{ e.venue }}</td>
                  <td class="py-1.5 pr-4 text-gray-600 dark:text-gray-400">{{ e.artists || '—' }}</td>
                  <td class="py-1.5 pr-4"><span v-if="e.festival" class="text-xs bg-violet-100 dark:bg-violet-900/40 text-violet-700 dark:text-violet-300 px-2 py-0.5 rounded-full">{{ e.festival }}</span></td>
                  <td class="py-1.5"><i class="pi pi-arrow-right text-xs text-gray-300" /></td>
                </tr>
              </tbody>
            </table>
          </div>
        </template>
      </DataTable>
    </template>
  </div>
</template>
