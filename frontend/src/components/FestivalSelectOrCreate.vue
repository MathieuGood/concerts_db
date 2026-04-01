<script setup lang="ts">
import { ref } from 'vue'
import Select from 'primevue/select'
import InputText from 'primevue/inputtext'
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
}>()

const showCreate = ref(false)
const newName = ref('')
const saving = ref(false)

async function create() {
  if (!newName.value.trim()) return
  saving.value = true
  try {
    const festival = await festivalService.create(newName.value.trim())
    emit('festival-created', festival)
    emit('update:modelValue', festival.id)
    newName.value = ''
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
        :options="festivals"
        option-label="name"
        option-value="id"
        filter
        filter-placeholder="Search festival..."
        placeholder="No festival"
        show-clear
        class="flex-1"
        @update:model-value="emit('update:modelValue', $event)"
      />
      <Button
        :icon="showCreate ? 'pi pi-times' : 'pi pi-plus'"
        size="small"
        rounded
        :severity="showCreate ? 'secondary' : 'primary'"
        @click="showCreate = !showCreate"
        aria-label="Add festival"
      />
    </div>

    <div v-if="showCreate" class="border border-violet-200 dark:border-violet-800 rounded-lg p-3 space-y-2 bg-violet-50 dark:bg-violet-950/30">
      <p class="text-xs font-semibold text-violet-600 dark:text-violet-400 uppercase tracking-wide">New Festival</p>
      <InputText v-model="newName" placeholder="Festival name" class="w-full" @keyup.enter="create" />
      <div class="flex justify-end gap-2">
        <Button label="Cancel" size="small" text severity="secondary" @click="showCreate = false" />
        <Button label="Save" size="small" :loading="saving" :disabled="!newName.trim()" @click="create" />
      </div>
    </div>
  </div>
</template>
