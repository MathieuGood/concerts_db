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
  eventList: EventEntry[]; _editing: boolean
}

const loading = ref(true)
const festivalRows = ref<FestivalRow[]>([])
const expandedRows = ref<any[]>([])
const editingRows = ref<any[]>([])
const editData = ref<Record<number, any>>({})
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
      return { id: f.id, name: f.name, events: s?.events ?? 0, artists: s?.artistIds.size ?? 0, editions: s?.years.size ?? 0, firstEdition: s?.first ?? null, lastEdition: s?.last ?? null, eventList: s?.eventList.sort((a, b) => b.date.localeCompare(a.date)) ?? [], _editing: false }
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

function startEdit(row: FestivalRow) {
  editData.value[row.id] = { name: row.name }
  row._editing = true
}
function cancelEdit(row: FestivalRow) {
  delete editData.value[row.id]
  row._editing = false
}
async function saveRow(data: FestivalRow) {
  await onSave({ newData: { ...data, ...editData.value[data.id] } })
  delete editData.value[data.id]
}

async function onSave(event: any) {
  const { newData } = event
  await festivalService.update(newData.id, newData.name)
  const idx = festivalRows.value.findIndex(f => f.id === newData.id)
  if (idx !== -1) festivalRows.value[idx] = { ...festivalRows.value[idx]!, name: String(newData.name), _editing: false }
}

function onDelete(row: FestivalRow) {
  confirm.require({ message: `Delete "${row.name}"?`, header: 'Confirm deletion', icon: 'pi pi-exclamation-triangle', acceptLabel: 'Delete', rejectLabel: 'Cancel',
    accept: async () => { await festivalService.delete(row.id); festivalRows.value = festivalRows.value.filter(f => f.id !== row.id) } })
}

async function createFestival() {
  if (!newFestivalName.value.trim()) return
  const created = await festivalService.create(newFestivalName.value.trim())
  festivalRows.value.push({ id: created.id, name: created.name, events: 0, artists: 0, editions: 0, firstEdition: null, lastEdition: null, eventList: [], _editing: false })
  festivalRows.value.sort((a, b) => a.name.localeCompare(b.name))
  newFestivalName.value = ''
  addingFestival.value = false
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
function startCardEdit(row: FestivalRow) {
  cardEditData.value[row.id] = { name: row.name }
  editingRows.value = [...editingRows.value, row]
}
function cancelCardEdit(row: FestivalRow) {
  delete cardEditData.value[row.id]
  editingRows.value = editingRows.value.filter((r: any) => r.id !== row.id)
}
async function saveCardEdit(row: FestivalRow) {
  const d = cardEditData.value[row.id]
  await saveRow({ ...row, ...d })
  delete cardEditData.value[row.id]
}
function deleteFromCard(row: FestivalRow) {
  cancelCardEdit(row)
  onDelete(row)
}
</script>

<template>
  <div class="space-y-4">
    <div v-if="loading" class="flex justify-center py-16"><ProgressSpinner style="width:40px;height:40px" /></div>
    <template v-else>
      <div class="flex gap-2">
        <IconField class="flex-1"><InputIcon class="pi pi-search" /><InputText v-model="search" placeholder="Search festivals…" class="w-full" /></IconField>
        <span class="text-xs text-gray-400 self-center whitespace-nowrap">{{ filtered.length }} festival{{ filtered.length !== 1 ? 's' : '' }}</span>
        <Button icon="pi pi-plus" label="Add" size="small" class="ml-3" @click="addingFestival = !addingFestival" />
      </div>
      <div v-if="addingFestival" class="flex gap-2 p-3 bg-gray-50 dark:bg-gray-800 rounded-lg">
        <InputText v-model="newFestivalName" placeholder="Name *" class="flex-1" @keyup.enter="createFestival" />
        <Button icon="pi pi-check" size="small" @click="createFestival" :disabled="!newFestivalName.trim()" />
        <Button icon="pi pi-times" size="small" severity="secondary" text @click="addingFestival = false" />
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
                    <span class="font-semibold text-d-red">{{ row.events }}</span><span class="text-gray-500">days</span>
                  </span>
                  <span class="inline-flex items-center gap-1 bg-gray-100 dark:bg-gray-800 px-2 py-0.5 rounded-full text-xs">
                    <span class="font-semibold text-d-red">{{ row.editions }}</span><span class="text-gray-500">editions</span>
                  </span>
                  <span class="inline-flex items-center gap-1 bg-gray-100 dark:bg-gray-800 px-2 py-0.5 rounded-full text-xs">
                    <span class="font-semibold text-d-red">{{ row.artists }}</span><span class="text-gray-500">artists</span>
                  </span>
                </div>
                <div v-if="row.firstEdition" class="text-xs text-gray-400 mt-1.5">
                  {{ formatDate(row.firstEdition) }} → {{ formatDate(row.lastEdition) }}
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
                  <div class="text-xs text-gray-500 whitespace-nowrap">{{ formatDate(e.date) }}</div>
                  <div class="text-sm truncate">{{ e.venue }}, {{ e.city }}</div>
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
          v-model:expandedRows="expandedRows"
          class="rounded-xl overflow-hidden border border-gray-200 dark:border-gray-700" rowHover>
          <Column expander style="width:3rem" />
          <Column field="name" header="Festival" sortable>
            <template #body="{ data }">
              <InputText v-if="data._editing" v-model="editData[data.id].name" class="w-full" @keyup.enter="saveRow(data)" @keyup.esc="cancelEdit(data)" />
              <span v-else>{{ data.name }}</span>
            </template>
          </Column>
          <Column field="firstEdition" header="First" sortable style="width:115px">
            <template #body="{ data }"><span class="text-xs text-gray-500">{{ formatDate(data.firstEdition) }}</span></template>
          </Column>
          <Column field="lastEdition" header="Last" sortable style="width:115px">
            <template #body="{ data }"><span class="text-xs text-gray-500">{{ formatDate(data.lastEdition) }}</span></template>
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
                  <span class="font-semibold text-d-red">{{ data.events }}</span><span class="text-gray-500">days</span>
                </span>
                <span class="inline-flex items-center gap-1.5 bg-gray-100 dark:bg-gray-800 px-3 py-1 rounded-full text-sm">
                  <span class="font-semibold text-d-red">{{ data.editions }}</span><span class="text-gray-500">editions</span>
                </span>
                <span class="inline-flex items-center gap-1.5 bg-gray-100 dark:bg-gray-800 px-3 py-1 rounded-full text-sm">
                  <span class="font-semibold text-d-red">{{ data.artists }}</span><span class="text-gray-500">artists</span>
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
      </div>
    </template>
  </div>
</template>
