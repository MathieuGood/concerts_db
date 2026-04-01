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
			value={show?.festival !== null && festivals.length > 0 ? show?.festival?.id : 0}
			label={"Festival"}
			displayEmpty
			renderValue={selected => {
				if (selected === 0) {
					return <em>No festival</em>
				}
				const selectedFestival = festivals.find(festival => festival.id === selected)
				return selectedFestival ? selectedFestival.name : "Error: No name for festival"
			}}
			onChange={event => {
				const selectedFestivalId = event.target.value
				const selectedFestival = festivals.find(festival => festival.id === selectedFestivalId)

				if (selectedFestivalId === 0) { 
					setShow({
						...show,
						festival: null
					} as Show)
					return
				}

				setShow({
					...show,
					festival: { id: selectedFestivalId, name: selectedFestival?.name }
				} as Show)
			}}>
			<MenuItem value={0}>
				<em>No festival</em>
			</MenuItem>
			{festivals.map(festival => (
				<MenuItem key={festival.id} value={festival.id || ""}>
					{festival.name}
				</MenuItem>
			))}
		</Select>
	)
}

export default FestivalSelect
