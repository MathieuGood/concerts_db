<script setup lang="ts">
import { ref, computed, watch, nextTick } from 'vue'
import Select from 'primevue/select'
import InputText from 'primevue/inputtext'
import InputNumber from 'primevue/inputnumber'
import Button from 'primevue/button'
import { festivalService } from '@/services/festivalService'
import type { Festival } from '@/models/Festival'

const props = defineProps<{
  modelValue: number | null
  festivals: Festival[]
}>()

const emit = defineEmits<{
  'update:modelValue': [value: number | null]
  'festival-created': [festival: Festival]
  'festival-updated': [festival: Festival]
}>()

function festivalLabel(f: Festival): string {
  return f.year ? `${f.name} (${f.year})` : f.name
}

const sortedFestivals = computed(() =>
  [...props.festivals].sort((a, b) => festivalLabel(a).localeCompare(festivalLabel(b))),
)

const selectedFestival = computed(() =>
  props.festivals.find((f) => f.id === props.modelValue) ?? null,
)

// ── Create state ──────────────────────────────────────────
const showCreate = ref(false)
const newName = ref('')
const newYear = ref<number | null>(null)
const saving = ref(false)
const newNameInput = ref<any>(null)

watch(showCreate, (val) => {
  if (val) nextTick(() => (newNameInput.value?.$el as HTMLInputElement)?.focus())
})

async function create() {
  if (!newName.value.trim()) return
  saving.value = true
  try {
    const festival = await festivalService.create(newName.value.trim(), newYear.value)
    emit('festival-created', festival)
    emit('update:modelValue', festival.id)
    newName.value = ''
    newYear.value = null
    showCreate.value = false
  } finally {
    saving.value = false
  }
}

// ── Edit state ────────────────────────────────────────────
const showEdit = ref(false)
const editName = ref('')
const editYear = ref<number | null>(null)
const editSaving = ref(false)
const editNameInput = ref<any>(null)

watch(showEdit, (val) => {
  if (val) nextTick(() => (editNameInput.value?.$el as HTMLInputElement)?.focus())
})

function openEdit() {
  if (!selectedFestival.value) return
  editName.value = selectedFestival.value.name
  editYear.value = selectedFestival.value.year ?? null
  showCreate.value = false
  showEdit.value = true
}

async function update() {
  if (!selectedFestival.value || !editName.value.trim()) return
  editSaving.value = true
  try {
    const updated = await festivalService.update(selectedFestival.value.id, editName.value.trim(), editYear.value)
    emit('festival-updated', updated)
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
        :options="sortedFestivals"
        :option-label="festivalLabel"
        option-value="id"
        filter
        auto-filter-focus
        filter-placeholder="Search festival..."
        placeholder="No festival"
        show-clear
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
        aria-label="Edit festival"
      />
      <Button
        :icon="showCreate ? 'pi pi-times' : 'pi pi-plus'"
        size="small"
        rounded
        :severity="showCreate ? 'secondary' : 'primary'"
        @click="showCreate = !showCreate; showEdit = false"
        aria-label="Add festival"
      />
    </div>

    <!-- Create panel -->
    <div v-if="showCreate" class="border border-violet-200 dark:border-violet-800 rounded-lg p-3 space-y-2 bg-violet-50 dark:bg-violet-950/30" @keydown.esc="showCreate = false">
      <p class="text-xs font-semibold text-violet-600 dark:text-violet-400 uppercase tracking-wide">New Festival</p>
      <div class="flex gap-2">
        <InputText ref="newNameInput" v-model="newName" placeholder="Festival name *" class="flex-1" @keyup.enter="create" />
        <InputNumber v-model="newYear" placeholder="Year" :use-grouping="false" :min="1900" :max="2100" class="w-28" />
      </div>
      <div class="flex justify-end gap-2">
        <Button label="Cancel" size="small" text severity="secondary" @click="showCreate = false" />
        <Button label="Save" size="small" :loading="saving" :disabled="!newName.trim()" @click="create" />
      </div>
    </div>

    <!-- Edit panel -->
    <div v-if="showEdit" class="border border-amber-200 dark:border-amber-800 rounded-lg p-3 space-y-2 bg-amber-50 dark:bg-amber-950/30" @keydown.esc="showEdit = false">
      <p class="text-xs font-semibold text-amber-600 dark:text-amber-400 uppercase tracking-wide">Edit Festival</p>
      <div class="flex gap-2">
        <InputText ref="editNameInput" v-model="editName" placeholder="Festival name *" class="flex-1" @keyup.enter="update" />
        <InputNumber v-model="editYear" placeholder="Year" :use-grouping="false" :min="1900" :max="2100" class="w-28" />
      </div>
      <div class="flex justify-end gap-2">
        <Button label="Cancel" size="small" text severity="secondary" @click="showEdit = false" />
        <Button label="Save" size="small" :loading="editSaving" :disabled="!editName.trim()" @click="update" />
      </div>
    </div>
  </div>
</template>
