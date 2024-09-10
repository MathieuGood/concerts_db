/**
 * Back button component.
 */
import React from "react"
import { Button } from "@mui/material"
import ArrowBackIosNewIcon from "@mui/icons-material/ArrowBackIosNew"

const BackButton: React.FC = () => {
    return (
        <Button
            variant="contained"
            color="error"
            startIcon={<ArrowBackIosNewIcon />}
        >
            Back
        </Button>
    )
}

export default BackButton
