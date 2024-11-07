import React, { useEffect, useState } from "react"
import { useParams } from "react-router-dom"
import { getShow } from "../services/showService"
import { Show } from "../models/Show"
import { DatePicker } from "@mui/x-date-pickers/DatePicker"
import dayjs from "dayjs"
import { Button, MenuItem, Select, TextField } from "@mui/material"

const ShowEdit: React.FC = () => {
	const { showId } = useParams<{ showId: string }>()
	const [show, setShow] = useState<Show>()

	useEffect(() => {
		console.log(`Show Edit for ID ${showId}`)
		if (showId) {
			getShow(Number(showId)).then(show => {
				setShow(show)
				console.log(show)
			})
		}
	}, [showId])

	useEffect(() => {
		// Get all festivals
		console.log("Get all festivals")
		console.log("Current festival of show", show?.festival)
	}, [show])

	useEffect(() => {
		console.log("Show name :", show?.name)
	}, [show])

	return (
		<div className="p-4 max-w-[1080px]">
			<div className="flex flex-row gap-5 mb-4">
				<h1 className="text-2xl font-bold">Show Edit</h1>
				<Button href={"/list"}>Back to list</Button>
			</div>
			<table className="table-auto w-full">
				<tbody>
					<tr>
						<td className="font-semibold w-1 whitespace-nowrap pr-6">Show id</td>
						<td>{show?.id}</td>
					</tr>
					<tr>
						<td className="font-semibold w-1 whitespace-nowrap pr-6">Date</td>
						<td>
							<DatePicker
								label="Event date"
								value={show?.event_date ? dayjs(show.event_date) : null}
								onChange={date => {
									setShow({ ...show, event_date: date?.toISOString() } as Show)
								}}
							/>
						</td>
					</tr>
					<tr>
						<td className="font-semibold w-1 whitespace-nowrap pr-6">Name</td>
						<td>
							<TextField
								value={show?.name}
								onChange={name => {
									setShow({ ...show, name: name.target.value } as Show)
								}}
							/>
						</td>
					</tr>
					<tr>
						<td className="font-semibold w-1 whitespace-nowrap pr-6">Festival</td>
						<td>
							<Select
								value={show?.festival ? show?.festival?.id : ""}
								label={show?.festival ? show?.festival?.name : ""}
								onChange={event => {
									const selectedFestival = event.target.value
									console.log("Selected festival", selectedFestival)
									setShow({
										...show,
										festival: { id: selectedFestival, name: selectedFestival }
									} as Show)
									console.log("Show after setting festival", show?.festival)
								}}>
								<MenuItem value="V1">Valeur 1</MenuItem>
								<MenuItem value={undefined}>!UNDEFINED!</MenuItem>
								<MenuItem value="1">Punk In Drublic</MenuItem>
							</Select>
						</td>
					</tr>
					<tr>
						<td className="font-semibold w-1 whitespace-nowrap pr-6">Comments</td>
						<td>
							{" "}
							<TextField
								value={show?.comments}
								onChange={comments => {
									setShow({ ...show, name: comments.target.value } as Show)
								}}
							/>
						</td>
					</tr>
					<tr>
						<td className="font-semibold w-1 whitespace-nowrap pr-6">Concerts count</td>
						<td>{show?.concerts.length}</td>
					</tr>
					<tr>
						<td className="font-semibold w-1 whitespace-nowrap pr-6">Artists</td>
						<td>{show?.concerts.map(concert => concert.artist?.name).join(", ")}</td>
					</tr>
					<tr>
						<td className="font-semibold w-1 whitespace-nowrap pr-6">Venue name</td>
						<td>{show?.venue?.name}</td>
					</tr>
					<tr>
						<td className="font-semibold w-1 whitespace-nowrap pr-6">Venue city</td>
						<td>{show?.venue?.address?.city}</td>
					</tr>
					<tr>
						<td className="font-semibold w-1 whitespace-nowrap pr-6">Venue country</td>
						<td>{show?.venue?.address?.country}</td>
					</tr>
					<tr>
						<td className="font-semibold w-1 whitespace-nowrap pr-6">Attendees</td>
						<td>
							{show?.attendees
								.map(attendee => attendee.firstname + " " + attendee.lastname)
								.join(", ")}
						</td>
					</tr>
				</tbody>
			</table>
		</div>
	)
}

export default ShowEdit
