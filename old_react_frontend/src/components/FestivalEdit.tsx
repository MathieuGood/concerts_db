import { useEffect, useState } from "react"
import { Festival } from "../models/Festival"
import { Button, TextField } from "@mui/material"
import { updateFestival, deleteFestival } from "../services/festivalService"
import { Show } from "../models/Show"

const FestivalEdit: React.FC<{
	festivalToEdit?: Festival | null
	updateFestivalSelectCallback: () => void
	show?: Show
	setShow: (show: Show) => void
	closeFestivalModal: () => void
}> = ({ festivalToEdit, updateFestivalSelectCallback, show, setShow, closeFestivalModal }) => {
	const [festival, setFestival] = useState<Festival | undefined | null>()

	useEffect(() => {
		if (festivalToEdit) {
			setFestival(festivalToEdit)
		}
	}, [festivalToEdit])

	const handleSaveFestival = (festival: Festival) => {
		updateFestival(festival)
			.then(response => {
				console.log("Festival updated: ", response)
				updateFestivalSelectCallback()
				closeFestivalModal()
			})
			.catch(error => {
				alert("Error updating festival")
				console.warn("CATCHING ERROR Error updating festival : ", error)
			})
	}

	const handleDeleteFestival = (festival: Festival) => {
		deleteFestival(festival).then(response => {
			console.log("Festival deleted: ", response)
			updateFestivalSelectCallback()
			setShow({
				...show,
				festival: null
			} as Show)
			setFestival(null)
		})
	}

	return (
		<div className="flex">
			<TextField
				label="Name"
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
			<Button
				onClick={() => {
					handleDeleteFestival(festival!)
				}}>
				Delete
			</Button>
		</div>
	)
}

export default FestivalEdit
