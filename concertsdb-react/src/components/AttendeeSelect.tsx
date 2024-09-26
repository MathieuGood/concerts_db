import * as React from "react"
import { Theme, useTheme } from "@mui/material/styles"
import Box from "@mui/material/Box"
import OutlinedInput from "@mui/material/OutlinedInput"
import InputLabel from "@mui/material/InputLabel"
import MenuItem from "@mui/material/MenuItem"
import FormControl from "@mui/material/FormControl"
import Select, { SelectChangeEvent } from "@mui/material/Select"
import Chip from "@mui/material/Chip"
import { Show } from "../models/Show"

interface AttendeeSelectProps {
    show: Show | null
    setShow: React.Dispatch<React.SetStateAction<Show | null>>
}

const ITEM_HEIGHT = 48
const ITEM_PADDING_TOP = 8
const MenuProps = {
    PaperProps: {
        style: {
            maxHeight: ITEM_HEIGHT * 4.5 + ITEM_PADDING_TOP,
            width: 250,
        },
    },
}

const names = [
    "Franck Ludwig",
    "Agnès Maillard",
    "Gaëtan Wurtz",
    "Omar Alexander",
    "Carlos Abbott",
    "Miriam Wagner",
    "Bradley Wilkerson",
    "Virginia Andrews",
    "Kelly Snyder",
]

function getStyles(name: string, attendeeName: readonly string[], theme: Theme) {
    return {
        fontWeight: attendeeName.includes(name)
            ? theme.typography.fontWeightMedium
            : theme.typography.fontWeightRegular,
    }
}
const AttendeeSelect: React.FC<AttendeeSelectProps> = ({ show, setShow }) => {
    const theme = useTheme()
    const [selectedAttendees, setSelectedAttendeesName] = React.useState<string[]>([])

    console.log("AttendeeSelect show", show)

    const handleChange = (
        event: SelectChangeEvent<typeof selectedAttendees>
    ) => {
        const {
            target: { value },
        } = event
        setSelectedAttendeesName(
            // On autofill we get a stringified value.
            typeof value === "string" ? value.split(",") : value
        )
    }

    return (
        <FormControl fullWidth>
            <InputLabel id="demo-multiple-chip-label">Attendees</InputLabel>
            <Select
                labelId="demo-multiple-chip-label"
                id="demo-multiple-chip"
                multiple
                value={selectedAttendees}
                onChange={handleChange}
                input={
                    <OutlinedInput
                        id="select-multiple-chip"
                        label="Attendees"
                    />
                }
                renderValue={(selected) => (
                    <Box sx={{ display: "flex", flexWrap: "wrap", gap: 0.5 }}>
                        {selected.map((value) => (
                            <Chip key={value} label={value} />
                        ))}
                    </Box>
                )}
                MenuProps={MenuProps}
            >
                {names.map((fullName) => (
                    <MenuItem
                        key={fullName}
                        value={fullName}
                        style={getStyles(fullName, selectedAttendees, theme)}
                    >
                        {fullName}
                    </MenuItem>
                ))}
            </Select>
        </FormControl>
    )
}

export default AttendeeSelect
