<script setup lang="ts">
import { ref, watch, computed } from 'vue'
import Select from 'primevue/select'
import AutoComplete from 'primevue/autocomplete'
import InputText from 'primevue/inputtext'
import Button from 'primevue/button'
import { venueService } from '@/services/venueService'
import { countryService } from '@/services/countryService'
import { cityService } from '@/services/cityService'
import type { Venue } from '@/models/Venue'
import type { Country } from '@/models/Country'
import type { City } from '@/models/City'

const props = defineProps<{
  modelValue: number | null
  venues: Venue[]
}>()

const emit = defineEmits<{
  'update:modelValue': [value: number | null]
  'venue-created': [venue: Venue]
  'venue-updated': [venue: Venue]
}>()

// ── Create state ──────────────────────────────────────────
const showCreate = ref(false)
const newName = ref('')
const saving = ref(false)

const allCountries = ref<Country[]>([])
const selectedCountry = ref<Country | null>(null)
const countrySuggestions = ref<Country[]>([])

const allCities = ref<City[]>([])
const selectedCity = ref<City | null>(null)
const citySuggestions = ref<City[]>([])

async function onShowCreate() {
  showCreate.value = !showCreate.value
  showEdit.value = false
  if (showCreate.value && allCountries.value.length === 0) {
    allCountries.value = await countryService.getAll()
  }
}

function searchCountry(event: { query: string }) {
  const q = event.query.toLowerCase()
  countrySuggestions.value = allCountries.value.filter((c) =>
    c.name.toLowerCase().includes(q),
  )
}

watch(selectedCountry, async (country) => {
  selectedCity.value = null
  if (country && typeof country === 'object' && 'id' in country) {
    allCities.value = await cityService.getAll((country as Country).id)
  } else {
    allCities.value = []
  }
})

function searchCity(event: { query: string }) {
  const q = event.query.toLowerCase()
  citySuggestions.value = allCities.value.filter((c) =>
    c.name.toLowerCase().includes(q),
  )
}

function countryName(): string {
  if (!selectedCountry.value) return ''
  return typeof selectedCountry.value === 'string'
    ? selectedCountry.value
    : selectedCountry.value.name
}

function cityName(): string {
  if (!selectedCity.value) return ''
  return typeof selectedCity.value === 'string'
    ? selectedCity.value
    : selectedCity.value.name
}

async function create() {
  if (!newName.value.trim() || !selectedCountry.value || !selectedCity.value) return
  saving.value = true
  try {
    const country = await countryService.findOrCreate(countryName())
    const city = await cityService.findOrCreate(cityName(), country.id)
    const venue = await venueService.create(newName.value.trim(), city.id)
    emit('venue-created', venue)
    emit('update:modelValue', venue.id)
    newName.value = ''
    selectedCountry.value = null
    selectedCity.value = null
    showCreate.value = false
  } finally {
    saving.value = false
  }
}

function venueLabel(v: Venue): string {
  return v.city ? `${v.name} — ${v.city.name}` : v.name
}

// ── Edit state ────────────────────────────────────────────
const showEdit = ref(false)
const editName = ref('')
const editSaving = ref(false)

const editSelectedCountry = ref<Country | null>(null)
const editCountrySuggestions = ref<Country[]>([])
const editAllCities = ref<City[]>([])
const editSelectedCity = ref<City | null>(null)
const editCitySuggestions = ref<City[]>([])

const selectedVenue = computed(() =>
  props.venues.find((v) => v.id === props.modelValue) ?? null,
)

function searchEditCountry(event: { query: string }) {
  const q = event.query.toLowerCase()
  editCountrySuggestions.value = allCountries.value.filter((c) =>
    c.name.toLowerCase().includes(q),
  )
}

async function onEditCountrySelect(event: { value: Country }) {
  editSelectedCity.value = null
  editAllCities.value = await cityService.getAll(event.value.id)
}

function searchEditCity(event: { query: string }) {
  const q = event.query.toLowerCase()
  editCitySuggestions.value = editAllCities.value.filter((c) =>
    c.name.toLowerCase().includes(q),
  )
}

function editCityName(): string {
  if (!editSelectedCity.value) return ''
  return typeof editSelectedCity.value === 'string'
    ? editSelectedCity.value
    : editSelectedCity.value.name
}

function editCountryName(): string {
  if (!editSelectedCountry.value) return ''
  return typeof editSelectedCountry.value === 'string'
    ? editSelectedCountry.value
    : editSelectedCountry.value.name
}

async function openEdit() {
  const venue = selectedVenue.value
  if (!venue) return
  showCreate.value = false
  editName.value = venue.name
  if (allCountries.value.length === 0) {
    allCountries.value = await countryService.getAll()
  }
  if (venue.city) {
    editAllCities.value = await cityService.getAll(venue.city.country_id)
    editSelectedCountry.value = venue.city.country ?? null
    editSelectedCity.value = venue.city
  } else {
    editSelectedCountry.value = null
    editAllCities.value = []
    editSelectedCity.value = null
  }
  showEdit.value = true
}

async function update() {
  const venue = selectedVenue.value
  if (!venue || !editName.value.trim() || !editSelectedCountry.value || !editSelectedCity.value) return
  editSaving.value = true
  try {
    const country = await countryService.findOrCreate(editCountryName())
    const city = await cityService.findOrCreate(editCityName(), country.id)
    const updated = await venueService.update(venue.id, editName.value.trim(), city.id)
    emit('venue-updated', updated)
    showEdit.value = false
  } finally {
    editSaving.value = false
  }
}
</script>

<template>
  <div class="space-y-2">
    <div class="flex gap-2 items-center">
      <Select
        :model-value="modelValue"
        :options="venues"
        :option-label="venueLabel"
        option-value="id"
        filter
        filter-placeholder="Search venue..."
        placeholder="Select venue"
        class="flex-1"
        @update:model-value="emit('update:modelValue', $event)"
      />
      <Button
        v-if="modelValue"
        :icon="showEdit ? 'pi pi-times' : 'pi pi-pencil'"
        size="small"
        rounded
        :severity="showEdit ? 'secondary' : 'secondary'"
        @click="showEdit ? (showEdit = false) : openEdit()"
        aria-label="Edit venue"
      />
      <Button
        :icon="showCreate ? 'pi pi-times' : 'pi pi-plus'"
        size="small"
        rounded
        :severity="showCreate ? 'secondary' : 'primary'"
        @click="onShowCreate"
        aria-label="Add venue"
      />
    </div>

    <!-- Create panel -->
    <div v-if="showCreate" class="border border-violet-200 dark:border-violet-800 rounded-lg p-3 space-y-2 bg-violet-50 dark:bg-violet-950/30">
      <p class="text-xs font-semibold text-violet-600 dark:text-violet-400 uppercase tracking-wide">New Venue</p>
      <InputText v-model="newName" placeholder="Venue name" class="w-full" />
      <div class="grid grid-cols-2 gap-2">
        <AutoComplete
          v-model="selectedCountry"
          :suggestions="countrySuggestions"
          option-label="name"
          placeholder="Country"
          @complete="searchCountry"
          class="w-full"
          input-class="w-full"
        />
        <AutoComplete
          v-model="selectedCity"
          :suggestions="citySuggestions"
          option-label="name"
          placeholder="City"
          :disabled="!selectedCountry"
          @complete="searchCity"
          class="w-full"
          input-class="w-full"
        />
      </div>
      <div class="flex justify-end gap-2">
        <Button label="Cancel" size="small" text severity="secondary" @click="showCreate = false" />
        <Button
          label="Save"
          size="small"
          :loading="saving"
          :disabled="!newName.trim() || !selectedCountry || !selectedCity"
          @click="create"
        />
      </div>
    </div>

    <!-- Edit panel -->
    <div v-if="showEdit" class="border border-amber-200 dark:border-amber-800 rounded-lg p-3 space-y-2 bg-amber-50 dark:bg-amber-950/30">
      <p class="text-xs font-semibold text-amber-600 dark:text-amber-400 uppercase tracking-wide">Edit Venue</p>
      <InputText v-model="editName" placeholder="Venue name" class="w-full" />
      <div class="grid grid-cols-2 gap-2">
        <AutoComplete
          v-model="editSelectedCountry"
          :suggestions="editCountrySuggestions"
          option-label="name"
          placeholder="Country"
          @complete="searchEditCountry"
          @option-select="onEditCountrySelect"
          class="w-full"
          input-class="w-full"
        />
        <AutoComplete
          v-model="editSelectedCity"
          :suggestions="editCitySuggestions"
          option-label="name"
          placeholder="City"
          :disabled="!editSelectedCountry"
          @complete="searchEditCity"
          class="w-full"
          input-class="w-full"
        />
      </div>
      <div class="flex justify-end gap-2">
        <Button label="Cancel" size="small" text severity="secondary" @click="showEdit = false" />
        <Button
          label="Save"
          size="small"
          :loading="editSaving"
          :disabled="!editName.trim() || !editSelectedCountry || !editSelectedCity"
          @click="update"
        />
      </div>
    </div>
  </div>
</template>
