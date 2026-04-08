<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useConfirm } from 'primevue/useconfirm'
import Tabs from 'primevue/tabs'
import TabList from 'primevue/tablist'
import Tab from 'primevue/tab'
import TabPanels from 'primevue/tabpanels'
import TabPanel from 'primevue/tabpanel'
import DataTable from 'primevue/datatable'
import Column from 'primevue/column'
import InputText from 'primevue/inputtext'
import Select from 'primevue/select'
import Button from 'primevue/button'
import IconField from 'primevue/iconfield'
import InputIcon from 'primevue/inputicon'

import { countryService } from '@/services/countryService'
import { cityService } from '@/services/cityService'
import { artistService } from '@/services/artistService'
import { venueService } from '@/services/venueService'
import { attendeeService } from '@/services/attendeeService'
import { festivalService } from '@/services/festivalService'

import type { Country } from '@/models/Country'
import type { City } from '@/models/City'
import type { Artist } from '@/models/Artist'
import type { Venue } from '@/models/Venue'
import type { Attendee } from '@/models/Attendee'
import type { Festival } from '@/models/Festival'

const confirm = useConfirm()

// ── Data ──────────────────────────────────────────────────────────────
const countries = ref<Country[]>([])
const cities = ref<City[]>([])
const artists = ref<Artist[]>([])
const venues = ref<Venue[]>([])
const attendees = ref<Attendee[]>([])
const festivals = ref<Festival[]>([])
const loading = ref(true)

// ── Search ────────────────────────────────────────────────────────────
const countryQ = ref('')
const cityQ = ref('')
const artistQ = ref('')
const venueQ = ref('')
const attendeeQ = ref('')
const festivalQ = ref('')

// ── Editing rows ──────────────────────────────────────────────────────
const countryEditing = ref<any[]>([])
const cityEditing = ref<any[]>([])
const artistEditing = ref<any[]>([])
const venueEditing = ref<any[]>([])
const attendeeEditing = ref<any[]>([])
const festivalEditing = ref<any[]>([])

// ── New item forms ────────────────────────────────────────────────────
const addingCountry = ref(false)
const addingCity = ref(false)
const addingArtist = ref(false)
const addingVenue = ref(false)
const addingAttendee = ref(false)
const addingFestival = ref(false)

const newCountry = ref({ name: '' })
const newCity = ref({ name: '', country_id: null as number | null })
const newArtist = ref({ name: '', country_id: null as number | null })
const newVenue = ref({ name: '', city_id: null as number | null })
const newAttendee = ref({ firstname: '', lastname: '' })
const newFestival = ref({ name: '' })

// ── Filtered ──────────────────────────────────────────────────────────
const filteredCountries = computed(() => {
  const q = countryQ.value.toLowerCase()
  return q ? countries.value.filter(c => c.name.toLowerCase().includes(q)) : countries.value
})
const filteredCities = computed(() => {
  const q = cityQ.value.toLowerCase()
  return q ? cities.value.filter(c =>
    c.name.toLowerCase().includes(q) || c.country?.name.toLowerCase().includes(q)
  ) : cities.value
})
const filteredArtists = computed(() => {
  const q = artistQ.value.toLowerCase()
  return q ? artists.value.filter(a =>
    a.name.toLowerCase().includes(q) || (a.country?.name ?? '').toLowerCase().includes(q)
  ) : artists.value
})
const filteredVenues = computed(() => {
  const q = venueQ.value.toLowerCase()
  return q ? venues.value.filter(v =>
    v.name.toLowerCase().includes(q) ||
    (v.city?.name ?? '').toLowerCase().includes(q) ||
    (v.city?.country?.name ?? '').toLowerCase().includes(q)
  ) : venues.value
})
const filteredAttendees = computed(() => {
  const q = attendeeQ.value.toLowerCase()
  return q ? attendees.value.filter(a =>
    a.firstname.toLowerCase().includes(q) || (a.lastname ?? '').toLowerCase().includes(q)
  ) : attendees.value
})
const filteredFestivals = computed(() => {
  const q = festivalQ.value.toLowerCase()
  return q ? festivals.value.filter(f => f.name.toLowerCase().includes(q)) : festivals.value
})

// ── Load ──────────────────────────────────────────────────────────────
onMounted(async () => {
  try {
    const [c, ci, a, v, at, f] = await Promise.all([
      countryService.getAll(),
      cityService.getAll(),
      artistService.getAll(),
      venueService.getAll(),
      attendeeService.getAll(),
      festivalService.getAll(),
    ])
    countries.value = c
    cities.value = ci
    artists.value = a
    venues.value = v
    attendees.value = at
    festivals.value = f
  } finally {
    loading.value = false
  }
})

// ── Delete helper ─────────────────────────────────────────────────────
function confirmDelete(label: string, onAccept: () => Promise<void>) {
  confirm.require({
    message: `Delete "${label}"?`,
    header: 'Confirm deletion',
    icon: 'pi pi-exclamation-triangle',
    acceptLabel: 'Delete',
    rejectLabel: 'Cancel',
    acceptSeverity: 'danger',
    accept: onAccept,
  })
}

// ── Countries ─────────────────────────────────────────────────────────
async function onCountrySave(event: any) {
  const { newData } = event
  await countryService.update(newData.id, newData.name)
  const idx = countries.value.findIndex(c => c.id === newData.id)
  if (idx !== -1) countries.value[idx] = { ...countries.value[idx], name: newData.name }
}
function onCountryDelete(row: Country) {
  confirmDelete(row.name, async () => {
    await countryService.delete(row.id)
    countries.value = countries.value.filter(c => c.id !== row.id)
  })
}
async function createCountry() {
  if (!newCountry.value.name.trim()) return
  const created = await countryService.create(newCountry.value.name.trim())
  countries.value = [...countries.value, created].sort((a, b) => a.name.localeCompare(b.name))
  newCountry.value = { name: '' }
  addingCountry.value = false
}

// ── Cities ────────────────────────────────────────────────────────────
async function onCitySave(event: any) {
  const { newData } = event
  await cityService.update(newData.id, newData.name, newData.country_id)
  cities.value = await cityService.getAll()
}
function onCityDelete(row: City) {
  confirmDelete(row.name, async () => {
    await cityService.delete(row.id)
    cities.value = cities.value.filter(c => c.id !== row.id)
  })
}
async function createCity() {
  if (!newCity.value.name.trim() || !newCity.value.country_id) return
  await cityService.create(newCity.value.name.trim(), newCity.value.country_id)
  cities.value = await cityService.getAll()
  newCity.value = { name: '', country_id: null }
  addingCity.value = false
}

// ── Artists ───────────────────────────────────────────────────────────
async function onArtistSave(event: any) {
  const { newData } = event
  await artistService.update(newData.id, newData.name, newData.country_id)
  artists.value = await artistService.getAll()
}
function onArtistDelete(row: Artist) {
  confirmDelete(row.name, async () => {
    await artistService.delete(row.id)
    artists.value = artists.value.filter(a => a.id !== row.id)
  })
}
async function createArtist() {
  if (!newArtist.value.name.trim()) return
  await artistService.create(newArtist.value.name.trim(), newArtist.value.country_id)
  artists.value = await artistService.getAll()
  newArtist.value = { name: '', country_id: null }
  addingArtist.value = false
}

// ── Venues ────────────────────────────────────────────────────────────
async function onVenueSave(event: any) {
  const { newData } = event
  await venueService.update(newData.id, newData.name, newData.city_id)
  venues.value = await venueService.getAll()
}
function onVenueDelete(row: Venue) {
  confirmDelete(row.name, async () => {
    await venueService.delete(row.id)
    venues.value = venues.value.filter(v => v.id !== row.id)
  })
}
async function createVenue() {
  if (!newVenue.value.name.trim() || !newVenue.value.city_id) return
  await venueService.create(newVenue.value.name.trim(), newVenue.value.city_id)
  venues.value = await venueService.getAll()
  newVenue.value = { name: '', city_id: null }
  addingVenue.value = false
}

// ── Attendees ─────────────────────────────────────────────────────────
async function onAttendeeSave(event: any) {
  const { newData } = event
  const updated = await attendeeService.update(newData.id, newData.firstname, newData.lastname)
  const idx = attendees.value.findIndex(a => a.id === updated.id)
  if (idx !== -1) attendees.value[idx] = updated
}
function onAttendeeDelete(row: Attendee) {
  confirmDelete(`${row.firstname} ${row.lastname ?? ''}`.trim(), async () => {
    await attendeeService.delete(row.id)
    attendees.value = attendees.value.filter(a => a.id !== row.id)
  })
}
async function createAttendee() {
  if (!newAttendee.value.firstname.trim()) return
  const created = await attendeeService.create(
    newAttendee.value.firstname.trim(),
    newAttendee.value.lastname.trim() || undefined,
  )
  attendees.value = [...attendees.value, created]
  newAttendee.value = { firstname: '', lastname: '' }
  addingAttendee.value = false
}

// ── Festivals ─────────────────────────────────────────────────────────
async function onFestivalSave(event: any) {
  const { newData } = event
  await festivalService.update(newData.id, newData.name)
  const idx = festivals.value.findIndex(f => f.id === newData.id)
  if (idx !== -1) festivals.value[idx] = { ...festivals.value[idx], name: newData.name }
}
function onFestivalDelete(row: Festival) {
  confirmDelete(row.name, async () => {
    await festivalService.delete(row.id)
    festivals.value = festivals.value.filter(f => f.id !== row.id)
  })
}
async function createFestival() {
  if (!newFestival.value.name.trim()) return
  const created = await festivalService.create(newFestival.value.name.trim())
  festivals.value = [...festivals.value, created].sort((a, b) => a.name.localeCompare(b.name))
  newFestival.value = { name: '' }
  addingFestival.value = false
}
</script>

<template>
  <div>
    <h2 class="text-xl font-bold mb-6 text-gray-900 dark:text-gray-100">Library</h2>

    <div v-if="loading" class="text-gray-400 text-sm py-8 text-center">Loading…</div>

    <Tabs v-else value="artists">
      <TabList>
        <Tab value="artists">Artists ({{ artists.length }})</Tab>
        <Tab value="venues">Venues ({{ venues.length }})</Tab>
        <Tab value="cities">Cities ({{ cities.length }})</Tab>
        <Tab value="countries">Countries ({{ countries.length }})</Tab>
        <Tab value="attendees">Attendees ({{ attendees.length }})</Tab>
        <Tab value="festivals">Festivals ({{ festivals.length }})</Tab>
      </TabList>

      <TabPanels>

        <!-- ── ARTISTS ── -->
        <TabPanel value="artists">
          <div class="flex gap-2 mb-3 mt-4">
            <IconField class="flex-1">
              <InputIcon class="pi pi-search" />
              <InputText v-model="artistQ" placeholder="Search artists…" class="w-full" />
            </IconField>
            <Button icon="pi pi-plus" label="Add" size="small" @click="addingArtist = !addingArtist" />
          </div>

          <div v-if="addingArtist" class="flex gap-2 mb-3 p-3 bg-gray-50 dark:bg-gray-800 rounded-lg">
            <InputText v-model="newArtist.name" placeholder="Name *" class="flex-1" @keyup.enter="createArtist" />
            <Select v-model="newArtist.country_id" :options="countries" optionLabel="name" optionValue="id"
              showClear placeholder="Country" class="w-40" />
            <Button icon="pi pi-check" size="small" @click="createArtist" :disabled="!newArtist.name.trim()" />
            <Button icon="pi pi-times" size="small" severity="secondary" text @click="addingArtist = false" />
          </div>

          <DataTable :value="filteredArtists" dataKey="id" editMode="row"
            v-model:editingRows="artistEditing" @row-edit-save="onArtistSave"
            class="rounded-xl overflow-hidden border border-gray-200 dark:border-gray-700">
            <Column field="name" header="Name">
              <template #editor="{ data, field }">
                <InputText v-model="data[field]" class="w-full" />
              </template>
            </Column>
            <Column header="Country" style="width: 180px">
              <template #body="{ data }">{{ data.country?.name ?? '—' }}</template>
              <template #editor="{ data }">
                <Select v-model="data.country_id" :options="countries" optionLabel="name" optionValue="id"
                  showClear placeholder="None" class="w-full" />
              </template>
            </Column>
            <Column :rowEditor="true" style="width: 6rem" />
            <Column style="width: 3rem">
              <template #body="{ data }">
                <Button icon="pi pi-trash" text rounded severity="danger" size="small" @click="onArtistDelete(data)" />
              </template>
            </Column>
          </DataTable>
        </TabPanel>

        <!-- ── VENUES ── -->
        <TabPanel value="venues">
          <div class="flex gap-2 mb-3 mt-4">
            <IconField class="flex-1">
              <InputIcon class="pi pi-search" />
              <InputText v-model="venueQ" placeholder="Search venues…" class="w-full" />
            </IconField>
            <Button icon="pi pi-plus" label="Add" size="small" @click="addingVenue = !addingVenue" />
          </div>

          <div v-if="addingVenue" class="flex gap-2 mb-3 p-3 bg-gray-50 dark:bg-gray-800 rounded-lg">
            <InputText v-model="newVenue.name" placeholder="Name *" class="flex-1" @keyup.enter="createVenue" />
            <Select v-model="newVenue.city_id" :options="cities" optionLabel="name" optionValue="id"
              showClear placeholder="City *" filter class="w-48"
              :optionGroupLabel="undefined">
              <template #option="{ option }">
                {{ option.name }}<span class="text-gray-400 text-xs ml-1">({{ option.country?.name }})</span>
              </template>
            </Select>
            <Button icon="pi pi-check" size="small" @click="createVenue" :disabled="!newVenue.name.trim() || !newVenue.city_id" />
            <Button icon="pi pi-times" size="small" severity="secondary" text @click="addingVenue = false" />
          </div>

          <DataTable :value="filteredVenues" dataKey="id" editMode="row"
            v-model:editingRows="venueEditing" @row-edit-save="onVenueSave"
            class="rounded-xl overflow-hidden border border-gray-200 dark:border-gray-700">
            <Column field="name" header="Name">
              <template #editor="{ data, field }">
                <InputText v-model="data[field]" class="w-full" />
              </template>
            </Column>
            <Column header="City" style="width: 160px">
              <template #body="{ data }">{{ data.city?.name ?? '—' }}</template>
              <template #editor="{ data }">
                <Select v-model="data.city_id" :options="cities" optionLabel="name" optionValue="id"
                  filter placeholder="City" class="w-full" />
              </template>
            </Column>
            <Column header="Country" style="width: 140px">
              <template #body="{ data }">{{ data.city?.country?.name ?? '—' }}</template>
            </Column>
            <Column :rowEditor="true" style="width: 6rem" />
            <Column style="width: 3rem">
              <template #body="{ data }">
                <Button icon="pi pi-trash" text rounded severity="danger" size="small" @click="onVenueDelete(data)" />
              </template>
            </Column>
          </DataTable>
        </TabPanel>

        <!-- ── CITIES ── -->
        <TabPanel value="cities">
          <div class="flex gap-2 mb-3 mt-4">
            <IconField class="flex-1">
              <InputIcon class="pi pi-search" />
              <InputText v-model="cityQ" placeholder="Search cities…" class="w-full" />
            </IconField>
            <Button icon="pi pi-plus" label="Add" size="small" @click="addingCity = !addingCity" />
          </div>

          <div v-if="addingCity" class="flex gap-2 mb-3 p-3 bg-gray-50 dark:bg-gray-800 rounded-lg">
            <InputText v-model="newCity.name" placeholder="Name *" class="flex-1" @keyup.enter="createCity" />
            <Select v-model="newCity.country_id" :options="countries" optionLabel="name" optionValue="id"
              showClear placeholder="Country *" class="w-40" />
            <Button icon="pi pi-check" size="small" @click="createCity" :disabled="!newCity.name.trim() || !newCity.country_id" />
            <Button icon="pi pi-times" size="small" severity="secondary" text @click="addingCity = false" />
          </div>

          <DataTable :value="filteredCities" dataKey="id" editMode="row"
            v-model:editingRows="cityEditing" @row-edit-save="onCitySave"
            class="rounded-xl overflow-hidden border border-gray-200 dark:border-gray-700">
            <Column field="name" header="Name">
              <template #editor="{ data, field }">
                <InputText v-model="data[field]" class="w-full" />
              </template>
            </Column>
            <Column header="Country" style="width: 180px">
              <template #body="{ data }">{{ data.country?.name ?? '—' }}</template>
              <template #editor="{ data }">
                <Select v-model="data.country_id" :options="countries" optionLabel="name" optionValue="id"
                  placeholder="Country" class="w-full" />
              </template>
            </Column>
            <Column :rowEditor="true" style="width: 6rem" />
            <Column style="width: 3rem">
              <template #body="{ data }">
                <Button icon="pi pi-trash" text rounded severity="danger" size="small" @click="onCityDelete(data)" />
              </template>
            </Column>
          </DataTable>
        </TabPanel>

        <!-- ── COUNTRIES ── -->
        <TabPanel value="countries">
          <div class="flex gap-2 mb-3 mt-4">
            <IconField class="flex-1">
              <InputIcon class="pi pi-search" />
              <InputText v-model="countryQ" placeholder="Search countries…" class="w-full" />
            </IconField>
            <Button icon="pi pi-plus" label="Add" size="small" @click="addingCountry = !addingCountry" />
          </div>

          <div v-if="addingCountry" class="flex gap-2 mb-3 p-3 bg-gray-50 dark:bg-gray-800 rounded-lg">
            <InputText v-model="newCountry.name" placeholder="Name *" class="flex-1" @keyup.enter="createCountry" />
            <Button icon="pi pi-check" size="small" @click="createCountry" :disabled="!newCountry.name.trim()" />
            <Button icon="pi pi-times" size="small" severity="secondary" text @click="addingCountry = false" />
          </div>

          <DataTable :value="filteredCountries" dataKey="id" editMode="row"
            v-model:editingRows="countryEditing" @row-edit-save="onCountrySave"
            class="rounded-xl overflow-hidden border border-gray-200 dark:border-gray-700">
            <Column field="name" header="Name">
              <template #editor="{ data, field }">
                <InputText v-model="data[field]" class="w-full" />
              </template>
            </Column>
            <Column :rowEditor="true" style="width: 6rem" />
            <Column style="width: 3rem">
              <template #body="{ data }">
                <Button icon="pi pi-trash" text rounded severity="danger" size="small" @click="onCountryDelete(data)" />
              </template>
            </Column>
          </DataTable>
        </TabPanel>

        <!-- ── ATTENDEES ── -->
        <TabPanel value="attendees">
          <div class="flex gap-2 mb-3 mt-4">
            <IconField class="flex-1">
              <InputIcon class="pi pi-search" />
              <InputText v-model="attendeeQ" placeholder="Search attendees…" class="w-full" />
            </IconField>
            <Button icon="pi pi-plus" label="Add" size="small" @click="addingAttendee = !addingAttendee" />
          </div>

          <div v-if="addingAttendee" class="flex gap-2 mb-3 p-3 bg-gray-50 dark:bg-gray-800 rounded-lg">
            <InputText v-model="newAttendee.firstname" placeholder="First name *" class="flex-1" @keyup.enter="createAttendee" />
            <InputText v-model="newAttendee.lastname" placeholder="Last name" class="flex-1" @keyup.enter="createAttendee" />
            <Button icon="pi pi-check" size="small" @click="createAttendee" :disabled="!newAttendee.firstname.trim()" />
            <Button icon="pi pi-times" size="small" severity="secondary" text @click="addingAttendee = false" />
          </div>

          <DataTable :value="filteredAttendees" dataKey="id" editMode="row"
            v-model:editingRows="attendeeEditing" @row-edit-save="onAttendeeSave"
            class="rounded-xl overflow-hidden border border-gray-200 dark:border-gray-700">
            <Column field="firstname" header="First name">
              <template #editor="{ data, field }">
                <InputText v-model="data[field]" class="w-full" />
              </template>
            </Column>
            <Column field="lastname" header="Last name">
              <template #body="{ data }">{{ data.lastname ?? '—' }}</template>
              <template #editor="{ data, field }">
                <InputText v-model="data[field]" class="w-full" />
              </template>
            </Column>
            <Column :rowEditor="true" style="width: 6rem" />
            <Column style="width: 3rem">
              <template #body="{ data }">
                <Button icon="pi pi-trash" text rounded severity="danger" size="small" @click="onAttendeeDelete(data)" />
              </template>
            </Column>
          </DataTable>
        </TabPanel>

        <!-- ── FESTIVALS ── -->
        <TabPanel value="festivals">
          <div class="flex gap-2 mb-3 mt-4">
            <IconField class="flex-1">
              <InputIcon class="pi pi-search" />
              <InputText v-model="festivalQ" placeholder="Search festivals…" class="w-full" />
            </IconField>
            <Button icon="pi pi-plus" label="Add" size="small" @click="addingFestival = !addingFestival" />
          </div>

          <div v-if="addingFestival" class="flex gap-2 mb-3 p-3 bg-gray-50 dark:bg-gray-800 rounded-lg">
            <InputText v-model="newFestival.name" placeholder="Name *" class="flex-1" @keyup.enter="createFestival" />
            <Button icon="pi pi-check" size="small" @click="createFestival" :disabled="!newFestival.name.trim()" />
            <Button icon="pi pi-times" size="small" severity="secondary" text @click="addingFestival = false" />
          </div>

          <DataTable :value="filteredFestivals" dataKey="id" editMode="row"
            v-model:editingRows="festivalEditing" @row-edit-save="onFestivalSave"
            class="rounded-xl overflow-hidden border border-gray-200 dark:border-gray-700">
            <Column field="name" header="Name">
              <template #editor="{ data, field }">
                <InputText v-model="data[field]" class="w-full" />
              </template>
            </Column>
            <Column :rowEditor="true" style="width: 6rem" />
            <Column style="width: 3rem">
              <template #body="{ data }">
                <Button icon="pi pi-trash" text rounded severity="danger" size="small" @click="onFestivalDelete(data)" />
              </template>
            </Column>
          </DataTable>
        </TabPanel>

      </TabPanels>
    </Tabs>
  </div>
</template>
