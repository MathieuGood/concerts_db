import React from "react"
import { FormControl, InputLabel, Select, MenuItem } from "@mui/material"
import { Show } from "../models/Show"

interface FestivalSelectProps {
    show: Show | null
    setShow: React.Dispatch<React.SetStateAction<Show | null>>
}

const FestivalSelect: React.FC<FestivalSelectProps> = ({ show, setShow }) => {
    return (
        <FormControl fullWidth margin="normal">
            <InputLabel id="festival-label">Festival</InputLabel>
            <Select
                labelId="festival-label"
                id="festival"
                value={show?.festival?.name ? show.festival.name : ""}
                label="Festival"
                onChange={(e) =>
                    setShow({
                        ...show,
                        festival: { name: e.target.value },
                    } as Show)
                }
            >
                <MenuItem value={"Groezrock"}>Groezrock</MenuItem>
                <MenuItem value={"Hellfest"}>Hellfest</MenuItem>
                <MenuItem value={"Dour Festival"}>Dour Festival</MenuItem>
            </Select>
        </FormControl>
    )
}

export default FestivalSelect
