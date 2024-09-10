import { Artist } from "./Artist"

export interface Concert {
    id: number
    setlist: string | null
    comments: string
    show_id: number
    artist_id: number
    artist?: Artist
}
