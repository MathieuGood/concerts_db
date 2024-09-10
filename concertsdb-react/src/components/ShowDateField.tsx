import React from "react"
import { FormControl } from "@mui/material"
import { DatePicker } from "@mui/x-date-pickers/DatePicker"
import { LocalizationProvider } from "@mui/x-date-pickers/LocalizationProvider"
import { AdapterDayjs } from "@mui/x-date-pickers/AdapterDayjs"
import dayjs, { Dayjs } from "dayjs"
import { Show } from "../models/Show"

interface ShowDateFieldProps {
    show: Show | null
    setShow: React.Dispatch<React.SetStateAction<Show | null>>
}

/**
 * ShowDateField component.
 *
 * This component is responsible for rendering a date picker field for a show date.
 *
 * @component
 * @example
 * ```tsx
 * <ShowDateField show={show} setShow={setShow} />
 * ```
 *
 * @param {Object} props - The component props.
 * @param {Show} props.show - The show object.
 * @param {Function} props.setShow - The function to update the show object.
 * @returns {JSX.Element} The rendered ShowDateField component.
 */
const ShowDateField: React.FC<ShowDateFieldProps> = ({ show, setShow }) => {
    const handleDateChange = (date: Dayjs | null) => {
        if (date) {
            setShow({ ...show, event_date: date.toISOString() } as Show)
        }
    }

    return (
        <FormControl fullWidth margin="normal">
            <LocalizationProvider dateAdapter={AdapterDayjs}>
                <DatePicker
                    label="Show date"
                    value={show?.event_date ? dayjs(show.event_date) : null}
                    onChange={handleDateChange}
                />
            </LocalizationProvider>
        </FormControl>
    )
}

export default ShowDateField
