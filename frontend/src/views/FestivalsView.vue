<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue'
import { normalize } from '@/utils/search'
import { useRouter } from 'vue-router'
import { useConfirm } from 'primevue/useconfirm'
import { useToast } from 'primevue/usetoast'
import DataTable from 'primevue/datatable'
import Column from 'primevue/column'
import InputText from 'primevue/inputtext'
import InputNumber from 'primevue/inputnumber'
import Button from 'primevue/button'
import IconField from 'primevue/iconfield'
import InputIcon from 'primevue/inputicon'
import ProgressSpinner from 'primevue/progressspinner'

import { festivalService } from '@/services/festivalService'
import { eventService } from '@/services/eventService'
import { useListState } from '@/composables/useListState'

const router = useRouter()
const confirm = useConfirm()
const toast = useToast()

interface EventEntry { id: number; date: string; venue: string; city: string; artists: string }

interface FestivalEdition {
  id: number
  year: number | null
  events: number
  artists: number
  firstDate: string | null
  lastDate: string | null
  eventList: EventEntry[]
  _editing: boolean
}

interface FestivalSeries {
  name: string
  editions: FestivalEdition[]
  totalEvents: number
  totalArtists: number
  firstYear: number | null
  lastYear: number | null
}

const { initialSearch, initialExpandedIds, syncToUrl } = useListState()

const loading = ref(true)
const series = ref<FestivalSeries[]>([])
const expandedRows = ref<any[]>([])  // expanded series
const expandedCards = ref<number[]>([]) // mobile: expanded series by first-edition id
const editData = ref<Record<number, { name: string; year: number | null }>>({})
const search = ref(initialSearch)
const addingFestival = ref(false)
const newFestivalName = ref('')
const newFestivalYear = ref<number | null>(null)

onMounted(async () => {
  try {
    const [festivals, events] = await Promise.all([festivalService.getAll(), eventService.getAll()])

    // Per-festival stats
    const statsMap = new Map<number, { events: number; artistIds: Set<number>; first: string; last: string; eventList: EventEntry[] }>()
    for (const event of events) {
      const fid = event.festival_id
      if (!fid) continue
      if (!statsMap.has(fid)) statsMap.set(fid, { events: 0, artistIds: new Set(), first: event.event_date, last: event.event_date, eventList: [] })
      const s = statsMap.get(fid)!
      s.events++
      event.concerts.forEach(c => { if (c.artist_id) s.artistIds.add(c.artist_id) })
      if (event.event_date < s.first) s.first = event.event_date
      if (event.event_date > s.last) s.last = event.event_date
      s.eventList.push({ id: event.id, date: event.event_date, venue: event.venue?.name ?? '—', city: event.venue?.city?.name ?? '—', artists: event.concerts.map(c => c.artist?.name ?? '').filter(Boolean).join(', ') })
    }

    // Group by name into series
    const seriesMap = new Map<string, FestivalEdition[]>()
    for (const f of festivals) {
      const s = statsMap.get(f.id)
      const edition: FestivalEdition = {
        id: f.id,
        year: f.year ?? null,
        events: s?.events ?? 0,
        artists: s?.artistIds.size ?? 0,
        firstDate: s?.first ?? null,
        lastDate: s?.last ?? null,
        eventList: s?.eventList.sort((a, b) => b.date.localeCompare(a.date)) ?? [],
        _editing: false,
      }
      if (!seriesMap.has(f.name)) seriesMap.set(f.name, [])
      seriesMap.get(f.name)!.push(edition)
    }

    series.value = [...seriesMap.entries()].map(([name, editions]) => {
      editions.sort((a, b) => (a.year ?? 0) - (b.year ?? 0))
      const allArtistIds = new Set(editions.flatMap(e => {
        const s = statsMap.get(e.id)
        return s ? [...s.artistIds] : []
      }))
      const years = editions.map(e => e.year).filter((y): y is number => y !== null)
      return {
        name,
        editions,
        totalEvents: editions.reduce((sum, e) => sum + e.events, 0),
        totalArtists: allArtistIds.size,
        firstYear: years.length ? Math.min(...years) : null,
        lastYear: years.length ? Math.max(...years) : null,
      }
    }).sort((a, b) => a.name.localeCompare(b.name))

    // Restore expanded state — a series is expanded if any of its edition IDs is in initialExpandedIds
    expandedRows.value = series.value.filter(s => s.editions.some(e => initialExpandedIds.includes(e.id)))
    expandedCards.value = initialExpandedIds.filter(id => series.value.some(s => s.editions.some(e => e.id === id)))
  } finally { loading.value = false }
})

watch([search, expandedRows, expandedCards], () => {
  // Store first edition ID of each expanded series in URL
  const ids = [...new Set([
    ...expandedRows.value.flatMap((s: FestivalSeries) => s.editions[0] ? [s.editions[0].id] : []),
    ...expandedCards.value,
  ])]
  syncToUrl(search.value, ids)
}, { deep: true })

function formatDate(d: string | null) {
  if (!d) return '—'
  return new Date(d + 'T00:00:00').toLocaleDateString('en-GB', { day: '2-digit', month: 'short', year: 'numeric' })
}

const filtered = computed(() => {
  const q = normalize(search.value)
  return q ? series.value.filter(s => normalize(s.name).includes(q)) : series.value
})

// ── Edit ─────────────────────────────────────────────────────
function startEdit(edition: FestivalEdition) {
  editData.value[edition.id] = { name: findSeriesName(edition.id), year: edition.year }
  edition._editing = true
}
function cancelEdit(edition: FestivalEdition) {
  delete editData.value[edition.id]
  edition._editing = false
}
function findSeriesName(editionId: number): string {
  return series.value.find(s => s.editions.some(e => e.id === editionId))?.name ?? ''
}
async function saveEdition(edition: FestivalEdition) {
  const d = editData.value[edition.id]
  if (!d) return
  try {
    await festivalService.update(edition.id, d.name.trim(), d.year)
    // Update local state
    const oldSeries = series.value.find(s => s.editions.some(e => e.id === edition.id))
    if (oldSeries) {
      oldSeries.editions = oldSeries.editions.filter(e => e.id !== edition.id)
      edition.year = d.year
      edition._editing = false
      // Move to correct series (name may have changed)
      let targetSeries = series.value.find(s => s.name === d.name.trim())
      if (!targetSeries) {
        targetSeries = { name: d.name.trim(), editions: [], totalEvents: 0, totalArtists: 0, firstYear: null, lastYear: null }
        series.value.push(targetSeries)
        series.value.sort((a, b) => a.name.localeCompare(b.name))
      }
      targetSeries.editions.push(edition)
      targetSeries.editions.sort((a, b) => (a.year ?? 0) - (b.year ?? 0))
      // Recompute series stats
      recomputeSeries(targetSeries)
      if (oldSeries !== targetSeries) {
        recomputeSeries(oldSeries)
        if (oldSeries.editions.length === 0) series.value = series.value.filter(s => s !== oldSeries)
      }
    }
    delete editData.value[edition.id]
  } catch (e) {
    toast.add({ severity: 'error', summary: 'Error', detail: e instanceof Error ? e.message : 'An error occurred.', life: 5000 })
  }
}
function recomputeSeries(s: FestivalSeries) {
  const years = s.editions.map(e => e.year).filter((y): y is number => y !== null)
  s.totalEvents = s.editions.reduce((sum, e) => sum + e.events, 0)
  s.firstYear = years.length ? Math.min(...years) : null
  s.lastYear = years.length ? Math.max(...years) : null
}

function onDelete(edition: FestivalEdition) {
  const seriesName = findSeriesName(edition.id)
  const label = edition.year ? `${seriesName} (${edition.year})` : seriesName
  confirm.require({
    message: `Delete "${label}"?`, header: 'Confirm deletion', icon: 'pi pi-exclamation-triangle',
    acceptLabel: 'Delete', rejectLabel: 'Cancel',
    accept: async () => {
      try {
        await festivalService.delete(edition.id)
        const s = series.value.find(sr => sr.editions.some(e => e.id === edition.id))
        if (s) {
          s.editions = s.editions.filter(e => e.id !== edition.id)
          if (s.editions.length === 0) series.value = series.value.filter(sr => sr !== s)
          else recomputeSeries(s)
        }
      } catch (e) {
        toast.add({ severity: 'error', summary: 'Error', detail: e instanceof Error ? e.message : 'An error occurred.', life: 5000 })
      }
    }
  })
}

async function createFestival() {
  if (!newFestivalName.value.trim()) return
  try {
    const created = await festivalService.create(newFestivalName.value.trim(), newFestivalYear.value)
    const newEdition: FestivalEdition = { id: created.id, year: created.year ?? null, events: 0, artists: 0, firstDate: null, lastDate: null, eventList: [], _editing: false }
    let target = series.value.find(s => s.name === created.name)
    if (!target) {
      target = { name: created.name, editions: [], totalEvents: 0, totalArtists: 0, firstYear: null, lastYear: null }
      series.value.push(target)
      series.value.sort((a, b) => a.name.localeCompare(b.name))
    }
    target.editions.push(newEdition)
    target.editions.sort((a, b) => (a.year ?? 0) - (b.year ?? 0))
    recomputeSeries(target)
    newFestivalName.value = ''
    newFestivalYear.value = null
    addingFestival.value = false
  } catch (e) {
    toast.add({ severity: 'error', summary: 'Error', detail: e instanceof Error ? e.message : 'An error occurred.', life: 5000 })
  }
}

// ── Mobile helpers ────────────────────────────────────────
function isExpanded(id: number) { return expandedCards.value.includes(id) }
function toggleExpand(id: number) {
  const idx = expandedCards.value.indexOf(id)
  if (idx === -1) expandedCards.value.push(id)
  else expandedCards.value.splice(idx, 1)
}
</script>

<template>
  <div class="space-y-4">
    <div v-if="loading" class="flex justify-center py-16"><ProgressSpinner style="width:40px;height:40px" /></div>
    <template v-else>
      <div class="flex gap-2">
        <IconField class="flex-1"><InputIcon class="pi pi-search" /><InputText v-model="search" placeholder="Search festivals…" class="w-full" /></IconField>
        <span class="text-xs text-gray-400 self-center whitespace-nowrap">{{ filtered.length }} serie{{ filtered.length !== 1 ? 's' : '' }}</span>
        <Button icon="pi pi-plus" label="Add" size="small" class="ml-3" @click="addingFestival = !addingFestival" />
      </div>
      <div v-if="addingFestival" class="flex gap-2 p-3 bg-gray-50 dark:bg-gray-800 rounded-lg">
        <InputText v-model="newFestivalName" placeholder="Name *" class="flex-1" @keyup.enter="createFestival" />
        <InputNumber v-model="newFestivalYear" placeholder="Year" :use-grouping="false" :min="1900" :max="2100" class="w-28" />
        <Button icon="pi pi-check" size="small" @click="createFestival" :disabled="!newFestivalName.trim()" />
        <Button icon="pi pi-times" size="small" severity="secondary" text @click="addingFestival = false" />
      </div>

      <!-- Mobile card list -->
      <div class="sm:hidden space-y-2">
        <div v-for="s in filtered" :key="s.name"
             class="rounded-xl border border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-900 overflow-hidden">
          <div class="flex items-start p-3 gap-2 cursor-pointer" @click="toggleExpand(s.editions[0]?.id ?? -1)">
            <div class="flex-1 min-w-0">
              <div class="font-medium text-sm">{{ s.name }}</div>
              <div class="flex flex-wrap gap-1.5 mt-2">
                <span class="inline-flex items-center gap-1 bg-gray-100 dark:bg-gray-800 px-2 py-0.5 rounded-full text-xs">
                  <span class="font-semibold text-d-red">{{ s.editions.length }}</span><span class="text-gray-500">edition{{ s.editions.length !== 1 ? 's' : '' }}</span>
                </span>
                <span class="inline-flex items-center gap-1 bg-gray-100 dark:bg-gray-800 px-2 py-0.5 rounded-full text-xs">
                  <span class="font-semibold text-d-red">{{ s.totalEvents }}</span><span class="text-gray-500">days</span>
                </span>
                <span v-if="s.firstYear" class="inline-flex items-center gap-1 bg-gray-100 dark:bg-gray-800 px-2 py-0.5 rounded-full text-xs text-gray-500">
                  {{ s.firstYear === s.lastYear ? s.firstYear : `${s.firstYear}–${s.lastYear}` }}
                </span>
              </div>
            </div>
            <i class="pi text-xs text-gray-400 w-5 text-center mt-1" :class="isExpanded(s.editions[0]?.id ?? -1) ? 'pi-chevron-up' : 'pi-chevron-down'" />
          </div>

          <div v-if="isExpanded(s.editions[0]?.id ?? -1)" class="border-t border-gray-100 dark:border-gray-800">
            <div v-for="edition in s.editions" :key="edition.id">
              <!-- Edition edit mode -->
              <div v-if="edition._editing" class="p-3 space-y-2 bg-gray-50 dark:bg-gray-800/50">
                <div class="flex gap-2">
                  <InputText v-model="editData[edition.id]!.name" placeholder="Name *" class="flex-1" />
                  <InputNumber v-model="editData[edition.id]!.year" placeholder="Year" :use-grouping="false" :min="1900" :max="2100" class="w-24" />
                </div>
                <div class="flex gap-2">
                  <Button icon="pi pi-check" label="Save" size="small" severity="success" @click="saveEdition(edition)" class="flex-1" />
                  <Button icon="pi pi-times" size="small" severity="secondary" text rounded @click="cancelEdit(edition)" />
                  <Button icon="pi pi-trash" size="small" severity="danger" text rounded @click="onDelete(edition)" />
                </div>
              </div>
              <!-- Edition normal mode -->
              <div v-else class="flex items-center gap-2 px-4 py-2.5 border-b border-gray-50 dark:border-gray-800/50 last:border-0">
                <div class="flex-1 min-w-0">
                  <span class="text-sm font-medium">{{ edition.year ?? '—' }}</span>
                  <span class="text-xs text-gray-400 ml-2">{{ edition.events }} days · {{ edition.artists }} artists</span>
                </div>
                <Button icon="pi pi-pencil" text rounded size="small" severity="secondary" @click.stop="startEdit(edition)" />
              </div>
              <!-- Events under this edition -->
              <div v-for="e in edition.eventList" :key="e.id"
                   class="flex items-center gap-2 pl-8 pr-4 py-2 border-b border-gray-50 dark:border-gray-800/50 cursor-pointer active:bg-gray-50 dark:active:bg-gray-800/30 last:border-0"
                   @click="router.push(`/event/${e.id}`)">
                <div class="flex-1 min-w-0">
                  <div class="text-xs text-gray-500 whitespace-nowrap">{{ formatDate(e.date) }}</div>
                  <div class="text-sm truncate">{{ e.venue }}, {{ e.city }}</div>
                  <div class="text-xs text-gray-400 truncate">{{ e.artists || '—' }}</div>
                </div>
                <i class="pi pi-arrow-right text-xs text-gray-300 shrink-0" />
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Desktop table -->
      <div class="hidden sm:block">
        <DataTable :value="filtered" dataKey="name" size="small"
          v-model:expandedRows="expandedRows"
          class="rounded-xl overflow-hidden border border-gray-200 dark:border-gray-700" rowHover>
          <Column expander style="width:3rem" />
          <Column field="name" header="Festival" sortable />
          <Column header="Editions" style="width:90px">
            <template #body="{ data }">
              <span class="text-sm">{{ data.editions.length }}</span>
            </template>
          </Column>
          <Column header="Years" style="width:120px">
            <template #body="{ data }">
              <span class="text-xs text-gray-500">
                {{ data.firstYear ? (data.firstYear === data.lastYear ? data.firstYear : `${data.firstYear} – ${data.lastYear}`) : '—' }}
              </span>
            </template>
          </Column>
          <Column header="Days" style="width:70px">
            <template #body="{ data }"><span class="text-sm">{{ data.totalEvents }}</span></template>
          </Column>

          <!-- Expansion: per-edition sub-table -->
          <template #expansion="{ data: s }">
            <div class="px-4 py-4">
              <table class="w-full text-sm">
                <thead>
                  <tr class="text-xs text-gray-400 uppercase tracking-wide border-b border-gray-100 dark:border-gray-800">
                    <th class="text-left pb-2 font-medium w-20">Year</th>
                    <th class="text-left pb-2 font-medium w-20">Days</th>
                    <th class="text-left pb-2 font-medium w-20">Artists</th>
                    <th class="text-left pb-2 font-medium">Dates</th>
                    <th class="pb-2 w-24"></th>
                  </tr>
                </thead>
                <tbody>
                  <template v-for="edition in s.editions" :key="edition.id">
                    <!-- Edit row -->
                    <tr v-if="edition._editing" class="border-b border-gray-50 dark:border-gray-800/50">
                      <td colspan="4" class="py-2 pr-4">
                        <div class="flex gap-2">
                          <InputText v-model="editData[edition.id]!.name" placeholder="Name *" class="flex-1" @keyup.enter="saveEdition(edition)" @keyup.esc="cancelEdit(edition)" />
                          <InputNumber v-model="editData[edition.id]!.year" placeholder="Year" :use-grouping="false" :min="1900" :max="2100" class="w-28" />
                        </div>
                      </td>
                      <td class="py-2">
                        <div class="flex gap-0.5 justify-end">
                          <Button icon="pi pi-check" text rounded size="small" severity="success" @click="saveEdition(edition)" />
                          <Button icon="pi pi-times" text rounded size="small" severity="secondary" @click="cancelEdit(edition)" />
                          <Button icon="pi pi-trash" text rounded size="small" severity="danger" @click="onDelete(edition)" />
                        </div>
                      </td>
                    </tr>
                    <!-- Normal row -->
                    <tr v-else class="border-b border-gray-50 dark:border-gray-800/50">
                      <td class="py-1.5 pr-4 font-medium">{{ edition.year ?? '—' }}</td>
                      <td class="py-1.5 pr-4 text-gray-500">{{ edition.events }}</td>
                      <td class="py-1.5 pr-4 text-gray-500">{{ edition.artists }}</td>
                      <td class="py-1.5 pr-4 text-xs text-gray-400">
                        {{ edition.firstDate ? formatDate(edition.firstDate) : '—' }}
                        <span v-if="edition.firstDate !== edition.lastDate"> → {{ formatDate(edition.lastDate) }}</span>
                      </td>
                      <td class="py-1.5 text-right">
                        <Button icon="pi pi-pencil" text rounded size="small" severity="secondary" @click="startEdit(edition)" />
                      </td>
                    </tr>
                    <!-- Events under this edition -->
                    <tr v-for="e in edition.eventList" :key="e.id"
                        class="border-b border-gray-50 dark:border-gray-800/50 hover:bg-gray-50 dark:hover:bg-gray-800/30 cursor-pointer"
                        @click="router.push(`/event/${e.id}`)">
                      <td class="py-1.5 pl-6 pr-4 text-gray-400 text-xs whitespace-nowrap" colspan="1">{{ formatDate(e.date) }}</td>
                      <td class="py-1.5 pr-4 text-gray-500" colspan="1">{{ e.venue }}</td>
                      <td class="py-1.5 pr-4 text-gray-500" colspan="1">{{ e.city }}</td>
                      <td class="py-1.5 pr-4 text-gray-500 text-xs" colspan="1">{{ e.artists || '—' }}</td>
                      <td class="py-1.5"><i class="pi pi-arrow-right text-xs text-gray-300" /></td>
                    </tr>
                  </template>
                </tbody>
              </table>
            </div>
          </template>
        </DataTable>
      </div>
    </template>
  </div>
</template>
