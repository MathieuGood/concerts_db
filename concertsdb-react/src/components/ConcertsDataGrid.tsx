import React, { useEffect } from "react"
import { DataGrid, GridColDef } from "@mui/x-data-grid"
import { Box } from "@mui/material"
import { Show } from "../models/Show"

interface ConcertsDataGridProps {
    show: Show | null
}

const ConcertsDataGrid: React.FC<ConcertsDataGridProps> = ({ show }) => {
    const [concertsRows, setConcertsRows] = React.useState<any[]>([])

    useEffect(() => {
        if (show) {
            const parsedRows = parseShowsToConcertsRows(show)
            setConcertsRows(parsedRows)
        }
    }, [show])

    const parseShowsToConcertsRows = (show: Show) => {
        const parsedRows = show.concerts.map((concert) => {
            return {
                id: concert.id,
                artist: concert.artist?.name,
                comments: concert.comments,
                setlist: concert.setlist,
                photos: concert.photos,
                videos: concert.videos,
            }
        })
        return parsedRows
    }

    const columns: GridColDef[] = [
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
            editable: true,
            sortable: false,
            disableColumnMenu: true,
        },
        {
            field: "setlist",
            headerName: "Setlist",
            editable: true,
            description: "Songs played at the concert",
            sortable: false,
            disableColumnMenu: true,
        },
        {
            field: "photos",
            headerName: "📷",
            editable: false,
            sortable: false,
            disableColumnMenu: true,
        },
        {
            field: "videos",
            headerName: "🎬",
            editable: false,
            sortable: false,
            disableColumnMenu: true,
        },
    ]

    console.log("Show data in ConcertsDataGrid component:")
    console.log(show)
    return (
        <Box sx={{ height: "auto", width: "100%" }}>
            <DataGrid
                rows={concertsRows}
                columns={columns}
                disableRowSelectionOnClick
            />
        </Box>
    )
}

export default ConcertsDataGrid
