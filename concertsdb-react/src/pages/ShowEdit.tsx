import React from "react"
import { Typography, Box, Paper, Stack } from "@mui/material"
import { useState, useEffect } from "react"
import { fetchShow } from "../services/showService"
import { Show } from "../models/Show"
import ShowNameField from "../components/ShowNameField"
import ShowDateField from "../components/ShowDateField"
import VenueSelect from "../components/VenueSelect"
import FestivalSelect from "../components/FestivalSelect"
import CommentsField from "../components/CommentsField"
import SaveButton from "../components/SaveButton"
import BackButton from "../components/BackButton"

/**
 * ShowEdit page is used to create and edit shows.
 *
 * @returns The ShowEdit page.
 */

// Add an id parameter to the ShowEdit component
// The id parameter is a number
interface ShowEditProps {
    showId: number
}
const ShowEdit: React.FC<ShowEditProps> = ({ showId }) => {
    const [show, setShow] = useState<Show | null>(null)

    useEffect(() => {
        fetchShow(showId).then((data: Show) => {
            setShow(data)
        })
    }, [])

    return (
        <Box sx={{ display: "flex", justifyContent: "center", mt: 2 }}>
            <Paper elevation={3} sx={{ p: 4, width: "100%", maxWidth: 600 }}>
                <Typography variant="h4" gutterBottom>
                    Edit Show
                </Typography>
                <Stack spacing={3}>
                    <ShowNameField show={show} setShow={setShow} />
                    <ShowDateField show={show} setShow={setShow} />
                    <VenueSelect show={show} setShow={setShow} />
                    <FestivalSelect show={show} setShow={setShow} />
                    <CommentsField show={show} setShow={setShow} />
                    <Box sx={{ display: "flex", justifyContent: "center" }}>
                        <BackButton />
                        <Box sx={{ width: 16 }} />
                        <SaveButton />
                    </Box>
                </Stack>
            </Paper>
        </Box>
    )
}

export default ShowEdit
