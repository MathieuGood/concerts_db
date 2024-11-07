/**
 * Save button component.
 *
 * This component renders a button with a save icon.
 *
 * @returns The SaveButton component.
 */
import React from "react"
import { Button } from "@mui/material"
import SaveIcon from "@mui/icons-material/Save"

const SaveButton: React.FC = () => {
    return (
        <Button variant="contained" endIcon={<SaveIcon />}>
            Save show
        </Button>
    )
}

export default SaveButton
