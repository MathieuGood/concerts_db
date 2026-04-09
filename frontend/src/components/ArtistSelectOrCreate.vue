<script setup lang="ts">
import { ref, computed } from 'vue'
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
  'artist-updated': [artist: Artist]
}>()

// ── Create state ──────────────────────────────────────────
const showCreate = ref(false)
const newName = ref('')
const saving = ref(false)

const allCountries = ref<Country[]>([])
const selectedCountry = ref<Country | null>(null)
const countrySuggestions = ref<Country[]>([])

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

// ── Edit state ────────────────────────────────────────────
const showEdit = ref(false)
const editName = ref('')
const editSaving = ref(false)
const editSelectedCountry = ref<Country | null>(null)
const editCountrySuggestions = ref<Country[]>([])

const selectedArtist = computed(() =>
  props.artists.find((a) => a.id === props.modelValue) ?? null,
)

function searchEditCountry(event: { query: string }) {
  const q = event.query.toLowerCase()
  editCountrySuggestions.value = allCountries.value.filter((c) =>
    c.name.toLowerCase().includes(q),
  )
}

function editCountryName(): string {
  if (!editSelectedCountry.value) return ''
  return typeof editSelectedCountry.value === 'string'
    ? editSelectedCountry.value
    : editSelectedCountry.value.name
}

async function openEdit() {
  const artist = selectedArtist.value
  if (!artist) return
  showCreate.value = false
  editName.value = artist.name
  if (allCountries.value.length === 0) {
    allCountries.value = await countryService.getAll()
  }
  editSelectedCountry.value = artist.country ?? null
  showEdit.value = true
}

async function update() {
  const artist = selectedArtist.value
  if (!artist || !editName.value.trim()) return
  editSaving.value = true
  try {
    let country_id: number | null = null
    if (editSelectedCountry.value) {
      const country = await countryService.findOrCreate(editCountryName())
      country_id = country.id
    }
    const updated = await artistService.update(artist.id, editName.value.trim(), country_id)
    emit('artist-updated', updated)
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
        v-if="modelValue"
        :icon="showEdit ? 'pi pi-times' : 'pi pi-pencil'"
        size="small"
        rounded
        severity="secondary"
        @click="showEdit ? (showEdit = false) : openEdit()"
        aria-label="Edit artist"
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

    <!-- Create panel -->
    <div v-if="showCreate" class="border border-violet-200 dark:border-violet-800 rounded-lg p-3 space-y-2 bg-violet-50 dark:bg-violet-950/30">
      <p class="text-xs font-semibold text-violet-600 dark:text-violet-400 uppercase tracking-wide">New Artist</p>
      <InputText v-model="newName" placeholder="Artist name" class="w-full" />
      <AutoComplete
        v-model="selectedCountry"
        :suggestions="countrySuggestions"
        option-label="name"
        placeholder="Country"
        @complete="searchCountry"
        class="w-full"
        input-class="w-full"
      />
      <div class="flex justify-end gap-2">
        <Button label="Cancel" size="small" text severity="secondary" @click="showCreate = false" />
        <Button label="Save" size="small" :loading="saving" :disabled="!newName.trim()" @click="create" />
      </div>
    </div>

    <!-- Edit panel -->
    <div v-if="showEdit" class="border border-amber-200 dark:border-amber-800 rounded-lg p-3 space-y-2 bg-amber-50 dark:bg-amber-950/30">
      <p class="text-xs font-semibold text-amber-600 dark:text-amber-400 uppercase tracking-wide">Edit Artist</p>
      <InputText v-model="editName" placeholder="Artist name" class="w-full" />
      <AutoComplete
        v-model="editSelectedCountry"
        :suggestions="editCountrySuggestions"
        option-label="name"
        placeholder="Country"
        @complete="searchEditCountry"
        class="w-full"
        input-class="w-full"
      />
      <div class="flex justify-end gap-2">
        <Button label="Cancel" size="small" text severity="secondary" @click="showEdit = false" />
        <Button label="Save" size="small" :loading="editSaving" :disabled="!editName.trim()" @click="update" />
      </div>
    </div>
  </div>
</template>
