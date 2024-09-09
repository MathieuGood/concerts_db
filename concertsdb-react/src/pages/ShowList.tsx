import React, { useEffect } from "react"

import { useState } from "react"
import { fetchShows } from "../requests"

const ShowList: React.FC = () => {
    const [shows, setShows] = useState([])
    useEffect(() => {
        fetchShows().then((data) => {
            setShows(data)
            console.log(data)
        })
    }, [])

    return (
        <div>
            <h1>Concerts I Have Been To</h1>
            <p>Here is the list</p>
            <p>Shows: {shows.length}</p>
            <table>
                <thead>
                    <tr>
                        <th>Date</th>
                        <th>Artist</th>
                        <th>Venue</th>
                        <th>City</th>
                        <th>Country</th>
                    </tr>
                </thead>
                <tbody>
                    {shows.map((show: any) => (
                        <tr key={show.id}>
                            <td>{show.date}</td>
                            <td>{show.artist}</td>
                            <td>{show.venue}</td>
                            <td>{show.city}</td>
                            <td>{show.country}</td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    )
}

export default ShowList
1
