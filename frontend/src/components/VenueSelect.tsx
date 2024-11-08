import { MenuItem, Select } from "@mui/material"
import { Venue } from "../models/Venue"
import { Show } from "../models/Show"

export const VenueSelect: React.FC<{
	show?: Show
	setShow: (show: Show) => void
	venues: Venue[]
}> = ({ show, setShow, venues }) => {
	return (
		<Select
			value={show?.venue && venues.length > 0 ? show?.venue?.id : 0}
			label={show?.venue && venues.length > 0 ? show?.venue.name : "No venue"}
			onChange={event => {
				const selectedVenueId = event.target.value
				console.log(`Selected venue >>> ID ${selectedVenueId}`)
				if (selectedVenueId === 0) {
					setShow({
						...show,
						venue: { id: 0, name: "No venue" }
					} as Show)
					return
				}

				setShow({
					...show,
					venue: { id: selectedVenueId, name: selectedVenueId }
				} as Show)
			}}>
			<MenuItem value={0}>No venue</MenuItem>
			{venues.map(venue => (
				<MenuItem key={venue.id} value={venue.id}>
					{venue.name}
				</MenuItem>
			))}
			<MenuItem value={0}>No venue</MenuItem>
		</Select>
	)
}

export default VenueSelect
