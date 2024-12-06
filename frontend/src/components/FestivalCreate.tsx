import { useState } from "react"
import { Festival } from "../models/Festival"
import { Button, TextField } from "@mui/material"
import { createFestival } from "../services/festivalService"
import { Show } from "../models/Show"

const FestivalCreate: React.FC<{
	updateFestivalSelectCallback: () => void
	show?: Show
	setShow: (show: Show) => void
}> = ({ updateFestivalSelectCallback, show, setShow }) => {
	const [festival, setFestival] = useState<Festival | undefined | null>()

	const handleSaveFestival = (festival: Festival) => {
		createFestival(festival).then(response => {
			console.log("Festival created: ", response)
			updateFestivalSelectCallback()
			setShow({
				...show,
				festival: { id: response.id, name: response.name }
			} as Show)
			setFestival(null)
		})
	}

	return (
		<div>
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
