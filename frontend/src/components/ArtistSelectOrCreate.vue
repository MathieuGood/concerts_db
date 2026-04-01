<script setup lang="ts">
import { ref } from 'vue'
import Select from 'primevue/select'
import AutoComplete from 'primevue/autocomplete'
import InputText from 'primevue/inputtext'
import Button from 'primevue/button'
import { artistService } from '@/services/artistService'
import { countryService } from '@/services/countryService'
import type { Artist } from '@/models/Artist'
import type { Country } from '@/models/Country'

const props = defineProps<{
  modelValue: number | null
  artists: Artist[]
}>()

const emit = defineEmits<{
  'update:modelValue': [value: number | null]
  'artist-created': [artist: Artist]
}>()

const showCreate = ref(false)
const newName = ref('')
const saving = ref(false)

const allCountries = ref<Country[]>([])
const selectedCountry = ref<Country | null>(null)
const countrySuggestions = ref<Country[]>([])

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

function countryName(): string {
  if (!selectedCountry.value) return ''
  return typeof selectedCountry.value === 'string'
    ? selectedCountry.value
    : selectedCountry.value.name
}

async function create() {
  if (!newName.value.trim()) return
  saving.value = true
  try {
    let country_id: number | null = null
    if (selectedCountry.value) {
      const country = await countryService.findOrCreate(countryName())
      country_id = country.id
    }
    const artist = await artistService.create(newName.value.trim(), country_id)
    emit('artist-created', artist)
    emit('update:modelValue', artist.id)
    newName.value = ''
    selectedCountry.value = null
    showCreate.value = false
  } finally {
    saving.value = false
  }
}
</script>

<template>
  <div class="space-y-2">
    <div class="flex gap-2 items-center">
      <Select
        :model-value="modelValue"
        :options="artists"
        option-label="name"
        option-value="id"
        filter
        filter-placeholder="Search artist..."
        placeholder="Select artist"
        class="flex-1"
        @update:model-value="emit('update:modelValue', $event)"
      />
      <Button
        :icon="showCreate ? 'pi pi-times' : 'pi pi-plus'"
        size="small"
        rounded
        :severity="showCreate ? 'secondary' : 'primary'"
        @click="onShowCreate"
        aria-label="Add artist"
      />
    </div>

    <div v-if="showCreate" class="border border-violet-200 dark:border-violet-800 rounded-lg p-3 space-y-2 bg-violet-50 dark:bg-violet-950/30">
      <p class="text-xs font-semibold text-violet-600 dark:text-violet-400 uppercase tracking-wide">New Artist</p>
      <InputText v-model="newName" placeholder="Artist name" class="w-full" />
      <AutoComplete
        v-model="selectedCountry"
        :suggestions="countrySuggestions"
        option-label="name"
        placeholder="Country (optional)"
        @complete="searchCountry"
        class="w-full"
        input-class="w-full"
      />
      <div class="flex justify-end gap-2">
        <Button label="Cancel" size="small" text severity="secondary" @click="showCreate = false" />
        <Button label="Save" size="small" :loading="saving" :disabled="!newName.trim()" @click="create" />
      </div>
    </div>
  </div>
</template>
