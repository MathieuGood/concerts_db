import { MenuItem, Select } from "@mui/material"
import { Artist } from "../models/Artist"
import { Show } from "../models/Show"
import { Concert } from "../models/Concert"

const ConcertArtistSelect: React.FC<{
	show?: Show
	setShow: (show: Show) => void
	artists: Artist[]
	concert: Concert
}> = ({ show, setShow, concert, artists }) => {
	return (
		<Select
			value={concert?.artist && artists.length > 0 ? concert?.artist.id : ""}
			label={concert?.artist && artists.length > 0 ? concert?.artist.name : "No artist"}
			onChange={event => {
				const selectedArtistId = event.target.value
				const selectedArtist = artists.find(artist => artist.id === selectedArtistId)
				console.log(`Selected artist >>> ID ${selectedArtistId}`)
				const updatedConcerts = show?.concerts.map(updatedConcert =>
					updatedConcert.id === concert.id
						? {
								...updatedConcert,
								artist_id: selectedArtistId,
								artist: {
									id: selectedArtistId,
									name: selectedArtist?.name || ""
								}
						  }
						: updatedConcert
				)

				setShow({
					...show,
					concerts: updatedConcerts
				} as Show)
			}}>
			{artists.map(artist => (
				<MenuItem key={artist.id} value={artist.id}>
					{artist.name}
				</MenuItem>
			))}
		</Select>
	)
}

export default ConcertArtistSelect
