import React, { useEffect, useState } from "react"
import { useParams } from "react-router-dom"
import { getShow, parseShowToAPIFormat, updateShow } from "../services/showService"
import { Show } from "../models/Show"
import { DatePicker } from "@mui/x-date-pickers/DatePicker"
import dayjs from "dayjs"
import { Button, TextField } from "@mui/material"
import { getVenues } from "../services/venueService"
import { getFestivals } from "../services/festivalService"
import { Festival } from "../models/Festival"
import { Venue } from "../models/Venue"
import FestivalSelect from "../components/FestivalSelect"
import ShowEditRow from "../components/ShowEditRow"
import VenueSelect from "../components/VenueSelect"
import AttendeeMultiSelect from "../components/AttendeeMultiSelect"
import { Attendee } from "../models/Attendee"
import { getAttendees } from "../services/attendeeService"
import { getArtists } from "../services/artistService"
import { Artist } from "../models/Artist"
import ConcertsDataGrid from "../components/ConcertsDataGrid"

const ShowEdit: React.FC = () => {
	const { showId } = useParams<{ showId: string }>()
	const [show, setShow] = useState<Show>()
	const [error, setError] = useState<string>()
	const [festivals, setFestivals] = useState<Festival[]>([])
	const [venues, setVenues] = useState<Venue[]>([])
	const [attendees, setAttendees] = useState<Attendee[]>([])
	const [artists, setArtists] = useState<Artist[]>([])

	const isValidForm = (show: Show): boolean => {
		console.log(show)

		// Check if there are no empty concerts
		show.concerts.map((concert) => {
			return !isEmpty(concert.artist)
		})

		return true
	}

	const isEmpty = (inputValue: string | Artist): boolean => {
		if (typeof inputValue === "object") {
			if (Object.keys(inputValue).length === 0) {
				setError("ALAAAAAAARMA")
				return true
			}

			if (error?.length > 0) {
				setError("")
			}

			return false
		}

		return inputValue.length === 0
	}

	const isMaxLength = (inputValue: string, maxLength: number): boolean => {
		return inputValue.length > maxLength
	}

	const saveShow = (show: Show) => {
		if (!isValidForm(show)) return
		updateShow(show)
			.then(response => {
				console.log(response)
				return getShow(Number(showId))
			})
			.then(show => {
				setShow(show)
				console.log(
					`Loading show ${show.id} / ${show.event_date} / ${show.venue?.name} / ${show.venue?.address?.city}, ${show.venue?.address?.country}`
				)
			})
	}

	const updateAllSelectContent = () => {
		getVenues().then(venues => {
			setVenues(venues)
		})
		getFestivals().then(festivals => {
			setFestivals(festivals)
		})
		getAttendees().then(attendees => {
			setAttendees(attendees)
		})
		getArtists().then(artists => {
			setArtists(artists)
		})
	}

	const addEmptyConcert = () => {
		if (show) {
			const newId = () => {
				let minId = 0
				show.concerts.forEach(concert => {
					if (concert.id !== undefined && concert.id < minId) {
						minId = concert.id
					}
				})
				console.log("minId IS", minId)
				return minId - 1
			}

			const newConcert = {
				id: newId(),
				show_id: show.id,
				artist: {} as Artist,
				comments: "",
				setlist: "",
				photos: [],
				videos: []
			}
			setShow({ ...show, concerts: [...show.concerts, newConcert] })
		}
	}

	useEffect(() => {
		if (showId) {
			getShow(Number(showId)).then(show => {
				setShow(show)
				console.log(
					`Loading show ${show.id} / ${show.event_date} / ${show.venue?.name} / ${show.venue?.address?.city}, ${show.venue?.address?.country}`
				)
			})
		}
		updateAllSelectContent()
	}, [showId])

	useEffect(() => {
		console.log(`Show updated ${new Date().toISOString()}`, show)
	}, [show])

	return (
		<div className="p-4 max-w-[1080px]">
			{error && <p className="text-red-600 text-2xl font-bold">{error}</p>}
			<div className="flex flex-row gap-5 mb-4">
				<h1 className="text-2xl font-bold">Show Edit</h1>
				<Button href={"/list"}>Back to list</Button>
			</div>
			<table className="table-auto w-full">
				<tbody>
					<ShowEditRow label="ID">{show?.id}</ShowEditRow>

					<ShowEditRow label="Date">
						<DatePicker
							label="Event date"
							value={show?.event_date ? dayjs(show.event_date) : null}
							onChange={date => {
								setShow({ ...show, event_date: date?.toISOString() } as Show)
							}}
						/>
					</ShowEditRow>

					<ShowEditRow label="Name">
						<TextField
							value={show?.name || ""}
							onChange={name => {
								setShow({ ...show, name: name.target.value } as Show)
							}}
						/>
					</ShowEditRow>

					<ShowEditRow label="Festival">
						<FestivalSelect show={show} setShow={setShow} festivals={festivals} />
					</ShowEditRow>

					<ShowEditRow label="Venue">
						<VenueSelect show={show} setShow={setShow} venues={venues} />
					</ShowEditRow>

					<ShowEditRow label="Venue info">
						{`${show?.venue?.name} / ${show?.venue?.address?.city}, ${show?.venue?.address?.country}`}
					</ShowEditRow>

					<ShowEditRow label="Comments">
						<TextField
							value={show?.comments || ""}
							onChange={comments => {
								setShow({ ...show, comments: comments.target.value } as Show)
							}}
						/>
					</ShowEditRow>

					<ShowEditRow label="Attendees">
						<AttendeeMultiSelect show={show} setShow={setShow} attendees={attendees} />
					</ShowEditRow>
				</tbody>
			</table>

			<Button
				onClick={() => {
					addEmptyConcert()
				}}>
				Add concert
			</Button>

			{show !== undefined && (
				<ConcertsDataGrid show={show} setShow={setShow} artists={artists} />
			)}
			<Button
				onClick={() => {
					if (show) {
						parseShowToAPIFormat(show)
						saveShow(show!)
					}
				}}>
				Save show
			</Button>
		</div>
	)
}

export default ShowEdit
