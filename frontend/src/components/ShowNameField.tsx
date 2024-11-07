import React from "react"
import { TextField, FormControl } from "@mui/material"
import { Show } from "../models/Show"

interface ShowNameFieldProps {
    show: Show | null
    setShow: React.Dispatch<React.SetStateAction<Show | null>>
}

/**
 * ShowNameField component.
 *
 * @component
 * @param {Object} props - The component props.
 * @param {Show} props.show - The show object.
 * @param {function} props.setShow - The function to update the show object.
 * @returns {JSX.Element} The rendered ShowNameField component.
 */
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
