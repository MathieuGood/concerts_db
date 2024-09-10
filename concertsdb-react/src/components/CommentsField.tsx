import React from "react"
import { TextField, FormControl } from "@mui/material"
import { Show } from "../models/Show"

interface CommentsFieldProps {
    show: Show | null
    setShow: React.Dispatch<React.SetStateAction<Show | null>>
}

/**
 * CommentsField component.
 *
 * @component
 * @param {Object} props - The component props.
 * @param {boolean} props.show - The show prop.
 * @param {function} props.setShow - The setShow prop.
 * @returns {JSX.Element} The rendered CommentsField component.
 */
const CommentsField: React.FC<CommentsFieldProps> = ({ show, setShow }) => {
    return (
        <FormControl fullWidth margin="normal">
            <TextField
                id="comments"
                label="Comments"
                multiline
                fullWidth
                rows={4}
                variant="standard"
                value={show?.comments ? show.comments : ""}
                onChange={(e) =>
                    setShow({ ...show, comments: e.target.value } as Show)
                }
            />
        </FormControl>
    )
}

export default CommentsField
