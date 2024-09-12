import React from "react"
import { DataGrid, GridColDef } from "@mui/x-data-grid"
import { Box } from "@mui/material"
import { Show } from "../models/Show"

interface ConcertsDataGridProps {
    show: Show | null
    setShow: React.Dispatch<React.SetStateAction<Show | null>>
}

const ConcertsDataGrid: React.FC<ConcertsDataGridProps> = ({
    show,
    setShow,
}) => {
    console.log("Show data in ConcertsDataGrid component:")
    console.log(show)
    return (
        <Box sx={{ height: "auto", width: "100%" }}>
            <DataGrid rows={[]} columns={[]} disableRowSelectionOnClick />
        </Box>
    )
}

export default ConcertsDataGrid
