import { useRoute, useRouter } from 'vue-router'

export function useListState() {
  const route = useRoute()
  const router = useRouter()

  const initialSearch = (route.query.search as string) || ''
  const initialExpandedIds: number[] = ((route.query.expanded as string) || '')
    .split(',').filter(Boolean).map(Number)

  function syncToUrl(search: string, expandedIds: number[]) {
    const query: Record<string, string> = {}
    if (search) query.search = search
    if (expandedIds.length) query.expanded = expandedIds.join(',')
    router.replace({ query })
  }

  return { initialSearch, initialExpandedIds, syncToUrl }
}
