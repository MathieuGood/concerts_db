<script setup lang="ts">
import { ref, reactive, onMounted, onUnmounted, computed, nextTick } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useToast } from 'primevue/usetoast'
import DatePicker from 'primevue/datepicker'
import InputText from 'primevue/inputtext'
import Textarea from 'primevue/textarea'
import Button from 'primevue/button'
import ProgressSpinner from 'primevue/progressspinner'
import VenueSelectOrCreate from '@/components/VenueSelectOrCreate.vue'
import FestivalSelectOrCreate from '@/components/FestivalSelectOrCreate.vue'
import ConcertRow from '@/components/ConcertRow.vue'
import AttendeeMultiSelect from '@/components/AttendeeMultiSelect.vue'
import { eventService, buildPayload } from '@/services/eventService'
import { venueService } from '@/services/venueService'
import { festivalService } from '@/services/festivalService'
import { artistService } from '@/services/artistService'
import { attendeeService } from '@/services/attendeeService'
import type { Venue } from '@/models/Venue'
import type { Festival } from '@/models/Festival'
import type { Artist } from '@/models/Artist'
import type { Attendee } from '@/models/Attendee'
import type { ConcertFormData } from '@/models/Event'

const route = useRoute()
const router = useRouter()
const toast = useToast()

const isEdit = computed(() => !!route.params.id)
const eventId = computed(() => Number(route.params.id))

// Reference data
const venues = ref<Venue[]>([])
const festivals = ref<Festival[]>([])
const artists = ref<Artist[]>([])
const attendees = ref<Attendee[]>([])

// Form state
const form = reactive({
  name: '',
  event_date: null as Date | null,
  comments: '',
  venue_id: null as number | null,
  festival_id: null as number | null,
  attendees_ids: [] as number[],
  concerts: [] as ConcertFormData[],
})

const loading = ref(true)
const saving = ref(false)
const deleting = ref(false)
const showAttendees = ref(false)
const datePickerRef = ref<any>(null)

function onKeyDown(e: KeyboardEvent) {
  if ((e.metaKey || e.ctrlKey) && e.key === 's') {
    e.preventDefault()
    save()
  }
}

onMounted(() => window.addEventListener('keydown', onKeyDown))
onUnmounted(() => window.removeEventListener('keydown', onKeyDown))

function newConcert(): ConcertFormData {
  return { id: null, artist_id: null, comments: '', setlist: '' }
}

function addConcert() {
  form.concerts.push(newConcert())
}

function removeConcert(index: number) {
  form.concerts.splice(index, 1)
}

function validate(): string | null {
  if (!form.event_date) return 'Date is required.'
  if (!form.venue_id) return 'Venue is required.'
  if (form.concerts.length === 0) return 'Add at least one concert.'
  if (form.concerts.some((c) => !c.artist_id)) return 'All concerts must have an artist.'
  return null
}

async function save() {
  const error = validate()
  if (error) {
    toast.add({ severity: 'warn', summary: 'Validation', detail: error, life: 4000 })
    return
  }

  saving.value = true
  try {
    const payload = buildPayload({
      ...form,
      event_date: form.event_date!,
      venue_id: form.venue_id!,
    })

    if (isEdit.value) {
      await eventService.update(eventId.value, payload)
      toast.add({ severity: 'success', summary: 'Saved', detail: 'Event updated.', life: 3000 })
      router.push('/')
    } else {
      await eventService.create(payload)
      toast.add({ severity: 'success', summary: 'Created', detail: 'Event created.', life: 3000 })
      router.push('/')
    }
  } catch (e: unknown) {
    const msg = e instanceof Error ? e.message : 'An error occurred.'
    toast.add({ severity: 'error', summary: 'Error', detail: msg, life: 5000 })
  } finally {
    saving.value = false
  }
}

async function deleteEvent() {
  if (!confirm('Delete this event? This cannot be undone.')) return
  deleting.value = true
  try {
    await eventService.delete(eventId.value)
    toast.add({ severity: 'info', summary: 'Deleted', detail: 'Event deleted.', life: 3000 })
    router.push('/')
  } catch (e: unknown) {
    const msg = e instanceof Error ? e.message : 'An error occurred.'
    toast.add({ severity: 'error', summary: 'Error', detail: msg, life: 5000 })
  } finally {
    deleting.value = false
  }
}

onMounted(async () => {
  const [v, f, a, att] = await Promise.all([
    venueService.getAll(),
    festivalService.getAll(),
    artistService.getAll(),
    attendeeService.getAll(),
  ])
  venues.value = v
  festivals.value = f
  artists.value = a
  attendees.value = att

  if (isEdit.value) {
    const event = await eventService.getOne(eventId.value)
    form.name = event.name ?? ''
    form.event_date = new Date(event.event_date + 'T00:00:00')
    form.comments = event.comments
    form.venue_id = event.venue_id
    form.festival_id = event.festival_id ?? null
    form.attendees_ids = event.attendees?.map((a) => a.id) ?? []
    form.concerts = event.concerts.map((c) => ({
      id: c.id,
      artist_id: c.artist_id,
      comments: c.comments,
      setlist: c.setlist ?? '',
    }))
    // Show attendees section if there are any
    if (form.attendees_ids.length > 0) showAttendees.value = true
  } else {
    addConcert()
  }

  loading.value = false
  if (!isEdit.value) {
    nextTick(() => {
      const input = datePickerRef.value?.$el?.querySelector('input') as HTMLInputElement | null
      input?.focus()
    })
  }
})
</script>

<template>
  <div class="space-y-6">
    <!-- Back + title -->
    <div class="flex items-center gap-3">
      <Button icon="pi pi-arrow-left" text size="small" @click="router.push('/')" aria-label="Back" />
      <h1 class="text-xl font-bold text-gray-900 dark:text-gray-100">
        {{ isEdit ? 'Edit Event' : 'New Event' }}
      </h1>
    </div>

    <!-- Loading -->
    <div v-if="loading" class="flex justify-center py-16">
      <ProgressSpinner style="width: 40px; height: 40px" />
    </div>

    <template v-else>
      <!-- Date + Name -->
      <section class="bg-white dark:bg-gray-900 rounded-xl border border-gray-200 dark:border-gray-700 p-4 space-y-4">
        <div>
          <label class="form-label">Date *</label>
          <DatePicker
            ref="datePickerRef"
            v-model="form.event_date"
            date-format="dd/mm/yy"
            :show-icon="true"
            :show-button-bar="true"
            class="w-full"
            input-class="w-full"
          />
        </div>
        <div>
          <label class="form-label">Event Name</label>
          <InputText v-model="form.name" class="w-full" />
        </div>
        <div>
          <label class="form-label">Comments</label>
          <Textarea v-model="form.comments" rows="2" auto-resize class="w-full" />
        </div>
      </section>

      <!-- Venue -->
      <section class="bg-white dark:bg-gray-900 rounded-xl border border-gray-200 dark:border-gray-700 p-4 space-y-2">
        <label class="form-label">Venue *</label>
        <VenueSelectOrCreate
          v-model="form.venue_id"
          :venues="venues"
          @venue-created="venues.push($event)"
          @venue-updated="venues = venues.map(v => v.id === $event.id ? $event : v)"
        />
      </section>

      <!-- Festival -->
      <section class="bg-white dark:bg-gray-900 rounded-xl border border-gray-200 dark:border-gray-700 p-4 space-y-2">
        <label class="form-label">Festival</label>
        <FestivalSelectOrCreate
          v-model="form.festival_id"
          :festivals="festivals"
          @festival-created="festivals.push($event)"
          @festival-updated="festivals = festivals.map(f => f.id === $event.id ? $event : f)"
        />
      </section>

      <!-- Concerts -->
      <section class="space-y-3">
        <div class="flex items-center justify-between">
          <h2 class="font-semibold text-gray-900 dark:text-gray-100">
            Concerts <span class="text-gray-400 font-normal">({{ form.concerts.length }})</span>
          </h2>
          <Button icon="pi pi-plus" label="Add concert" size="small" text @click="addConcert" />
        </div>

        <div v-if="form.concerts.length === 0" class="text-sm text-gray-400 text-center py-6 border border-dashed border-gray-300 dark:border-gray-700 rounded-xl">
          No concerts yet. Add at least one.
        </div>

        <ConcertRow
          v-for="(concert, i) in form.concerts"
          :key="i"
          v-model="form.concerts[i]!"
          :index="i"
          :artists="artists"
          @remove="removeConcert(i)"
          @artist-created="artists.push($event)"
          @artist-updated="artists = artists.map(a => a.id === $event.id ? $event : a)"
        />
      </section>

      <!-- Attendees (collapsible) -->
      <section class="bg-white dark:bg-gray-900 rounded-xl border border-gray-200 dark:border-gray-700 p-4">
        <button
          class="w-full flex items-center justify-between text-left"
          @click="showAttendees = !showAttendees"
        >
          <span class="form-label mb-0">
            Attendees
            <span v-if="form.attendees_ids.length" class="text-d-yellow font-semibold ml-1">({{ form.attendees_ids.length }})</span>
          </span>
          <i :class="['pi text-gray-400', showAttendees ? 'pi-chevron-up' : 'pi-chevron-down']" />
        </button>
        <div v-if="showAttendees" class="mt-3">
          <AttendeeMultiSelect v-model="form.attendees_ids" :attendees="attendees" @attendee-created="attendees.push($event)" />
        </div>
      </section>

      <!-- Actions -->
      <div class="flex gap-3 pt-2 pb-8">
        <Button
          label="Save"
          icon="pi pi-check"
          :loading="saving"
          class="flex-1"
          @click="save"
        />
        <Button
          v-if="isEdit"
          icon="pi pi-trash"
          severity="danger"
          outlined
          :loading="deleting"
          @click="deleteEvent"
          aria-label="Delete event"
        />
      </div>
    </template>
  </div>
</template>

<style scoped>
@reference "../assets/styles.css";

.form-label {
  @apply block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1;
}
</style>
