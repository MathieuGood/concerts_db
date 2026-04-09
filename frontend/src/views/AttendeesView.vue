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

import { attendeeService } from '@/services/attendeeService'
import { eventService } from '@/services/eventService'

const router = useRouter()
const confirm = useConfirm()

interface EventEntry { id: number; date: string; venue: string; city: string; artists: string; festival: string | null }
interface AttendeeRow {
  id: number; firstname: string; lastname: string | null; fullName: string
  events: number; artists: number
  firstEvent: string | null; lastEvent: string | null
  eventList: EventEntry[]
}

const loading = ref(true)
const attendeeRows = ref<AttendeeRow[]>([])
const expandedRows = ref<any[]>([])
const editingRows = ref<any[]>([])
const search = ref('')
const addingAttendee = ref(false)
const newAttendee = ref({ firstname: '', lastname: '' })

onMounted(async () => {
  try {
    const [attendees, events] = await Promise.all([attendeeService.getAll(), eventService.getAll()])

    const statsMap = new Map<number, { events: number; artistIds: Set<number>; first: string; last: string; eventList: EventEntry[] }>()
    for (const event of events) {
      for (const attendee of event.attendees ?? []) {
        if (!statsMap.has(attendee.id)) statsMap.set(attendee.id, { events: 0, artistIds: new Set(), first: event.event_date, last: event.event_date, eventList: [] })
        const s = statsMap.get(attendee.id)!
        s.events++
        event.concerts.forEach(c => { if (c.artist_id) s.artistIds.add(c.artist_id) })
        if (event.event_date < s.first) s.first = event.event_date
        if (event.event_date > s.last) s.last = event.event_date
        s.eventList.push({ id: event.id, date: event.event_date, venue: event.venue?.name ?? '—', city: event.venue?.city?.name ?? '—', artists: event.concerts.map(c => c.artist?.name ?? '').filter(Boolean).join(', '), festival: event.festival?.name ?? null })
      }
    }

    attendeeRows.value = attendees.map(a => {
      const s = statsMap.get(a.id)
      return { id: a.id, firstname: a.firstname, lastname: a.lastname ?? null, fullName: [a.firstname, a.lastname].filter(Boolean).join(' '), events: s?.events ?? 0, artists: s?.artistIds.size ?? 0, firstEvent: s?.first ?? null, lastEvent: s?.last ?? null, eventList: s?.eventList.sort((a, b) => b.date.localeCompare(a.date)) ?? [] }
    })
  } finally { loading.value = false }
})

function formatDate(d: string | null) {
  if (!d) return '—'
  return new Date(d + 'T00:00:00').toLocaleDateString('en-GB', { day: '2-digit', month: 'short', year: 'numeric' })
}

const filtered = computed(() => {
  const q = search.value.toLowerCase()
  return q ? attendeeRows.value.filter(a => a.fullName.toLowerCase().includes(q)) : attendeeRows.value
})

function startEdit(row: AttendeeRow) { editingRows.value = [...editingRows.value, row] }
function cancelEdit(row: AttendeeRow) { editingRows.value = editingRows.value.filter(r => r.id !== row.id) }
async function saveRow(data: AttendeeRow) { await onSave({ newData: data }); editingRows.value = editingRows.value.filter(r => r.id !== data.id) }

async function onSave(event: any) {
  const { newData } = event
  const updated = await attendeeService.update(newData.id, newData.firstname, newData.lastname)
  const idx = attendeeRows.value.findIndex(a => a.id === updated.id)
  if (idx !== -1) attendeeRows.value[idx] = { ...attendeeRows.value[idx]!, firstname: updated.firstname, lastname: updated.lastname ?? null, fullName: [updated.firstname, updated.lastname].filter(Boolean).join(' ') }
}

function onDelete(row: AttendeeRow) {
  confirm.require({ message: `Delete "${row.fullName}"?`, header: 'Confirm deletion', icon: 'pi pi-exclamation-triangle', acceptLabel: 'Delete', rejectLabel: 'Cancel',
    accept: async () => { await attendeeService.delete(row.id); attendeeRows.value = attendeeRows.value.filter(a => a.id !== row.id) } })
}

async function createAttendee() {
  if (!newAttendee.value.firstname.trim()) return
  const created = await attendeeService.create(newAttendee.value.firstname.trim(), newAttendee.value.lastname.trim() || undefined)
  attendeeRows.value.push({ id: created.id, firstname: created.firstname, lastname: created.lastname ?? null, fullName: [created.firstname, created.lastname].filter(Boolean).join(' '), events: 0, artists: 0, firstEvent: null, lastEvent: null, eventList: [] })
  newAttendee.value = { firstname: '', lastname: '' }
  addingAttendee.value = false
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
function startCardEdit(row: AttendeeRow) {
  cardEditData.value[row.id] = { firstname: row.firstname, lastname: row.lastname }
  editingRows.value = [...editingRows.value, row]
}
function cancelCardEdit(row: AttendeeRow) {
  delete cardEditData.value[row.id]
  editingRows.value = editingRows.value.filter((r: any) => r.id !== row.id)
}
async function saveCardEdit(row: AttendeeRow) {
  const d = cardEditData.value[row.id]
  await saveRow({ ...row, ...d })
  delete cardEditData.value[row.id]
}
function deleteFromCard(row: AttendeeRow) {
  cancelCardEdit(row)
  onDelete(row)
}
</script>

<template>
  <div>
    <div v-if="loading" class="flex justify-center py-16"><ProgressSpinner style="width:40px;height:40px" /></div>
    <template v-else>
      <div class="flex gap-2 mb-3">
        <IconField class="flex-1"><InputIcon class="pi pi-search" /><InputText v-model="search" placeholder="Search people…" class="w-full" /></IconField>
        <span class="text-xs text-gray-400 self-center whitespace-nowrap">{{ filtered.length }} person{{ filtered.length !== 1 ? 's' : '' }}</span>
        <Button icon="pi pi-plus" label="Add" size="small" class="ml-3" @click="addingAttendee = !addingAttendee" />
      </div>
      <div v-if="addingAttendee" class="flex gap-2 mb-3 p-3 bg-gray-50 dark:bg-gray-800 rounded-lg">
        <InputText v-model="newAttendee.firstname" placeholder="First name *" class="flex-1" @keyup.enter="createAttendee" />
        <InputText v-model="newAttendee.lastname" placeholder="Last name" class="flex-1" @keyup.enter="createAttendee" />
        <Button icon="pi pi-check" size="small" @click="createAttendee" :disabled="!newAttendee.firstname.trim()" />
        <Button icon="pi pi-times" size="small" severity="secondary" text @click="addingAttendee = false" />
      </div>

      <!-- Mobile card list -->
      <div class="sm:hidden space-y-2">
        <div v-for="row in filtered" :key="row.id"
             class="rounded-xl border border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-900 overflow-hidden">

          <!-- Edit mode -->
          <div v-if="isEditingCard(row.id)" class="p-3 space-y-2 bg-gray-50 dark:bg-gray-800/50">
            <InputText v-model="cardEditData[row.id].firstname" placeholder="First name *" class="w-full" />
            <InputText v-model="cardEditData[row.id].lastname" placeholder="Last name" class="w-full" />
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
                <div class="font-medium text-sm">{{ row.fullName }}</div>
                <div class="flex flex-wrap gap-1.5 mt-2">
                  <span class="inline-flex items-center gap-1 bg-gray-100 dark:bg-gray-800 px-2 py-0.5 rounded-full text-xs">
                    <span class="font-semibold text-d-yellow">{{ row.events }}</span><span class="text-gray-500">shows</span>
                  </span>
                  <span class="inline-flex items-center gap-1 bg-gray-100 dark:bg-gray-800 px-2 py-0.5 rounded-full text-xs">
                    <span class="font-semibold text-d-yellow">{{ row.artists }}</span><span class="text-gray-500">artists</span>
                  </span>
                </div>
                <div v-if="row.firstEvent" class="text-xs text-gray-400 mt-1.5">
                  {{ formatDate(row.firstEvent) }} → {{ formatDate(row.lastEvent) }}
                </div>
              </div>
              <div class="flex items-center gap-0.5 shrink-0 mt-0.5">
                <Button icon="pi pi-pencil" text rounded size="small" severity="secondary" @click.stop="startCardEdit(row)" />
                <i class="pi text-xs text-gray-400 w-5 text-center" :class="isExpanded(row.id) ? 'pi-chevron-up' : 'pi-chevron-down'" />
              </div>
            </div>

            <div v-if="isExpanded(row.id)" class="border-t border-gray-100 dark:border-gray-800">
              <p v-if="row.eventList.length === 0" class="text-sm text-gray-400 px-4 py-3">No shared events recorded.</p>
              <div v-for="e in row.eventList" :key="e.id"
                   class="flex items-center gap-2 px-4 py-2.5 border-b border-gray-50 dark:border-gray-800/50 cursor-pointer active:bg-gray-50 dark:active:bg-gray-800/30 last:border-0"
                   @click="router.push(`/event/${e.id}`)">
                <div class="flex-1 min-w-0">
                  <div class="flex items-center gap-2">
                    <span class="text-xs text-gray-500 whitespace-nowrap">{{ formatDate(e.date) }}</span>
                    <span v-if="e.festival" class="text-xs badge-d-red px-1.5 py-0.5 rounded-full truncate">{{ e.festival }}</span>
                  </div>
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
          v-model:expandedRows="expandedRows" editMode="row" v-model:editingRows="editingRows"
          class="rounded-xl overflow-hidden border border-gray-200 dark:border-gray-700" rowHover>
          <Column expander style="width:3rem" />
          <Column field="firstname" header="First name" sortable>
            <template #editor="{ data, field }"><InputText v-model="data[field]" class="w-full" /></template>
          </Column>
          <Column field="lastname" header="Last name" sortable>
            <template #body="{ data }">{{ data.lastname ?? '—' }}</template>
            <template #editor="{ data, field }"><InputText v-model="data[field]" class="w-full" /></template>
          </Column>
          <Column field="events" header="Shows" sortable style="width:75px">
            <template #body="{ data }"><span class="font-semibold" :class="data.events > 0 ? 'text-d-yellow' : 'text-gray-400'">{{ data.events || '—' }}</span></template>
          </Column>
          <Column field="firstEvent" header="First event" sortable style="width:115px">
            <template #body="{ data }"><span class="text-xs text-gray-500">{{ formatDate(data.firstEvent) }}</span></template>
          </Column>
          <Column field="lastEvent" header="Last event" sortable style="width:115px">
            <template #body="{ data }"><span class="text-xs text-gray-500">{{ formatDate(data.lastEvent) }}</span></template>
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
                  <span class="font-semibold text-d-yellow">{{ data.events }}</span><span class="text-gray-500">events</span>
                </span>
                <span class="inline-flex items-center gap-1.5 bg-gray-100 dark:bg-gray-800 px-3 py-1 rounded-full text-sm">
                  <span class="font-semibold text-d-yellow">{{ data.artists }}</span><span class="text-gray-500">artists</span>
                </span>
              </div>
              <p v-if="data.eventList.length === 0" class="text-sm text-gray-400">No shared events recorded.</p>
              <table v-else class="w-full text-sm">
                <thead><tr class="text-xs text-gray-400 uppercase tracking-wide border-b border-gray-100 dark:border-gray-800">
                  <th class="text-left pb-2 font-medium">Date</th><th class="text-left pb-2 font-medium">Venue</th><th class="text-left pb-2 font-medium">City</th><th class="text-left pb-2 font-medium">Artists</th><th class="text-left pb-2 font-medium">Festival</th><th class="pb-2"></th>
                </tr></thead>
                <tbody>
                  <tr v-for="e in data.eventList" :key="e.id" class="border-b border-gray-50 dark:border-gray-800/50 hover:bg-gray-50 dark:hover:bg-gray-800/30 cursor-pointer" @click="router.push(`/event/${e.id}`)">
                    <td class="py-1.5 pr-4 text-gray-500 whitespace-nowrap">{{ formatDate(e.date) }}</td>
                    <td class="py-1.5 pr-4">{{ e.venue }}</td>
                    <td class="py-1.5 pr-4 text-gray-500">{{ e.city }}</td>
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
