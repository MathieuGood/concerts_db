const BASE_URL = '/api'

function getToken(): string | null {
  return localStorage.getItem('access_token')
}

function authHeaders(): Record<string, string> {
  const token = getToken()
  return token ? { Authorization: `Bearer ${token}` } : {}
}

export async function downloadExport(): Promise<void> {
  const response = await fetch(`${BASE_URL}/transfer/export`, {
    headers: authHeaders(),
  })
  if (!response.ok) {
    const json = await response.json().catch(() => ({}))
    throw new Error((json as any).message ?? 'Export failed')
  }
  const blob = await response.blob()
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  const stamp = new Date().toISOString().slice(0, 10).replace(/-/g, '')
  a.download = `concerts_${stamp}.csv`
  document.body.appendChild(a)
  a.click()
  document.body.removeChild(a)
  URL.revokeObjectURL(url)
}

export interface ImportRow {
  row: number
  event_date: string
  venue: string
  artists: string
  status: 'import' | 'skip' | 'error'
  reason?: string
}

export interface ImportReport {
  dry_run: boolean
  total: number
  imported: number
  skipped: number
  errors: number
  rows: ImportRow[]
}

export async function runImport(file: File, dryRun: boolean): Promise<ImportReport> {
  const formData = new FormData()
  formData.append('file', file)

  const response = await fetch(`${BASE_URL}/transfer/import?dry_run=${dryRun}`, {
    method: 'POST',
    headers: authHeaders(),  // no Content-Type — browser sets multipart boundary
    body: formData,
  })

  const json = await response.json()
  if (response.status === 401) {
    localStorage.removeItem('access_token')
    localStorage.removeItem('user')
    window.location.href = '/login'
    throw new Error('Unauthorized')
  }
  if (!response.ok || !json.success) {
    throw new Error(json.message ?? 'Import failed')
  }
  return json.data as ImportReport
}
