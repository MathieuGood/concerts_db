import { Artist } from "./Artist"
import { Photo } from "./Photo"
import { Video } from "./Video"

export interface Concert {
	id?: number | undefined
	setlist: string | null
	comments: string
	show_id: number
	artist_id?: number
	artist: Artist
	photos: Photo[]
	videos: Video[]
}
