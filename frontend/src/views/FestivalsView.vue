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

import { festivalService } from '@/services/festivalService'
import { eventService } from '@/services/eventService'

const router = useRouter()
const confirm = useConfirm()

interface EventEntry { id: number; date: string; venue: string; city: string; artists: string }
interface FestivalRow {
  id: number; name: string
  events: number; artists: number; editions: number
  firstEdition: string | null; lastEdition: string | null
  eventList: EventEntry[]
}

const loading = ref(true)
const festivalRows = ref<FestivalRow[]>([])
const expandedRows = ref<any[]>([])
const editingRows = ref<any[]>([])
const search = ref('')
const addingFestival = ref(false)
const newFestivalName = ref('')

onMounted(async () => {
  try {
    const [festivals, events] = await Promise.all([festivalService.getAll(), eventService.getAll()])

    const statsMap = new Map<number, { events: number; artistIds: Set<number>; years: Set<string>; first: string; last: string; eventList: EventEntry[] }>()
    for (const event of events) {
      const fid = event.festival_id
      if (!fid) continue
      if (!statsMap.has(fid)) statsMap.set(fid, { events: 0, artistIds: new Set(), years: new Set(), first: event.event_date, last: event.event_date, eventList: [] })
      const s = statsMap.get(fid)!
      s.events++
      s.years.add(event.event_date.substring(0, 4))
      event.concerts.forEach(c => { if (c.artist_id) s.artistIds.add(c.artist_id) })
      if (event.event_date < s.first) s.first = event.event_date
      if (event.event_date > s.last) s.last = event.event_date
      s.eventList.push({ id: event.id, date: event.event_date, venue: event.venue?.name ?? '—', city: event.venue?.city?.name ?? '—', artists: event.concerts.map(c => c.artist?.name ?? '').filter(Boolean).join(', ') })
    }

    festivalRows.value = festivals.map(f => {
      const s = statsMap.get(f.id)
      return { id: f.id, name: f.name, events: s?.events ?? 0, artists: s?.artistIds.size ?? 0, editions: s?.years.size ?? 0, firstEdition: s?.first ?? null, lastEdition: s?.last ?? null, eventList: s?.eventList.sort((a, b) => b.date.localeCompare(a.date)) ?? [] }
    })
  } finally { loading.value = false }
})

function formatDate(d: string | null) {
  if (!d) return '—'
  return new Date(d + 'T00:00:00').toLocaleDateString('en-GB', { day: '2-digit', month: 'short', year: 'numeric' })
}

const filtered = computed(() => {
  const q = search.value.toLowerCase()
  return q ? festivalRows.value.filter(f => f.name.toLowerCase().includes(q)) : festivalRows.value
})

async function onSave(event: any) {
  const { newData } = event
  await festivalService.update(newData.id, newData.name)
  const idx = festivalRows.value.findIndex(f => f.id === newData.id)
  if (idx !== -1) festivalRows.value[idx] = { ...festivalRows.value[idx]!, name: String(newData.name) }
}

function onDelete(row: FestivalRow) {
  confirm.require({ message: `Delete "${row.name}"?`, header: 'Confirm deletion', icon: 'pi pi-exclamation-triangle', acceptLabel: 'Delete', rejectLabel: 'Cancel',
    accept: async () => { await festivalService.delete(row.id); festivalRows.value = festivalRows.value.filter(f => f.id !== row.id) } })
}

async function createFestival() {
  if (!newFestivalName.value.trim()) return
  const created = await festivalService.create(newFestivalName.value.trim())
  festivalRows.value.push({ id: created.id, name: created.name, events: 0, artists: 0, editions: 0, firstEdition: null, lastEdition: null, eventList: [] })
  festivalRows.value.sort((a, b) => a.name.localeCompare(b.name))
  newFestivalName.value = ''
  addingFestival.value = false
}
</script>

<template>
  <div>
    <div class="flex items-center justify-between mb-6">
      <h2 class="text-xl font-bold text-gray-900 dark:text-gray-100">Festivals</h2>
      <Button icon="pi pi-plus" label="Add festival" size="small" @click="addingFestival = !addingFestival" />
    </div>
    <div v-if="loading" class="flex justify-center py-16"><ProgressSpinner style="width:40px;height:40px" /></div>
    <template v-else>
      <div class="flex gap-2 mb-3">
        <IconField class="flex-1"><InputIcon class="pi pi-search" /><InputText v-model="search" placeholder="Search festivals…" class="w-full" /></IconField>
        <span class="text-xs text-gray-400 self-center whitespace-nowrap">{{ filtered.length }} festival{{ filtered.length !== 1 ? 's' : '' }}</span>
      </div>
      <div v-if="addingFestival" class="flex gap-2 mb-3 p-3 bg-gray-50 dark:bg-gray-800 rounded-lg">
        <InputText v-model="newFestivalName" placeholder="Name *" class="flex-1" @keyup.enter="createFestival" />
        <Button icon="pi pi-check" size="small" @click="createFestival" :disabled="!newFestivalName.trim()" />
        <Button icon="pi pi-times" size="small" severity="secondary" text @click="addingFestival = false" />
      </div>
      <DataTable :value="filtered" dataKey="id" sortField="events" :sortOrder="-1"
        v-model:expandedRows="expandedRows" editMode="row" v-model:editingRows="editingRows" @row-edit-save="onSave"
        class="rounded-xl overflow-hidden border border-gray-200 dark:border-gray-700" rowHover>
        <Column expander style="width:3rem" />
        <Column field="name" header="Festival" sortable>
          <template #editor="{ data, field }"><InputText v-model="data[field]" class="w-full" /></template>
        </Column>
        <Column field="firstEdition" header="First" sortable style="width:115px">
          <template #body="{ data }"><span class="text-xs text-gray-500">{{ formatDate(data.firstEdition) }}</span></template>
        </Column>
        <Column field="lastEdition" header="Last" sortable style="width:115px">
          <template #body="{ data }"><span class="text-xs text-gray-500">{{ formatDate(data.lastEdition) }}</span></template>
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
                <span class="font-semibold text-violet-600 dark:text-violet-400">{{ data.events }}</span><span class="text-gray-500">days</span>
              </span>
              <span class="inline-flex items-center gap-1.5 bg-gray-100 dark:bg-gray-800 px-3 py-1 rounded-full text-sm">
                <span class="font-semibold text-violet-600 dark:text-violet-400">{{ data.editions }}</span><span class="text-gray-500">editions</span>
              </span>
              <span class="inline-flex items-center gap-1.5 bg-gray-100 dark:bg-gray-800 px-3 py-1 rounded-full text-sm">
                <span class="font-semibold text-violet-600 dark:text-violet-400">{{ data.artists }}</span><span class="text-gray-500">artists</span>
              </span>
            </div>
            <p v-if="data.eventList.length === 0" class="text-sm text-gray-400">No events recorded.</p>
            <table v-else class="w-full text-sm">
              <thead><tr class="text-xs text-gray-400 uppercase tracking-wide border-b border-gray-100 dark:border-gray-800">
                <th class="text-left pb-2 font-medium">Date</th><th class="text-left pb-2 font-medium">Venue</th><th class="text-left pb-2 font-medium">City</th><th class="text-left pb-2 font-medium">Artists</th><th class="pb-2"></th>
              </tr></thead>
              <tbody>
                <tr v-for="e in data.eventList" :key="e.id" class="border-b border-gray-50 dark:border-gray-800/50 hover:bg-gray-50 dark:hover:bg-gray-800/30 cursor-pointer" @click="router.push(`/event/${e.id}`)">
                  <td class="py-1.5 pr-4 text-gray-500 whitespace-nowrap">{{ formatDate(e.date) }}</td>
                  <td class="py-1.5 pr-4">{{ e.venue }}</td>
                  <td class="py-1.5 pr-4 text-gray-500">{{ e.city }}</td>
                  <td class="py-1.5 pr-4 text-gray-600 dark:text-gray-400">{{ e.artists || '—' }}</td>
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
