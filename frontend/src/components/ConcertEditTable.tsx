import { Show } from "../models/Show"
import { Artist } from "../models/Artist"
import ConcertArtistSelect from "./ConcertArtistSelect"
import ConcertCommentsTextField from "./ConcertCommentsTextField"

const ConcertEditTable: React.FC<{
	show?: Show
	setShow: (show: Show) => void
	artists: Artist[]
}> = ({ show, setShow, artists }) => {
	return (
		<table className="table-auto">
			<thead>
				<tr>
					<th className="px-4 py-2">Artist</th>
					<th className="px-4 py-2">Comments</th>
					<th className="px-4 py-2">Photos</th>
					<th className="px-4 py-2">Videos</th>
					<th className="px-4 py-2">Setlist</th>
				</tr>
			</thead>
			<tbody>
				{show?.concerts.map(concert => (
					<tr key={concert.id}>
						<td className="border px-4 py-2">
							<ConcertArtistSelect
								show={show}
								setShow={setShow}
								concert={concert}
								artists={artists}
							/>
						</td>
						<td className="border px-4 py-2">
							<ConcertCommentsTextField
								show={show}
								setShow={setShow}
								concert={concert}
							/>
						</td>

						<td className="border px-4 py-2">{concert.photos.length}</td>
						<td className="border px-4 py-2">{concert.videos.length}</td>
						<td className="border px-4 py-2">{concert.setlist}</td>
					</tr>
				))}
			</tbody>
		</table>
	)
}

export default ConcertEditTable
