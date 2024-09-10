import React from "react"
import { TextField, FormControl } from "@mui/material"
import { Show } from "../models/Show"

interface ShowNameFieldProps {
    show: Show | null
    setShow: React.Dispatch<React.SetStateAction<Show | null>>
}

const ShowNameField: React.FC<ShowNameFieldProps> = ({ show, setShow }) => {
    return (
        <FormControl fullWidth margin="normal">
            <TextField
                id="showName"
                label="Show name"
                value={show?.name || ""}
                variant="standard"
                onChange={(e) =>
                    setShow({ ...show, name: e.target.value } as Show)
                }
            />
        </FormControl>
    )
}

export default ShowNameField
