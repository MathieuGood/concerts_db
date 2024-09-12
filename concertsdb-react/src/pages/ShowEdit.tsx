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
import ConcertsDataGrid from "../components/ConcertsDataGrid"
import { DataGrid, GridColDef } from "@mui/x-data-grid"

/**
 * ShowEdit page is used to create and edit shows.
 *
 * @returns The ShowEdit page.
 */

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

    const rows = [
        {
            id: 1,
            artist: "Snow",
            comments: "Jon",
            setlist: "",
            photos: "",
            videos: "",
        },
        {
            id: 2,
            artist: "Lannister",
            comments: "Cersei",
            setlist: "",
            photos: "",
            videos: "",
        },
        {
            id: 3,
            artist: "Lannister",
            comments: "Jaime",
            setlist: "",
            photos: "",
            videos: "",
        },
        {
            id: 4,
            artist: "Stark",
            comments: "Arya",
            setlist: "",
            photos: "",
            videos: "",
        },
        {
            id: 5,
            artist: "Targaryen",
            comments: "Daenerys",
            setlist: "",
            photos: "",
            videos: "",
        },
        {
            id: 6,
            artist: "Melisandre",
            comments: "",
            setlist: "",
            photos: "",
            videos: "",
        },
        {
            id: 7,
            artist: "Clifford",
            comments: "Ferrara",
            setlist: "",
            photos: "",
            videos: "",
        },
        {
            id: 8,
            artist: "Frances",
            comments: "Rossini",
            setlist: "",
            photos: "",
            videos: "",
        },
        { id: 9, artist: "Roxie", comments: "Harvey" },
    ]

    const columns: GridColDef<(typeof rows)[number]>[] = [
        {
            field: "artist",
            headerName: "Artist",
            width: 150,
            editable: true,
            sortable: true,
        },
        {
            field: "comments",
            headerName: "Comments",
            // width: 150,
            editable: true,
            sortable: false,
        },
        {
            field: "setlist",
            headerName: "Setlist",
            // width: 110,
            editable: true,
            description: "Songs played at the concert",
            sortable: false,
        },
        {
            field: "photos",
            headerName: "Photos",
            // width: 160,
            description: "Photos of the concert",
            sortable: false,
        },
        {
            field: "videos",
            headerName: "Videos",
            // width: 160,
            description: "Videos of the concert",
            sortable: false,
        },
    ]

    return (
        <Box sx={{ display: "flex", justifyContent: "center", mt: 2 }}>
            <Paper elevation={3} sx={{ p: 4, width: "100%", maxWidth: 800 }}>
                <Typography variant="h4" gutterBottom>
                    Edit Show
                </Typography>
                <Stack spacing={3}>
                    <ShowNameField show={show} setShow={setShow} />
                    <ShowDateField show={show} setShow={setShow} />
                    <VenueSelect show={show} setShow={setShow} />
                    <FestivalSelect show={show} setShow={setShow} />
                    <CommentsField show={show} setShow={setShow} />

                    <Box sx={{ height: "auto", width: "100%" }}>
                        <DataGrid
                            rows={rows}
                            columns={columns}
                            disableRowSelectionOnClick
                        />
                    </Box>

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
