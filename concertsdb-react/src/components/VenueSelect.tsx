import React from "react"
import { FormControl, InputLabel, Select, MenuItem } from "@mui/material"
import { Show } from "../models/Show"

interface VenueSelectProps {
    show: Show | null
    setShow: React.Dispatch<React.SetStateAction<Show | null>>
}

const VenueSelect: React.FC<VenueSelectProps> = ({ show, setShow }) => {
    return (
        <FormControl fullWidth margin="normal">
            <InputLabel id="venue-label">Venue</InputLabel>
            <Select
                labelId="venue-label"
                id="venue"
                value={show?.venue?.name ? show.venue.name : ""}
                label="Venue"
                onChange={(e) =>
                    setShow({
                        ...show,
                        venue: { name: e.target.value },
                    } as Show)
                }
            >
                <MenuItem value={"The Fillmore"}>The Fillmore</MenuItem>
                <MenuItem value={"La Laiterie"}>La Laiterie</MenuItem>
                <MenuItem value={"E-Werk"}>E-Werk</MenuItem>
                <MenuItem value={"Boston Garden"}>Boston Garden</MenuItem>
                <MenuItem value={"House of Blues"}>House of Blues</MenuItem>
            </Select>
        </FormControl>
    )
}

export default VenueSelect
