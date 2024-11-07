import { MenuItem, Select } from "@mui/material"
import { Festival } from "../models/Festival"
import { Show } from "../models/Show"

export const FestivalSelect: React.FC<{
	show?: Show
	setShow: (show: Show) => void
	festivals: Festival[]
}> = ({ show, setShow, festivals }) => {
	return (
		<Select
			value={show?.festival && festivals.length > 0 ? show?.festival?.id : 0}
			label={show?.festival && festivals.length > 0 ? show?.festival.name : "No festival"}
			onChange={event => {
				const selectedFestivalId = event.target.value
				console.log(`Selected festival >>> ID ${selectedFestivalId}`)
				if (selectedFestivalId === 0) {
					setShow({
						...show,
						festival: { id: 0, name: "No festival" }
					} as Show)
					return
				}

				setShow({
					...show,
					festival: { id: selectedFestivalId, name: selectedFestivalId }
				} as Show)
			}}>
			<MenuItem value={0}>No festival</MenuItem>
			{festivals.map(festival => (
				<MenuItem key={festival.id} value={festival.id}>
					{festival.name}
				</MenuItem>
			))}
			<MenuItem value={0}>No festival</MenuItem>
		</Select>
	)
}

export default FestivalSelect
