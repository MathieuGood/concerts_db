import { Autocomplete, TextField } from "@mui/material"

import { Show } from "../models/Show"
import { Attendee } from "../models/Attendee"

export const AttendeeMultiSelect: React.FC<{
	show?: Show
	setShow: (show: Show) => void
	attendees: Attendee[]
}> = ({ show, setShow, attendees }) => {
	return (
		<Autocomplete
			multiple
			id="tags-standard"
			options={attendees}
			onChange={(event, newValue: Attendee[]) => {
				setShow({
					...show,
					attendees: newValue
				} as Show)
			}}
			value={show?.attendees && attendees.length > 0 ? show?.attendees : []}
			getOptionLabel={(option: Attendee) => option.firstname + " " + option.lastname}
			defaultValue={[]}
			renderInput={params => (
				<TextField
					{...params}
					variant="standard"
					label="Attendees"
					placeholder="Select one or more attendees"
				/>
			)}
		/>
	)
}

export default AttendeeMultiSelect
