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
import Tag from 'primevue/tag'

import { artistService } from '@/services/artistService'
import { countryService } from '@/services/countryService'
import { eventService } from '@/services/eventService'
import type { Country } from '@/models/Country'
import type { Event } from '@/models/Event'

const router = useRouter()
const confirm = useConfirm()

interface EventEntry {
  id: number
  date: string
  venue: string
  city: string
  country: string
  festival: string | null
}

interface ArtistRow {
  id: number
  name: string
  countryName: string
  country_id: number | null
  country: Country | null
  concerts: number
  venues: number
  cities: number
  countries: number
  firstSeen: string | null
  lastSeen: string | null
  events: EventEntry[]
}

const loading = ref(true)
const countries = ref<Country[]>([])
const artistRows = ref<ArtistRow[]>([])
const expandedRows = ref<any[]>([])
const editingRows = ref<any[]>([])
const search = ref('')
const addingArtist = ref(false)
const newArtist = ref({ name: '', country_id: null as number | null })

onMounted(async () => {
  try {
    const [artists, events, ctrs] = await Promise.all([
      artistService.getAll(),
      eventService.getAll(),
      countryService.getAll(),
    ])
    countries.value = ctrs

    // Build stats per artist from events
    const statsMap = new Map<number, {
      concerts: number
      venueIds: Set<number>
      cityIds: Set<number>
      countryIds: Set<number>
      firstSeen: string
      lastSeen: string
      events: EventEntry[]
    }>()

    for (const event of events) {
      for (const concert of event.concerts) {
        if (!concert.artist_id) continue
        if (!statsMap.has(concert.artist_id)) {
          statsMap.set(concert.artist_id, {
            concerts: 0,
            venueIds: new Set(),
            cityIds: new Set(),
            countryIds: new Set(),
            firstSeen: event.event_date,
            lastSeen: event.event_date,
            events: [],
          })
        }
        const s = statsMap.get(concert.artist_id)!
        s.concerts++
        if (event.venue_id) s.venueIds.add(event.venue_id)
        if (event.venue?.city?.id) s.cityIds.add(event.venue.city.id)
        if (event.venue?.city?.country_id) s.countryIds.add(event.venue.city.country_id)
        if (event.event_date < s.firstSeen) s.firstSeen = event.event_date
        if (event.event_date > s.lastSeen) s.lastSeen = event.event_date
        s.events.push({
          id: event.id,
          date: event.event_date,
          venue: event.venue?.name ?? '—',
          city: event.venue?.city?.name ?? '—',
          country: event.venue?.city?.country?.name ?? '—',
          festival: event.festival?.name ?? null,
        })
      }
    }

    artistRows.value = artists.map((a) => {
      const s = statsMap.get(a.id)
      return {
        id: a.id,
        name: a.name,
        countryName: a.country?.name ?? '',
        country_id: a.country_id ?? null,
        country: a.country ?? null,
        concerts: s?.concerts ?? 0,
        venues: s?.venueIds.size ?? 0,
        cities: s?.cityIds.size ?? 0,
        countries: s?.countryIds.size ?? 0,
        firstSeen: s?.firstSeen ?? null,
        lastSeen: s?.lastSeen ?? null,
        events: s?.events.sort((a, b) => a.date.localeCompare(b.date)) ?? [],
      }
    })
  } finally {
    loading.value = false
  }
})

function formatDate(dateStr: string | null): string {
  if (!dateStr) return '—'
  return new Date(dateStr + 'T00:00:00').toLocaleDateString('en-GB', {
    day: '2-digit', month: 'short', year: 'numeric',
  })
}

const filtered = computed(() => {
  const q = search.value.toLowerCase()
  return q
    ? artistRows.value.filter(a =>
        a.name.toLowerCase().includes(q) || a.countryName.toLowerCase().includes(q)
      )
    : artistRows.value
})

async function onArtistSave(event: any) {
  const { newData } = event
  await artistService.update(newData.id, newData.name, newData.country_id)
  const idx = artistRows.value.findIndex(a => a.id === newData.id)
  if (idx !== -1) {
    const country = countries.value.find(c => c.id === newData.country_id) ?? null
    artistRows.value[idx] = {
      ...artistRows.value[idx]!,
      name: newData.name,
      country_id: newData.country_id,
      country,
      countryName: country?.name ?? '',
    }
  }
}

function onArtistDelete(row: ArtistRow) {
  confirm.require({
    message: `Delete "${row.name}"? This will not delete their concerts.`,
    header: 'Confirm deletion',
    icon: 'pi pi-exclamation-triangle',
    acceptLabel: 'Delete',
    rejectLabel: 'Cancel',
    accept: async () => {
      await artistService.delete(row.id)
      artistRows.value = artistRows.value.filter(a => a.id !== row.id)
    },
  })
}

async function createArtist() {
  if (!newArtist.value.name.trim()) return
  const created = await artistService.create(newArtist.value.name.trim(), newArtist.value.country_id)
  const country = countries.value.find(c => c.id === created.country_id) ?? null
  artistRows.value.push({
    id: created.id,
    name: created.name,
    countryName: country?.name ?? '',
    country_id: created.country_id ?? null,
    country,
    concerts: 0,
    venues: 0,
    cities: 0,
    countries: 0,
    firstSeen: null,
    lastSeen: null,
    events: [],
  })
  newArtist.value = { name: '', country_id: null }
  addingArtist.value = false
}
</script>

<template>
  <div>
    <div class="flex items-center justify-between mb-6">
      <h2 class="text-xl font-bold text-gray-900 dark:text-gray-100">Artists</h2>
      <Button icon="pi pi-plus" label="Add artist" size="small" @click="addingArtist = !addingArtist" />
    </div>

    <div v-if="loading" class="flex justify-center py-16">
      <ProgressSpinner style="width: 40px; height: 40px" />
    </div>

    <template v-else>
      <div class="flex gap-2 mb-3">
        <IconField class="flex-1">
          <InputIcon class="pi pi-search" />
          <InputText v-model="search" placeholder="Search artists…" class="w-full" />
        </IconField>
        <span class="text-xs text-gray-400 self-center whitespace-nowrap">{{ filtered.length }} artist{{ filtered.length !== 1 ? 's' : '' }}</span>
      </div>

      <div v-if="addingArtist" class="flex gap-2 mb-3 p-3 bg-gray-50 dark:bg-gray-800 rounded-lg">
        <InputText v-model="newArtist.name" placeholder="Name *" class="flex-1" @keyup.enter="createArtist" />
        <Select v-model="newArtist.country_id" :options="countries" optionLabel="name" optionValue="id"
          showClear placeholder="Country" class="w-40" />
        <Button icon="pi pi-check" size="small" @click="createArtist" :disabled="!newArtist.name.trim()" />
        <Button icon="pi pi-times" size="small" severity="secondary" text @click="addingArtist = false" />
      </div>

      <DataTable
        :value="filtered"
        dataKey="id"
        sortField="concerts"
        :sortOrder="-1"
        v-model:expandedRows="expandedRows"
        editMode="row"
        v-model:editingRows="editingRows"
        @row-edit-save="onArtistSave"
        class="rounded-xl overflow-hidden border border-gray-200 dark:border-gray-700"
        row-hover
      >
        <Column expander style="width: 3rem" />

        <Column field="name" header="Artist" sortable>
          <template #editor="{ data, field }">
            <InputText v-model="data[field]" class="w-full" />
          </template>
        </Column>

        <Column field="countryName" header="From" sortable style="width: 140px">
          <template #body="{ data }">{{ data.country?.name ?? '—' }}</template>
          <template #editor="{ data }">
            <Select v-model="data.country_id" :options="countries" optionLabel="name" optionValue="id"
              showClear placeholder="None" class="w-full" />
          </template>
        </Column>

        <Column field="concerts" header="Concerts" sortable style="width: 100px" class="text-center">
          <template #body="{ data }">
            <span class="font-semibold" :class="data.concerts > 0 ? 'text-violet-600 dark:text-violet-400' : 'text-gray-400'">
              {{ data.concerts }}
            </span>
          </template>
        </Column>

        <Column field="venues" header="Venues" sortable style="width: 80px" class="text-center">
          <template #body="{ data }">
            <span :class="data.venues > 0 ? '' : 'text-gray-400'">{{ data.venues || '—' }}</span>
          </template>
        </Column>

        <Column field="cities" header="Cities" sortable style="width: 75px" class="text-center">
          <template #body="{ data }">
            <span :class="data.cities > 0 ? '' : 'text-gray-400'">{{ data.cities || '—' }}</span>
          </template>
        </Column>

        <Column field="countries" header="Countries" sortable style="width: 95px" class="text-center">
          <template #body="{ data }">
            <span :class="data.countries > 0 ? '' : 'text-gray-400'">{{ data.countries || '—' }}</span>
          </template>
        </Column>

        <Column field="firstSeen" header="First seen" sortable style="width: 115px">
          <template #body="{ data }">
            <span class="text-xs text-gray-500">{{ formatDate(data.firstSeen) }}</span>
          </template>
        </Column>

        <Column field="lastSeen" header="Last seen" sortable style="width: 115px">
          <template #body="{ data }">
            <span class="text-xs text-gray-500">{{ formatDate(data.lastSeen) }}</span>
          </template>
        </Column>

        <Column :rowEditor="true" style="width: 6rem" />
        <Column style="width: 3rem">
          <template #body="{ data }">
            <Button icon="pi pi-trash" text rounded severity="danger" size="small" @click="onArtistDelete(data)" />
          </template>
        </Column>

        <!-- Expanded event list -->
        <template #expansion="{ data }">
          <div class="px-4 py-3">
            <p v-if="data.events.length === 0" class="text-sm text-gray-400">No concerts recorded.</p>
            <table v-else class="w-full text-sm">
              <thead>
                <tr class="text-xs text-gray-400 uppercase tracking-wide border-b border-gray-100 dark:border-gray-800">
                  <th class="text-left pb-2 font-medium">Date</th>
                  <th class="text-left pb-2 font-medium">Venue</th>
                  <th class="text-left pb-2 font-medium">City</th>
                  <th class="text-left pb-2 font-medium">Country</th>
                  <th class="text-left pb-2 font-medium">Festival</th>
                  <th class="text-left pb-2 font-medium"></th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="e in data.events" :key="e.id"
                  class="border-b border-gray-50 dark:border-gray-800/50 hover:bg-gray-50 dark:hover:bg-gray-800/30 cursor-pointer"
                  @click="router.push(`/event/${e.id}`)">
                  <td class="py-1.5 pr-4 text-gray-600 dark:text-gray-400 whitespace-nowrap">{{ formatDate(e.date) }}</td>
                  <td class="py-1.5 pr-4">{{ e.venue }}</td>
                  <td class="py-1.5 pr-4 text-gray-500">{{ e.city }}</td>
                  <td class="py-1.5 pr-4 text-gray-500">{{ e.country }}</td>
                  <td class="py-1.5 pr-4">
                    <span v-if="e.festival" class="text-xs bg-violet-100 dark:bg-violet-900/40 text-violet-700 dark:text-violet-300 px-2 py-0.5 rounded-full">
                      {{ e.festival }}
                    </span>
                  </td>
                  <td class="py-1.5">
                    <i class="pi pi-arrow-right text-xs text-gray-300" />
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </template>
      </DataTable>
    </template>
  </div>
</template>
