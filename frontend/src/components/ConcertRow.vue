<script setup lang="ts">
import { ref, computed } from 'vue'
import Textarea from 'primevue/textarea'
import Button from 'primevue/button'
import ArtistSelectOrCreate from './ArtistSelectOrCreate.vue'
import type { ConcertFormData } from '@/models/Event'
import type { Artist } from '@/models/Artist'

const props = defineProps<{
  modelValue: ConcertFormData
  index: number
  artists: Artist[]
}>()

const emit = defineEmits<{
  'update:modelValue': [value: ConcertFormData]
  'remove': []
  'artist-created': [artist: Artist]
  'artist-updated': [artist: Artist]
}>()

const showSetlist = ref(false)

const concert = computed({
  get: () => props.modelValue,
  set: (val) => emit('update:modelValue', val),
})

function update(field: keyof ConcertFormData, value: unknown) {
  emit('update:modelValue', { ...props.modelValue, [field]: value })
}
</script>

<template>
  <div class="border border-gray-200 dark:border-gray-700 rounded-xl p-4 space-y-3 bg-white dark:bg-gray-900">
    <div class="flex items-center justify-between">
      <span class="text-sm font-semibold text-d-purple">
        Concert {{ index + 1 }}
      </span>
      <Button
        icon="pi pi-trash"
        size="small"
        text
        severity="danger"
        @click="emit('remove')"
        aria-label="Remove concert"
      />
    </div>

    <ArtistSelectOrCreate
      :model-value="concert.artist_id"
      :artists="artists"
      @update:model-value="update('artist_id', $event)"
      @artist-created="emit('artist-created', $event)"
      @artist-updated="emit('artist-updated', $event)"
    />

    <Textarea
      :model-value="concert.comments"
      placeholder="Comments"
      rows="2"
      auto-resize
      class="w-full"
      @update:model-value="update('comments', $event)"
    />

    <button
      class="text-xs text-violet-500 dark:text-violet-400 underline cursor-pointer"
      @click="showSetlist = !showSetlist"
    >
      {{ showSetlist ? 'Hide setlist' : '+ Add setlist' }}
    </button>

    <Textarea
      v-if="showSetlist"
      :model-value="concert.setlist"
      placeholder="Setlist (one song per line)"
      rows="4"
      auto-resize
      class="w-full"
      @update:model-value="update('setlist', $event)"
    />
  </div>
</template>
