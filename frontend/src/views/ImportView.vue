<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import Button from 'primevue/button'
import ProgressSpinner from 'primevue/progressspinner'
import { useToast } from 'primevue/usetoast'
import { downloadExport, runImport, type ImportReport } from '@/services/transferService'

const router = useRouter()
const toast = useToast()

// ── Export ────────────────────────────────────────────────────────────────────

const exporting = ref(false)

async function doExport() {
  exporting.value = true
  try {
    await downloadExport()
  } catch (e) {
    toast.add({ severity: 'error', summary: 'Export failed', detail: e instanceof Error ? e.message : 'Unknown error', life: 4000 })
  } finally {
    exporting.value = false
  }
}

// ── Import ────────────────────────────────────────────────────────────────────

const fileInput = ref<HTMLInputElement | null>(null)
const selectedFile = ref<File | null>(null)
const isDragging = ref(false)
const dryRunning = ref(false)
const importing = ref(false)
const report = ref<ImportReport | null>(null)
const importDone = ref(false)

function onDrop(e: DragEvent) {
  isDragging.value = false
  const file = e.dataTransfer?.files[0]
  if (file) processFile(file)
}

function onFileChange(e: Event) {
  const file = (e.target as HTMLInputElement).files?.[0]
  if (file) processFile(file)
}

async function processFile(file: File) {
  selectedFile.value = file
  report.value = null
  importDone.value = false
  dryRunning.value = true
  try {
    report.value = await runImport(file, true)
  } catch (e) {
    toast.add({ severity: 'error', summary: 'Could not parse CSV', detail: e instanceof Error ? e.message : 'Unknown error', life: 5000 })
    selectedFile.value = null
  } finally {
    dryRunning.value = false
  }
}

async function confirmImport() {
  if (!selectedFile.value) return
  importing.value = true
  try {
    report.value = await runImport(selectedFile.value, false)
    importDone.value = true
    toast.add({
      severity: 'success',
      summary: 'Import complete',
      detail: `${report.value.imported} imported, ${report.value.skipped} skipped`,
      life: 5000,
    })
  } catch (e) {
    toast.add({ severity: 'error', summary: 'Import failed', detail: e instanceof Error ? e.message : 'Unknown error', life: 5000 })
  } finally {
    importing.value = false
  }
}

function reset() {
  selectedFile.value = null
  report.value = null
  importDone.value = false
  if (fileInput.value) fileInput.value.value = ''
}
</script>

<template>
  <div class="space-y-6">

    <!-- Header -->
    <div class="flex items-center gap-3">
      <Button icon="pi pi-arrow-left" text size="small" @click="router.push('/')" aria-label="Back" />
      <h1 class="text-xl font-bold text-gray-900 dark:text-gray-100">Import / Export</h1>
    </div>

    <!-- ── Export ──────────────────────────────────────────────────────────── -->
    <div class="bg-white dark:bg-gray-900 rounded-xl border border-gray-200 dark:border-gray-700 p-5">
      <div class="flex items-start justify-between gap-4">
        <div>
          <h2 class="font-semibold text-gray-900 dark:text-gray-100">Export database</h2>
          <p class="text-sm text-gray-500 dark:text-gray-400 mt-0.5">
            Download all your shows as a CSV — full fidelity, suitable for backup or re-import.
          </p>
        </div>
        <Button
          icon="pi pi-download"
          label="Download CSV"
          :loading="exporting"
          class="shrink-0"
          @click="doExport"
        />
      </div>
    </div>

    <!-- ── Import ──────────────────────────────────────────────────────────── -->
    <div class="bg-white dark:bg-gray-900 rounded-xl border border-gray-200 dark:border-gray-700 p-5 space-y-4">
      <h2 class="font-semibold text-gray-900 dark:text-gray-100">Import CSV</h2>

      <!-- Drop zone -->
      <div
        class="border-2 border-dashed rounded-xl p-8 text-center cursor-pointer transition-colors select-none"
        :class="isDragging
          ? 'border-d-purple bg-violet-50 dark:bg-violet-950/20'
          : 'border-gray-300 dark:border-gray-600 hover:border-d-purple'"
        @click="fileInput?.click()"
        @dragover.prevent="isDragging = true"
        @dragleave.prevent="isDragging = false"
        @drop.prevent="onDrop"
      >
        <i class="pi pi-file-import text-3xl text-gray-400 dark:text-gray-500 mb-3 block" />
        <p class="text-sm font-medium text-gray-700 dark:text-gray-300">
          {{ selectedFile ? selectedFile.name : 'Drop a CSV here or click to browse' }}
        </p>
        <p v-if="!selectedFile" class="text-xs text-gray-400 mt-1">
          Accepts the standard concerts CSV format
        </p>
        <button
          v-if="selectedFile && !importDone"
          class="mt-2 text-xs text-gray-400 hover:text-gray-600 dark:hover:text-gray-300 underline"
          @click.stop="reset"
        >
          Clear
        </button>
      </div>
      <input ref="fileInput" type="file" accept=".csv" class="hidden" @change="onFileChange" />

      <!-- Dry-run spinner -->
      <div v-if="dryRunning" class="flex items-center justify-center gap-3 py-4">
        <ProgressSpinner style="width:28px;height:28px" />
        <span class="text-sm text-gray-500">Analysing…</span>
      </div>

      <!-- Preview -->
      <template v-if="report">

        <!-- Summary pills -->
        <div class="flex flex-wrap gap-2">
          <span class="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-sm font-medium bg-green-100 dark:bg-green-900/30 text-green-700 dark:text-green-400">
            <i class="pi pi-check text-xs" />
            {{ report.imported }} {{ importDone ? 'imported' : 'to import' }}
          </span>
          <span class="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-sm font-medium bg-yellow-100 dark:bg-yellow-900/30 text-yellow-700 dark:text-yellow-400">
            <i class="pi pi-minus-circle text-xs" />
            {{ report.skipped }} duplicate{{ report.skipped !== 1 ? 's' : '' }}
          </span>
          <span
            v-if="report.errors"
            class="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-sm font-medium bg-red-100 dark:bg-red-900/30 text-red-700 dark:text-red-400"
          >
            <i class="pi pi-times-circle text-xs" />
            {{ report.errors }} error{{ report.errors !== 1 ? 's' : '' }}
          </span>
        </div>

        <!-- Row table -->
        <div class="rounded-lg border border-gray-200 dark:border-gray-700 overflow-x-auto">
          <table class="w-full text-sm">
            <thead class="bg-gray-50 dark:bg-gray-800/60">
              <tr>
                <th class="text-left px-3 py-2 text-xs font-semibold text-gray-500 w-10">#</th>
                <th class="text-left px-3 py-2 text-xs font-semibold text-gray-500 whitespace-nowrap">Date</th>
                <th class="text-left px-3 py-2 text-xs font-semibold text-gray-500">Venue</th>
                <th class="text-left px-3 py-2 text-xs font-semibold text-gray-500">Artists</th>
                <th class="text-left px-3 py-2 text-xs font-semibold text-gray-500">Status</th>
              </tr>
            </thead>
            <tbody>
              <tr
                v-for="r in report.rows"
                :key="r.row"
                class="border-t border-gray-100 dark:border-gray-800"
                :class="{
                  'bg-green-50/50 dark:bg-green-900/10': r.status === 'import',
                  'bg-yellow-50/50 dark:bg-yellow-900/10': r.status === 'skip',
                  'bg-red-50/50 dark:bg-red-900/10': r.status === 'error',
                }"
              >
                <td class="px-3 py-2 text-gray-400 font-mono text-xs">{{ r.row }}</td>
                <td class="px-3 py-2 text-gray-700 dark:text-gray-300 font-mono text-xs whitespace-nowrap">{{ r.event_date }}</td>
                <td class="px-3 py-2 text-gray-700 dark:text-gray-300 text-xs max-w-[160px] truncate">{{ r.venue }}</td>
                <td class="px-3 py-2 text-gray-700 dark:text-gray-300 text-xs max-w-[180px] truncate">{{ r.artists }}</td>
                <td class="px-3 py-2 whitespace-nowrap">
                  <span
                    class="text-xs font-semibold px-2 py-0.5 rounded-full"
                    :class="{
                      'bg-green-100 dark:bg-green-900/30 text-green-700 dark:text-green-400': r.status === 'import',
                      'bg-yellow-100 dark:bg-yellow-900/30 text-yellow-700 dark:text-yellow-400': r.status === 'skip',
                      'bg-red-100 dark:bg-red-900/30 text-red-700 dark:text-red-400': r.status === 'error',
                    }"
                  >
                    {{ r.status === 'import' ? (importDone ? 'imported' : 'new') : r.status }}
                  </span>
                  <span v-if="r.reason" class="ml-1.5 text-xs text-gray-400">{{ r.reason }}</span>
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- Actions -->
        <div class="flex gap-3 justify-end pt-1">
          <template v-if="!importDone">
            <Button label="Reset" size="small" text severity="secondary" @click="reset" />
            <Button
              :label="`Import ${report.imported} show${report.imported !== 1 ? 's' : ''}`"
              icon="pi pi-upload"
              size="small"
              :disabled="report.imported === 0"
              :loading="importing"
              @click="confirmImport"
            />
          </template>
          <template v-else>
            <Button label="Import another file" size="small" text severity="secondary" @click="reset" />
            <Button label="Go to shows" icon="pi pi-calendar" size="small" @click="router.push('/')" />
          </template>
        </div>

      </template>
    </div>

  </div>
</template>
