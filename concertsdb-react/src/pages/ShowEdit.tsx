import React from "react"
import { Typography, Box } from "@mui/material"
import { useState, useEffect } from "react"
import { fetchShow } from "../services/showService"
import { Show } from "../models/Show"
import ShowNameField from "../components/ShowNameField"
import ShowDateField from "../components/ShowDateField"
import VenueSelect from "../components/VenueSelect"
import FestivalSelect from "../components/FestivalSelect"
import CommentsField from "../components/CommentsField"
import SaveButton from "../components/SaveButton"

const ShowEdit: React.FC = () => {
    const showId = 1
    const [show, setShow] = useState<Show | null>(null)

    useEffect(() => {
        fetchShow(showId).then((data: Show) => {
            setShow(data)
        })
    }, [])

    return (
        <Box>
            <Typography variant="h4" gutterBottom>
                Edit show
            </Typography>
            <ShowNameField show={show} setShow={setShow} />
            <ShowDateField show={show} setShow={setShow} />
            <VenueSelect show={show} setShow={setShow} />
            <FestivalSelect show={show} setShow={setShow} />
            <CommentsField show={show} setShow={setShow} />
            <SaveButton />
        </Box>
    )
}

export default ShowEdit
