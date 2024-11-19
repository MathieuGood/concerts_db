import { Show } from "../models/Show"
import { Artist } from "../models/Artist"
import {
	DataGrid,
	GridColDef,
	GridRenderEditCellParams,
	GridRowModel,
	GridRowsProp
} from "@mui/x-data-grid"
import DeleteIcon from "@mui/icons-material/Delete"
import { MenuItem, Select } from "@mui/material"
import { Concert } from "../models/Concert"

const ConcertDataGrid: React.FC<{
	show: Show
	setShow: (show: Show) => void
	artists: Artist[]
}> = ({ show, setShow, artists }) => {
	const handleArtistChange = (rowIndex: number, artistId: number) => {
		const updatedConcerts = show.concerts.map((concert, index) => {
			if (index === rowIndex) {
				return { ...concert, artist: artists.find(artist => artist.id === artistId) }
			}
			return concert
		})
		setShow({ ...show, concerts: updatedConcerts })
	}

	const handleProcessRowUpdate = (newRow: GridRowModel) => {
		const updatedConcerts = show.concerts.map(concert => {
			if (concert.id === newRow.id) {
				return { ...concert, ...newRow }
			}
			return concert
		})
		setShow({ ...show, concerts: updatedConcerts })
		return newRow
	}

	const renderArtistCell = (params: GridRenderEditCellParams) => {
		const concert = params.row as Concert
		const rowNumber = params.row.rowIndex
		return (
			<Select
				value={
					concert.artist?.id != undefined && artists.length > 0 ? concert.artist.id : ""
				}
				onChange={event => {
					handleArtistChange(rowNumber, Number(event.target.value))
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

	const renderDeleteCell = (params: GridRenderEditCellParams) => {
		return (
			<DeleteIcon
				onClick={() => {
					const updatedConcerts = show.concerts.filter(
						(concert, index) => index !== params.row.rowIndex
					)
					setShow({ ...show, concerts: updatedConcerts })
				}}
			/>
		)
	}

	const columns: GridColDef[] = [
		{ field: "id", headerName: "ID", width: 20 },
		{
			field: "artist",
			headerName: "Artist",
			width: 250,
			renderCell: params => renderArtistCell(params)
		},
		{ field: "comments", headerName: "Comments", minWidth: 200, maxWidth: 300, editable: true },
		{
			field: "photos",
			headerName: "Photos",
			width: 20,
			valueFormatter: (value: Array<string>) => value.length
		},
		{
			field: "videos",
			headerName: "Videos",
			width: 20,
			valueFormatter: (value: Array<string>) => value.length
		},
		{ field: "setlist", headerName: "Setlist", minWidth: 150, editable: true },
		{
			field: "actions",
			type: "actions",
			width: 20,
			renderCell: params => renderDeleteCell(params)
		}
	]

	const rows: GridRowsProp = show.concerts.map((concert, index) => {
		const concertRows = {
			id: concert.id || 0,
			rowIndex: index,
			artist: concert.artist,
			comments: concert.comments,
			photos: concert.photos,
			videos: concert.videos,
			setlist: concert.setlist
		}
		return concertRows
	})

	return <DataGrid columns={columns} rows={rows} processRowUpdate={handleProcessRowUpdate} />
}

export default ConcertDataGrid
