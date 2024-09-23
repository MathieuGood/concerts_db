const showWithIds = {
	name: "Emo Glam 666",
	event_date: "2006-06-06",
	comments: "Soirée présentée par Thomas VDB",

	venue_id: 12,

	attendees_ids: [1, 2],

	concerts_ids: [1, 2, 3]
}

const showWithCompleteConcert = {
	name: "Emo Glam 666",
	event_date: "2006-06-06",
	comments: "Soirée présentée par Thomas VDB",
	venue_id: 12,
	festival_id: null,
	attendees_ids: [1, 2],
	concerts: [
		{
			artist_id: 1,
			comments: "Concert de 20h",
			setlist: "Song 1, Song 2",
			photos: ["Photo1", "Photo2"],
			videos: ["Video1", "Video2"]
		},
		{
			artist_id: 3,
			comments: "Concert de 21h",
			setlist: "Song 3, Song 4",
			photos: ["Photo3", "Photo4"],
			videos: ["Video3", "Video4"]
		}
	]
}

const createVenue = {
	name: "La Maroquinerie",
	address_id: "2"
}

const createAttendee = {
	first_name: "John",
	last_name: "Doe"
}

const createArtist = {
	name: "The Beatles",
	address_id: "1"
}

const createAddress = {
	city: "Paris",
	country: "France"
}
