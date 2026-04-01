import { DataGrid, GridColDef, GridRowsProp } from "@mui/x-data-grid"
import { getShows } from "../services/showService"
import { useEffect, useState } from "react"
import { Show } from "../models/Show"

const ShowList: React.FC = () => {
	const [shows, setShows] = useState<Show[]>([])

	const columns: GridColDef[] = [
		{ field: "id", headerName: "ID", width: 20 },
		{ field: "eventDate", headerName: "Event Date", width: 88 },
		{ field: "name", headerName: "Name", flex: 1 },
		{ field: "festival", headerName: "Festival", flex: 1 },
		{ field: "comments", headerName: "Comments", flex: 1 },
		{ field: "concertsCount", headerName: "Concerts", width: 20 },
		{ field: "artists", headerName: "Artists", flex: 1 },
		{ field: "venueName", headerName: "Venue Name", flex: 1 },
		{ field: "venueCity", headerName: "Venue City", flex: 1 },
		{ field: "venueCountry", headerName: "Venue Country", flex: 1 },
		{ field: "attendees", headerName: "Attendees", flex: 1 }
	]

	const buildRows: GridRowsProp = shows.map(show => {
		return {
			id: show.id,
			eventDate: show.event_date,
			name: show.name,
			festival: show.festival?.name,
			comments: show.comments,
			concertsCount: show.concerts.length,
			artists: show.concerts.map(concert => concert.artist?.name).join(", "),
			venueName: show.venue?.name,
			venueCity: show.venue?.address?.city,
			venueCountry: show.venue?.address?.country,
			attendees: show.attendees?.length
				? show.attendees
						.map(attendee => attendee.firstname + " " + attendee.lastname)
						.join(", ")
				: ""
		}
	})

	useEffect(() => {
		getShows().then(shows => {
			setShows(shows)
		})
	}, [])

	return (
		<div className="">
			<h1 className="text-2xl">List of Shows</h1>
			<div className="h-80 w-full">
				<DataGrid
					rows={buildRows}
					columns={columns}
					onRowDoubleClick={row => {
						console.log("Row clicked", row.row.id)
						window.location.href = `/edit/${row.row.id}`
					}}
					className="bg-white shadow-md rounded-lg"
					sx={{
						"& .MuiDataGrid-cell": {
							fontSize: "0.70rem"
						},
						"& .MuiDataGrid-columnHeaderTitle": {
							fontSize: "0.70rem"
						}
					}}
				/>
			</div>
		</div>
	)
}

export default ShowList
