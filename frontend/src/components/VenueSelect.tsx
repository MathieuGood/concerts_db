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
			value={show?.venue && venues.length > 0 ? show?.venue?.id : ""}
			label={show?.venue && venues.length > 0 ? show?.venue.name : "No venue"}
			onChange={event => {
				const selectedVenueId = event.target.value
				console.log(`Selected venue >>> ID ${selectedVenueId}`)

				const selectedVenue = venues.find(venue => venue.id === selectedVenueId)
				if (selectedVenue) {
					setShow({
						...show,
						venue: { id: selectedVenue.id, name: selectedVenue.name, address: selectedVenue.address }
					} as Show)
				}
			}}>
			{venues.map(venue => (
				<MenuItem key={venue.id} value={venue.id}>
					{venue.name}
				</MenuItem>
			))}
		</Select>
	)
}

export default VenueSelect
