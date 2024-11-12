import React from "react"
import { Concert } from "../models/Concert"
import { Button } from "@mui/material"
import { Show } from "../models/Show"

const AddConcertButton: React.FC<{
	show?: Show
	setShow: (show: Show) => void
}> = ({ show, setShow }) => {
	const concert: Concert = {
		setlist: "",
		comments: "",
		show_id: show?.id || 0,
		photos: [],
		videos: []
	}
	const createConcert = (setShow: (show: Show) => void, concert: Concert, show?: Show) => {
		if (show) setShow({ ...show, concerts: [...show.concerts, concert] })
	}

	return <Button onClick={() => createConcert(setShow, concert, show)}>Add concert</Button>
}

export default AddConcertButton
