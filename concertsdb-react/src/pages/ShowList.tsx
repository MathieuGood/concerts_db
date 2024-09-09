import React, { useEffect } from "react"
import {
    Table,
    TableBody,
    TableCell,
    TableContainer,
    TableHead,
    TableRow,
    Paper,
} from "@mui/material"
import { useState } from "react"
import { fetchShows } from "../requests"

const ShowList: React.FC = () => {
    const [shows, setShows] = useState([])
    useEffect(() => {
        fetchShows().then((data) => {
            setShows(data)
        })
    }, [])

    return (
        <div className="container">
            <h1 className="underline">Concerts I Have Been To</h1>
            <table className="table-auto">
                <thead>
                    <tr></tr>
                </thead>
                <tbody>{}</tbody>
            </table>

            <TableContainer component={Paper}>
                <Table sx={{ minWidth: 650 }} aria-label="simple table">
                    <TableHead>
                        <TableRow>
                            <TableCell>Date</TableCell>
                            <TableCell>Venue</TableCell>
                            <TableCell>City</TableCell>
                            <TableCell>Country</TableCell>
                            <TableCell>Artists</TableCell>
                        </TableRow>
                    </TableHead>
                    <TableBody>
                        {shows.map((show: any) => {
                            return (
                                <TableRow key={show.id}>
                                    <TableCell>{show.event_date}</TableCell>

                                    <TableCell>{show.venue.name}</TableCell>
                                    <TableCell>
                                        {show.venue.address.city}
                                    </TableCell>
                                    <TableCell>
                                        {show.venue.address.country}
                                    </TableCell>
                                    <TableCell>
                                        {show.concerts.map((concert: any) => {
                                            return (
                                                <div key={concert.artist.id}>
                                                    <span>
                                                        {concert.artist.name}
                                                    </span>
                                                </div>
                                            )
                                        })}
                                    </TableCell>
                                </TableRow>
                            )
                        })}
                    </TableBody>
                </Table>
            </TableContainer>
        </div>
    )
}

export default ShowList
