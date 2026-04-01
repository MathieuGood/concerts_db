import { useState } from "react"
import { Festival } from "../models/Festival"
import { Button, MenuItem, Select, TextField } from "@mui/material"
import { createFestival } from "../services/festivalService"
import { Show } from "../models/Show"
import VenueSelect from "./VenueSelect"
import { Venue } from "../models/Venue"

const FestivalCreate: React.FC<{
	updateFestivalSelectCallback: () => void
	show?: Show
	setShow: (show: Show) => void
	closeFestivalModal: () => void
	venues: Venue[]
}> = ({ updateFestivalSelectCallback, show, setShow, closeFestivalModal, venues }) => {
	const [festival, setFestival] = useState<Festival | undefined | null>()

	const handleSaveFestival = (festival: Festival) => {
		createFestival(festival)
			.then(response => {
				console.log("Festival created: ", response)
				updateFestivalSelectCallback()
				setShow({
					...show,
					festival: { id: response.id, name: response.name }
				} as Show)
				setFestival(null)
				closeFestivalModal()
			})
			.catch(error => {
				alert("Error creating festival")
				console.warn("CATCHING ERROR Error updating festival : ", error)
			})
	}

	return (
		<div className="flex">
			<TextField
				value={festival?.name || ""}
				onChange={e => {
					if (festival) {
						setFestival({ ...festival, name: e.target.value })
					} else {
						setFestival({ id: 0, name: e.target.value })
					}
				}}
			/>

			{/* Select pasted from frontend/src/components/VenueSelect.tsx */}
            {/* Create select for Venues */}
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
							venue: {
								id: selectedVenue.id,
								name: selectedVenue.name,
								address: selectedVenue.address
							}
						} as Show)
					}
				}}>
				{venues.map(venue => (
					<MenuItem key={venue.id} value={venue.id}>
						{venue.name}
					</MenuItem>
				))}
			</Select>

			<Button
				onClick={() => {
					handleSaveFestival(festival!)
				}}>
				Save
			</Button>
		</div>
	)
}

export default FestivalCreate
