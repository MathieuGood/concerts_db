<script setup lang="ts">
import { ref } from 'vue'
import Textarea from 'primevue/textarea'
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

const showComments = ref(!!props.modelValue.comments)
const showSetlist = ref(!!props.modelValue.setlist)

function update(field: keyof ConcertFormData, value: unknown) {
  emit('update:modelValue', { ...props.modelValue, [field]: value })
}
</script>

<template>
  <div class="border-b border-gray-100 dark:border-gray-800 last:border-0">
    <!-- Main row -->
    <div class="flex items-center gap-2 px-3 py-2">
      <span class="text-xs text-gray-400 w-4 shrink-0 text-center select-none">{{ index + 1 }}</span>
      <ArtistSelectOrCreate
        class="flex-1 min-w-0"
        :model-value="modelValue.artist_id"
        :artists="artists"
        @update:model-value="update('artist_id', $event)"
        @artist-created="emit('artist-created', $event)"
        @artist-updated="emit('artist-updated', $event)"
      />
      <button
        :title="showComments ? 'Hide comments' : 'Comments'"
        :class="['w-7 h-7 flex items-center justify-center rounded transition-colors',
          modelValue.comments ? 'text-d-cyan' : 'text-gray-300 dark:text-gray-600 hover:text-gray-500']"
        @click="showComments = !showComments"
      >
        <i class="pi pi-comment text-xs" />
      </button>
      <button
        :title="showSetlist ? 'Hide setlist' : 'Setlist'"
        :class="['w-7 h-7 flex items-center justify-center rounded transition-colors',
          modelValue.setlist ? 'text-d-purple' : 'text-gray-300 dark:text-gray-600 hover:text-gray-500']"
        @click="showSetlist = !showSetlist"
      >
        <i class="pi pi-list text-xs" />
      </button>
      <button
        :title="modelValue.i_played ? 'I performed (click to unmark)' : 'I performed'"
        :class="['w-7 h-7 flex items-center justify-center rounded transition-colors',
          modelValue.i_played ? 'text-amber-500' : 'text-gray-300 dark:text-gray-600 hover:text-gray-500']"
        @click="update('i_played', !modelValue.i_played)"
      >
        <i class="pi pi-microphone text-xs" />
      </button>
      <button
        title="Remove"
        class="w-7 h-7 flex items-center justify-center rounded text-gray-300 dark:text-gray-600 hover:text-red-400 transition-colors"
        @click="emit('remove')"
      >
        <i class="pi pi-times text-xs" />
      </button>
    </div>

    <!-- Comments (collapsible) -->
    <div v-if="showComments" class="px-3 pb-2 pl-9">
      <Textarea
        :model-value="modelValue.comments"
        placeholder="Comments"
        rows="2"
        auto-resize
        class="w-full text-sm"
        @update:model-value="update('comments', $event)"
      />
    </div>

    <!-- Setlist (collapsible) -->
    <div v-if="showSetlist" class="px-3 pb-2 pl-9">
      <Textarea
        :model-value="modelValue.setlist"
        placeholder="Setlist (one song per line)"
        rows="4"
        auto-resize
        class="w-full text-sm"
        @update:model-value="update('setlist', $event)"
      />
    </div>
  </div>
</template>
