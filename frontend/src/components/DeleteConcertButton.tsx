import { Show } from "../models/Show"
import { Button } from "@mui/material"

const DeleteConcertButton: React.FC<{
	show: Show
	setShow: (show: Show) => void
	concertIndex: number
}> = ({ show, setShow, concertIndex }) => {
	const deleteConcert = (show: Show, setShow: (show: Show) => void, concertIndex: number) => {
		const updatedConcerts = show.concerts.filter((_, index) => index !== concertIndex)
		setShow({ ...show, concerts: updatedConcerts })
	}

	return (
		<Button
			onClick={() => {
				deleteConcert(show, setShow, concertIndex)
			}}>
			❌
		</Button>
	)
}

export default DeleteConcertButton
