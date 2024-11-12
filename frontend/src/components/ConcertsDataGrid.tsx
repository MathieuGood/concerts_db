import { Show } from "../models/Show"
import { Artist } from "../models/Artist"
import { DataGrid, GridColDef, GridRenderEditCellParams, GridRowsProp } from "@mui/x-data-grid"
import { MenuItem, Select } from "@mui/material"

const ConcertDataGrid: React.FC<{
	show: Show
	setShow: (show: Show) => void
	artists: Artist[]
}> = ({ show, setShow, artists }) => {
	const handleArtistChange = (concertId: number, artistId: string) => {
		// Not implemented yet
		console.log(`Change the artist to concertId < ${concertId} > and artistId < ${artistId} >`)
		
	}

	const renderArtistCell = (index: number) => {
		const concert = show.concerts[index]
		console.log("UNDEFINED CONCERTS?", show.concerts)
		console.log("UNDEFINED ARTIST?", concert)
		console.log(`Render artistCell with index ${index}: ${concert.artist}`)
		if (!concert) {
			return <span> NO CONCERT</span>
		}
		return (
			<Select
				value={concert.artist != undefined && artists.length > 0 ? concert.artist.id : ""}
				onChange={event => {
					console.log("Artist CHANGE :", index, event.target.value)
					// handleArtistChange(index, event.target.value)
				}}
				fullWidth
				variant="standard">
				{artists.map(artist => (
					<MenuItem key={artist.id} value={artist.id}>
						{artist.name}
					</MenuItem>
				))}
			</Select>
		)
	}

	const columns: GridColDef[] = [
		{ field: "id", headerName: "ID", width: 20 },
		{
			field: "artist",
			headerName: "Artist",
			width: 250,
			renderCell: params => {
				renderArtistCell
			},
			renderEditCell: (params:GridRenderEditCellParams) => {
                
            }
		},
		{ field: "comments", headerName: "Comments", minWidth: 150, maxWidth: 300 },
		{ field: "photos", headerName: "Photos", width: 20 },
		{ field: "videos", headerName: "Videos", width: 20 },
		{ field: "setlist", headerName: "Setlist", minWidth: 150, maxWidth: 300 }
	]

	const rows: GridRowsProp = show.concerts.map(concert => {
		const concertRows = {
			id: concert.id || 0,
			artist: concert.artist?.name,
			comments: concert.comments,
			photos: concert.photos.length,
			videos: concert.videos.length,
			setlist: concert.setlist
		}
		console.log("concertRows", concertRows)
		return concertRows
	})

	return <DataGrid columns={columns} rows={rows} />
}

export default ConcertDataGrid
