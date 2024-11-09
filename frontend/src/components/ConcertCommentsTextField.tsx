import { Show } from "../models/Show"
import { Concert } from "../models/Concert"
import { TextField } from "@mui/material"

const ConcertCommentsTextField: React.FC<{
	show?: Show
	setShow: (show: Show) => void
	concert: Concert
}> = ({ show, setShow, concert }) => {
	return (
		<TextField
			value={concert.comments}
			onChange={event => {
				const newComments = event.target.value
				console.log("Updated comments : ", newComments)
				const updatedConcerts = show?.concerts.map(updatedConcert =>
					updatedConcert.id === concert.id
						? {
								...updatedConcert,
								comments: newComments
						  }
						: updatedConcert
				)
				console.log("Updated concerts after comment change", updatedConcerts)
				setShow({ ...show, concerts: updatedConcerts } as Show)
			}}
		/>
	)
}

export default ConcertCommentsTextField
