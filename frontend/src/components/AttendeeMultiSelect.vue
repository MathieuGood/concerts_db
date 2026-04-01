<script setup lang="ts">
import { ref } from 'vue'
import MultiSelect from 'primevue/multiselect'
import InputText from 'primevue/inputtext'
import Button from 'primevue/button'
import { attendeeService } from '@/services/attendeeService'
import type { Attendee } from '@/models/Attendee'

const props = defineProps<{
  modelValue: number[]
  attendees: Attendee[]
}>()

const emit = defineEmits<{
  'update:modelValue': [value: number[]]
  'attendee-created': [attendee: Attendee]
}>()

const showCreate = ref(false)
const newFirstname = ref('')
const newLastname = ref('')
const saving = ref(false)

async function create() {
  if (!newFirstname.value.trim()) return
  saving.value = true
  try {
    const attendee = await attendeeService.create(
      newFirstname.value.trim(),
      newLastname.value.trim() || undefined,
    )
    emit('attendee-created', attendee)
    emit('update:modelValue', [...props.modelValue, attendee.id])
    newFirstname.value = ''
    newLastname.value = ''
    showCreate.value = false
  } finally {
    saving.value = false
  }
}

function attendeeLabel(a: Attendee): string {
  return a.lastname ? `${a.firstname} ${a.lastname}` : a.firstname
}
</script>

<template>
  <div class="space-y-2">
    <div class="flex gap-2 items-center">
      <MultiSelect
        :model-value="modelValue"
        :options="attendees"
        :option-label="attendeeLabel"
        option-value="id"
        filter
        filter-placeholder="Search attendees..."
        placeholder="Select attendees"
        display="chip"
        class="flex-1"
        @update:model-value="emit('update:modelValue', $event)"
      />
      <Button
        :icon="showCreate ? 'pi pi-times' : 'pi pi-plus'"
        size="small"
        rounded
        :severity="showCreate ? 'secondary' : 'primary'"
        @click="showCreate = !showCreate"
        aria-label="Add attendee"
      />
    </div>

    <div v-if="showCreate" class="border border-violet-200 dark:border-violet-800 rounded-lg p-3 space-y-2 bg-violet-50 dark:bg-violet-950/30">
      <p class="text-xs font-semibold text-violet-600 dark:text-violet-400 uppercase tracking-wide">New Attendee</p>
      <div class="grid grid-cols-2 gap-2">
        <InputText v-model="newFirstname" placeholder="First name *" />
        <InputText v-model="newLastname" placeholder="Last name (optional)" @keyup.enter="create" />
      </div>
      <div class="flex justify-end gap-2">
        <Button label="Cancel" size="small" text severity="secondary" @click="showCreate = false" />
        <Button
          label="Save"
          size="small"
          :loading="saving"
          :disabled="!newFirstname.trim()"
          @click="create"
        />
      </div>
    </div>
  </div>
</template>
