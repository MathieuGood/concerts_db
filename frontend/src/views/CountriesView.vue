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

function startEdit(row: CountryRow) { editingRows.value = [...editingRows.value, row] }
function cancelEdit(row: CountryRow) { editingRows.value = editingRows.value.filter(r => r.id !== row.id) }
async function saveRow(data: CountryRow) { await onSave({ newData: data }); editingRows.value = editingRows.value.filter(r => r.id !== data.id) }

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
function startCardEdit(row: CountryRow) {
  cardEditData.value[row.id] = { name: row.name }
  editingRows.value = [...editingRows.value, row]
}
function cancelCardEdit(row: CountryRow) {
  delete cardEditData.value[row.id]
  editingRows.value = editingRows.value.filter((r: any) => r.id !== row.id)
}
async function saveCardEdit(row: CountryRow) {
  const d = cardEditData.value[row.id]
  await saveRow({ ...row, ...d })
  delete cardEditData.value[row.id]
}
function deleteFromCard(row: CountryRow) {
  cancelCardEdit(row)
  onDelete(row)
}
</script>

<template>
  <div>
    <div v-if="loading" class="flex justify-center py-16"><ProgressSpinner style="width:40px;height:40px" /></div>
    <template v-else>
      <div class="flex gap-2 mb-3">
        <IconField class="flex-1"><InputIcon class="pi pi-search" /><InputText v-model="search" placeholder="Search countries…" class="w-full" /></IconField>
        <span class="text-xs text-gray-400 self-center whitespace-nowrap">{{ filtered.length }} countr{{ filtered.length !== 1 ? 'ies' : 'y' }}</span>
        <Button icon="pi pi-plus" label="Add" size="small" class="ml-3" @click="addingCountry = !addingCountry" />
      </div>
      <div v-if="addingCountry" class="flex gap-2 mb-3 p-3 bg-gray-50 dark:bg-gray-800 rounded-lg">
        <InputText v-model="newCountryName" placeholder="Name *" class="flex-1" @keyup.enter="createCountry" />
        <Button icon="pi pi-check" size="small" @click="createCountry" :disabled="!newCountryName.trim()" />
        <Button icon="pi pi-times" size="small" severity="secondary" text @click="addingCountry = false" />
      </div>

      <!-- Mobile card list -->
      <div class="sm:hidden space-y-2">
        <div v-for="row in filtered" :key="row.id"
             class="rounded-xl border border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-900 overflow-hidden">

          <!-- Edit mode -->
          <div v-if="isEditingCard(row.id)" class="p-3 space-y-2 bg-gray-50 dark:bg-gray-800/50">
            <InputText v-model="cardEditData[row.id].name" placeholder="Name *" class="w-full" />
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
                <div class="flex flex-wrap gap-1.5 mt-2">
                  <span class="inline-flex items-center gap-1 bg-gray-100 dark:bg-gray-800 px-2 py-0.5 rounded-full text-xs">
                    <span class="font-semibold text-violet-600 dark:text-violet-400">{{ row.events }}</span><span class="text-gray-500">shows</span>
                  </span>
                  <span class="inline-flex items-center gap-1 bg-gray-100 dark:bg-gray-800 px-2 py-0.5 rounded-full text-xs">
                    <span class="font-semibold text-violet-600 dark:text-violet-400">{{ row.cities }}</span><span class="text-gray-500">cities</span>
                  </span>
                  <span class="inline-flex items-center gap-1 bg-gray-100 dark:bg-gray-800 px-2 py-0.5 rounded-full text-xs">
                    <span class="font-semibold text-violet-600 dark:text-violet-400">{{ row.venues }}</span><span class="text-gray-500">venues</span>
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
                  <div class="text-sm truncate">{{ e.city }} · {{ e.venue }}</div>
                  <div class="text-xs text-gray-400 truncate">{{ e.artists || '—' }}</div>
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
          <Column field="name" header="Country" sortable>
            <template #editor="{ data, field }"><InputText v-model="data[field]" class="w-full" /></template>
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
      </div>
    </template>
  </div>
</template>
