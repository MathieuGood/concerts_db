import React, { useEffect } from "react"
import {
    Table,
    TableBody,
    TableCell,
    TableContainer,
    TableHead,
    TableRow,
    Paper,
    Typography,
} from "@mui/material"
import { useState } from "react"
import { fetchShows } from "../services/showService"

const ShowList: React.FC = () => {
    const [shows, setShows] = useState([])

    useEffect(() => {
        fetchShows().then((data) => {
            setShows(data)
        })
    }, [])

    return (
        <div>
            <div style={{ display: "flex", alignSelf: "center" }}>
                <img
                    src="/assets/concertsdb-logo.svg"
                    style={{ width: "50px" }}
                />
                <Typography variant="h4" gutterBottom>
                    Concerts I Have Been To
                </Typography>
            </div>

            <TableContainer component={Paper}>
                <Table sx={{ minWidth: 300 }}>
                    <TableHead>
                        <TableRow>
                            <TableCell></TableCell>
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
                                    <TableCell style={{ width: "1%" }}>
                                        <a href={`/edit/${show.id}`}>
                                            <img
                                                src="/assets/music-library.svg"
                                                style={{ width: "25px" }}
                                            />
                                        </a>
                                    </TableCell>
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
