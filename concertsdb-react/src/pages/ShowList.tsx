import React, { useEffect } from "react"

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
            <h1>Concerts I Have Been To</h1>
            <p>Here is the list</p>
            <p>Shows: {shows.length}</p>
            <table className="table-auto">
                <thead>
                    <tr>
                        <th>Date</th>
                        <th>Venue</th>
                        <th>City</th>
                        <th>Country</th>
                        <th>Artists</th>
                    </tr>
                </thead>
                <tbody>
                    {shows.map((show: any) => {
                        console.log(">>> Show >>>")
                        console.log("  > ID: " + show.id)
                        console.log("  > Date: " + show.event_date)
                        console.log("  > Venue: " + show.venue.name)
                        console.log("  > City: " + show.venue.address.city)
                        console.log(
                            "  > Country: " + show.venue.address.country
                        )

                        return (
                            <tr key={show.id}>
                                <td>{show.event_date}</td>
                                <td>{show.venue.name}</td>
                                <td>{show.venue.address.city}</td>
                                <td>{show.venue.address.country}</td>
                                <td>
                                    {show.concerts.map((concert: any) => {
                                        return (
                                            <span key={concert.artist.id}>
                                                {concert.artist.name}
                                            </span>
                                        )
                                    })}
                                </td>
                            </tr>
                        )
                    })}
                </tbody>
            </table>
        </div>
    )
}

export default ShowList
1
