import React, { useEffect, useState } from "react"
import { useParams } from "react-router-dom"
import { getShow } from "../services/showService"
import { Show } from "../models/Show"

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
		console.log(show)
	}, [show])

	return (
		<div className="">
			<h1>Show Edit</h1>
            <div>
                <span>Show id : {show?.id}</span>
                <span>Show </span>
                 </div>
		</div>
	)
}

export default ShowEdit
