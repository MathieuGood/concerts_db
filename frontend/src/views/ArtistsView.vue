<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
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

import { artistService } from '@/services/artistService'
import { countryService } from '@/services/countryService'
import { eventService } from '@/services/eventService'
import type { Country } from '@/models/Country'

const router = useRouter()
const confirm = useConfirm()

interface EventEntry {
  id: number; date: string; venue: string; city: string; country: string; festival: string | null
}
interface ArtistRow {
  id: number; name: string; countryName: string; country_id: number | null; country: Country | null
  concerts: number; venues: number; cities: number; countries: number
  firstSeen: string | null; lastSeen: string | null
  events: EventEntry[]; _editing: boolean
}

const loading = ref(true)
const countries = ref<Country[]>([])
const artistRows = ref<ArtistRow[]>([])
const expandedRows = ref<any[]>([])
const editingRows = ref<any[]>([])
const editData = ref<Record<number, any>>({})
const search = ref('')
const addingArtist = ref(false)
const newArtist = ref({ name: '', countryInput: null as Country | null })

onMounted(async () => {
  try {
    const [artists, events, ctrs] = await Promise.all([
      artistService.getAll(), eventService.getAll(), countryService.getAll(),
    ])
    countries.value = ctrs.sort((a, b) => a.name.localeCompare(b.name))

    const statsMap = new Map<number, {
      concerts: number; venueIds: Set<number>; cityIds: Set<number>; countryIds: Set<number>
      firstSeen: string; lastSeen: string; events: EventEntry[]
    }>()

    for (const event of events) {
      for (const concert of event.concerts) {
        if (!concert.artist_id) continue
        if (!statsMap.has(concert.artist_id)) {
          statsMap.set(concert.artist_id, { concerts: 0, venueIds: new Set(), cityIds: new Set(), countryIds: new Set(), firstSeen: event.event_date, lastSeen: event.event_date, events: [] })
        }
        const s = statsMap.get(concert.artist_id)!
        s.concerts++
        if (event.venue_id) s.venueIds.add(event.venue_id)
        if (event.venue?.city?.id) s.cityIds.add(event.venue.city.id)
        if (event.venue?.city?.country_id) s.countryIds.add(event.venue.city.country_id)
        if (event.event_date < s.firstSeen) s.firstSeen = event.event_date
        if (event.event_date > s.lastSeen) s.lastSeen = event.event_date
        s.events.push({ id: event.id, date: event.event_date, venue: event.venue?.name ?? '—', city: event.venue?.city?.name ?? '—', country: event.venue?.city?.country?.name ?? '—', festival: event.festival?.name ?? null })
      }
    }

    artistRows.value = artists.map(a => {
      const s = statsMap.get(a.id)
      return {
        id: a.id, name: a.name, countryName: a.country?.name ?? '', country_id: a.country_id ?? null, country: a.country ?? null,
        concerts: s?.concerts ?? 0, venues: s?.venueIds.size ?? 0, cities: s?.cityIds.size ?? 0, countries: s?.countryIds.size ?? 0,
        firstSeen: s?.firstSeen ?? null, lastSeen: s?.lastSeen ?? null,
        events: s?.events.sort((a, b) => b.date.localeCompare(a.date)) ?? [],
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
  return q ? artistRows.value.filter(a => a.name.toLowerCase().includes(q) || a.countryName.toLowerCase().includes(q)) : artistRows.value
})

function startEdit(row: ArtistRow) {
  editData.value[row.id] = { name: row.name, country_id: row.country_id }
  row._editing = true
}
function cancelEdit(row: ArtistRow) {
  delete editData.value[row.id]
  row._editing = false
}
async function saveRow(data: ArtistRow) {
  await onArtistSave({ newData: { ...data, ...editData.value[data.id] } })
  delete editData.value[data.id]
}

async function onArtistSave(event: any) {
  const { newData } = event
  await artistService.update(newData.id, newData.name, newData.country_id)
  const country = countries.value.find(c => c.id === newData.country_id) ?? null
  const idx = artistRows.value.findIndex(a => a.id === newData.id)
  if (idx !== -1) artistRows.value[idx] = { ...artistRows.value[idx]!, name: newData.name, country_id: newData.country_id, country, countryName: country?.name ?? '', _editing: false }
}

function onArtistDelete(row: ArtistRow) {
  confirm.require({ message: `Delete "${row.name}"?`, header: 'Confirm deletion', icon: 'pi pi-exclamation-triangle', acceptLabel: 'Delete', rejectLabel: 'Cancel',
    accept: async () => { await artistService.delete(row.id); artistRows.value = artistRows.value.filter(a => a.id !== row.id) } })
}

async function resolveCountry(input: Country | string | null): Promise<number | null> {
  if (!input) return null
  const name = typeof input === 'string' ? input.trim() : input.name
  if (!name) return null
  const c = await countryService.findOrCreate(name)
  if (!countries.value.find(x => x.id === c.id)) countries.value.push(c)
  return c.id
}

async function createArtist() {
  if (!newArtist.value.name.trim()) return
  const country_id = await resolveCountry(newArtist.value.countryInput)
  const created = await artistService.create(newArtist.value.name.trim(), country_id)
  const country = countries.value.find(c => c.id === created.country_id) ?? null
  artistRows.value.push({ id: created.id, name: created.name, countryName: country?.name ?? '', country_id: created.country_id ?? null, country, concerts: 0, venues: 0, cities: 0, countries: 0, firstSeen: null, lastSeen: null, events: [], _editing: false })
  newArtist.value = { name: '', countryInput: null }
  addingArtist.value = false
}

// AutoComplete suggestions
const newArtistCountrySuggestions = ref<Country[]>([])
function searchNewArtistCountry(event: { query: string }) {
  const q = event.query.toLowerCase()
  newArtistCountrySuggestions.value = countries.value.filter(c => c.name.toLowerCase().includes(q))
}

const cardCountrySuggestions = ref<Country[]>([])
function searchCardCountry(event: { query: string }) {
  const q = event.query.toLowerCase()
  cardCountrySuggestions.value = countries.value.filter(c => c.name.toLowerCase().includes(q))
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
function startCardEdit(row: ArtistRow) {
  cardEditData.value[row.id] = { name: row.name, countryInput: row.country ?? null }
  editingRows.value = [...editingRows.value, row]
}
function cancelCardEdit(row: ArtistRow) {
  delete cardEditData.value[row.id]
  editingRows.value = editingRows.value.filter((r: any) => r.id !== row.id)
}
async function saveCardEdit(row: ArtistRow) {
  const d = cardEditData.value[row.id]
  const country_id = await resolveCountry(d.countryInput)
  await saveRow({ ...row, name: d.name, country_id })
  delete cardEditData.value[row.id]
}
function deleteFromCard(row: ArtistRow) {
  cancelCardEdit(row)
  onArtistDelete(row)
}
</script>

<template>
  <div>
    <div v-if="loading" class="flex justify-center py-16"><ProgressSpinner style="width:40px;height:40px" /></div>
    <template v-else>
      <div class="flex gap-2 mb-3">
        <IconField class="flex-1"><InputIcon class="pi pi-search" /><InputText v-model="search" placeholder="Search artists…" class="w-full" /></IconField>
        <span class="text-xs text-gray-400 self-center whitespace-nowrap">{{ filtered.length }} artist{{ filtered.length !== 1 ? 's' : '' }}</span>
        <Button icon="pi pi-plus" label="Add" size="small" class="ml-3" @click="addingArtist = !addingArtist" />
      </div>
      <div v-if="addingArtist" class="flex gap-2 mb-3 p-3 bg-gray-50 dark:bg-gray-800 rounded-lg">
        <InputText v-model="newArtist.name" placeholder="Name *" class="flex-1" @keyup.enter="createArtist" />
        <AutoComplete v-model="newArtist.countryInput" :suggestions="newArtistCountrySuggestions" optionLabel="name" placeholder="Country" @complete="searchNewArtistCountry" class="w-40" inputClass="w-full" />
        <Button icon="pi pi-check" size="small" @click="createArtist" :disabled="!newArtist.name.trim()" />
        <Button icon="pi pi-times" size="small" severity="secondary" text @click="addingArtist = false" />
      </div>

      <!-- Mobile card list -->
      <div class="sm:hidden space-y-2">
        <div v-for="row in filtered" :key="row.id"
             class="rounded-xl border border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-900 overflow-hidden">

          <!-- Edit mode -->
          <div v-if="isEditingCard(row.id)" class="p-3 space-y-2 bg-gray-50 dark:bg-gray-800/50">
            <InputText v-model="cardEditData[row.id].name" placeholder="Name *" class="w-full" />
            <AutoComplete v-model="cardEditData[row.id].countryInput" :suggestions="cardCountrySuggestions" optionLabel="name" placeholder="Country" @complete="searchCardCountry" class="w-full" inputClass="w-full" />
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
                    <span class="font-semibold text-d-pink">{{ row.concerts }}</span><span class="text-gray-500">shows</span>
                  </span>
                  <span class="inline-flex items-center gap-1 bg-gray-100 dark:bg-gray-800 px-2 py-0.5 rounded-full text-xs">
                    <span class="font-semibold text-d-pink">{{ row.venues }}</span><span class="text-gray-500">venues</span>
                  </span>
                  <span class="inline-flex items-center gap-1 bg-gray-100 dark:bg-gray-800 px-2 py-0.5 rounded-full text-xs">
                    <span class="font-semibold text-d-pink">{{ row.cities }}</span><span class="text-gray-500">cities</span>
                  </span>
                </div>
                <div v-if="row.firstSeen" class="text-xs text-gray-400 mt-1.5">
                  {{ formatDate(row.firstSeen) }} → {{ formatDate(row.lastSeen) }}
                </div>
              </div>
              <div class="flex items-center gap-0.5 shrink-0 mt-0.5">
                <Button icon="pi pi-pencil" text rounded size="small" severity="secondary" @click.stop="startCardEdit(row)" />
                <i class="pi text-xs text-gray-400 w-5 text-center" :class="isExpanded(row.id) ? 'pi-chevron-up' : 'pi-chevron-down'" />
              </div>
            </div>

            <div v-if="isExpanded(row.id)" class="border-t border-gray-100 dark:border-gray-800">
              <p v-if="row.events.length === 0" class="text-sm text-gray-400 px-4 py-3">No concerts recorded.</p>
              <div v-for="e in row.events" :key="e.id"
                   class="flex items-center gap-2 px-4 py-2.5 border-b border-gray-50 dark:border-gray-800/50 cursor-pointer active:bg-gray-50 dark:active:bg-gray-800/30 last:border-0"
                   @click="router.push(`/event/${e.id}`)">
                <div class="flex-1 min-w-0">
                  <div class="flex items-center gap-2">
                    <span class="text-xs text-gray-500 whitespace-nowrap">{{ formatDate(e.date) }}</span>
                    <span v-if="e.festival" class="text-xs badge-d-red px-1.5 py-0.5 rounded-full truncate">{{ e.festival }}</span>
                  </div>
                  <div class="text-sm truncate">{{ e.venue }}</div>
                  <div class="text-xs text-gray-400 truncate">{{ e.city }}, {{ e.country }}</div>
                </div>
                <i class="pi pi-arrow-right text-xs text-gray-300 shrink-0" />
              </div>
            </div>
          </template>
        </div>
      </div>

      <!-- Desktop table -->
      <div class="hidden sm:block">
        <DataTable :value="filtered" dataKey="id" sortField="concerts" :sortOrder="-1" size="small"
          v-model:expandedRows="expandedRows"
          class="rounded-xl overflow-hidden border border-gray-200 dark:border-gray-700" rowHover>
          <Column expander style="width:3rem" />
          <Column field="name" header="Artist" sortable>
            <template #body="{ data }">
              <InputText v-if="data._editing" v-model="editData[data.id].name" class="w-full" @keyup.enter="saveRow(data)" @keyup.esc="cancelEdit(data)" />
              <span v-else>{{ data.name }}</span>
            </template>
          </Column>
          <Column field="countryName" header="From" sortable style="width:150px">
            <template #body="{ data }">
              <Select v-if="data._editing" v-model="editData[data.id].country_id" :options="countries" optionLabel="name" optionValue="id" showClear placeholder="None" class="w-full" />
              <span v-else>{{ data.country?.name ?? '—' }}</span>
            </template>
          </Column>
          <Column field="concerts" header="Concerts" sortable style="width:90px">
            <template #body="{ data }">
              <span class="font-semibold text-d-pink">{{ data.concerts }}</span>
            </template>
          </Column>
          <Column field="firstSeen" header="First seen" sortable style="width:115px">
            <template #body="{ data }"><span class="text-xs text-gray-500">{{ formatDate(data.firstSeen) }}</span></template>
          </Column>
          <Column field="lastSeen" header="Last seen" sortable style="width:115px">
            <template #body="{ data }"><span class="text-xs text-gray-500">{{ formatDate(data.lastSeen) }}</span></template>
          </Column>
          <Column style="width:5.5rem">
            <template #body="{ data }">
              <div v-if="data._editing" class="flex gap-0.5">
                <Button icon="pi pi-check" text rounded size="small" severity="success" @click="saveRow(data)" />
                <Button icon="pi pi-times" text rounded size="small" severity="secondary" @click="cancelEdit(data)" />
                <Button icon="pi pi-trash" text rounded size="small" severity="danger" @click="onArtistDelete(data)" />
              </div>
              <Button v-else icon="pi pi-pencil" text rounded size="small" severity="secondary" @click="startEdit(data)" />
            </template>
          </Column>

          <template #expansion="{ data }">
            <div class="px-4 py-4">
              <div class="flex flex-wrap gap-2 mb-4">
                <span class="inline-flex items-center gap-1.5 bg-gray-100 dark:bg-gray-800 px-3 py-1 rounded-full text-sm">
                  <span class="font-semibold text-d-pink">{{ data.concerts }}</span><span class="text-gray-500">concerts</span>
                </span>
                <span class="inline-flex items-center gap-1.5 bg-gray-100 dark:bg-gray-800 px-3 py-1 rounded-full text-sm">
                  <span class="font-semibold text-d-pink">{{ data.venues }}</span><span class="text-gray-500">venues</span>
                </span>
                <span class="inline-flex items-center gap-1.5 bg-gray-100 dark:bg-gray-800 px-3 py-1 rounded-full text-sm">
                  <span class="font-semibold text-d-pink">{{ data.cities }}</span><span class="text-gray-500">cities</span>
                </span>
                <span class="inline-flex items-center gap-1.5 bg-gray-100 dark:bg-gray-800 px-3 py-1 rounded-full text-sm">
                  <span class="font-semibold text-d-pink">{{ data.countries }}</span><span class="text-gray-500">countries</span>
                </span>
              </div>
              <p v-if="data.events.length === 0" class="text-sm text-gray-400">No concerts recorded.</p>
              <table v-else class="w-full text-sm">
                <thead><tr class="text-xs text-gray-400 uppercase tracking-wide border-b border-gray-100 dark:border-gray-800">
                  <th class="text-left pb-2 font-medium">Date</th>
                  <th class="text-left pb-2 font-medium">Venue</th>
                  <th class="text-left pb-2 font-medium">City</th>
                  <th class="text-left pb-2 font-medium">Country</th>
                  <th class="text-left pb-2 font-medium">Festival</th>
                  <th class="pb-2"></th>
                </tr></thead>
                <tbody>
                  <tr v-for="e in data.events" :key="e.id"
                    class="border-b border-gray-50 dark:border-gray-800/50 hover:bg-gray-50 dark:hover:bg-gray-800/30 cursor-pointer"
                    @click="router.push(`/event/${e.id}`)">
                    <td class="py-1.5 pr-4 text-gray-500 whitespace-nowrap">{{ formatDate(e.date) }}</td>
                    <td class="py-1.5 pr-4">{{ e.venue }}</td>
                    <td class="py-1.5 pr-4 text-gray-500">{{ e.city }}</td>
                    <td class="py-1.5 pr-4 text-gray-500">{{ e.country }}</td>
                    <td class="py-1.5 pr-4">
                      <span v-if="e.festival" class="text-xs badge-d-red px-2 py-0.5 rounded-full">{{ e.festival }}</span>
                    </td>
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
