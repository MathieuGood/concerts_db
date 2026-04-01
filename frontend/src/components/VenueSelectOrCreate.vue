<script setup lang="ts">
import { ref, watch } from 'vue'
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
}>()

const showCreate = ref(false)
const newName = ref('')
const saving = ref(false)

// Country autocomplete
const allCountries = ref<Country[]>([])
const selectedCountry = ref<Country | null>(null)
const countrySuggestions = ref<Country[]>([])

// City autocomplete
const allCities = ref<City[]>([])
const selectedCity = ref<City | null>(null)
const citySuggestions = ref<City[]>([])

async function onShowCreate() {
  showCreate.value = !showCreate.value
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
        :icon="showCreate ? 'pi pi-times' : 'pi pi-plus'"
        size="small"
        rounded
        :severity="showCreate ? 'secondary' : 'primary'"
        @click="onShowCreate"
        aria-label="Add venue"
      />
    </div>

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
  </div>
</template>
