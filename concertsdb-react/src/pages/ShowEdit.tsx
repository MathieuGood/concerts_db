import React, { useEffect } from "react"
import {
    Typography,
    TextField,
    FormControl,
    InputLabel,
    Select,
    MenuItem,
    Box,
} from "@mui/material"
import { DemoContainer } from "@mui/x-date-pickers/internals/demo"
import { LocalizationProvider } from "@mui/x-date-pickers/LocalizationProvider"
import { AdapterDayjs } from "@mui/x-date-pickers/AdapterDayjs"
import { useState } from "react"
import { fetchShow } from "../services/showService"
import { DatePicker } from "@mui/x-date-pickers"
import daysjs from "dayjs"
import dayjs from "dayjs"

const ShowEdit: React.FC = () => {
    const showId = 1
    const [show, setShow] = useState([])

    useEffect(() => {
        fetchShow(showId).then((data) => {
            setShow(data)
            console.log(data)
            console.log(data.venue.name)
        })
    }, [])

    return (
        <Box>
            <Typography variant="h4" gutterBottom>
                Edit show
            </Typography>

            <TextField
                id="showName"
                label="Show name"
                variant="standard"
                value={show?.name || ""}
                onChange={(e) =>
                    setShow({ ...show, name: e.target.value } as Show)
                }
            />

            <LocalizationProvider dateAdapter={AdapterDayjs}>
                <DemoContainer components={["DateField"]}>
                    {/* Parse string show.event_date to Date object */}
                    <DatePicker
                        label="Show date"
                        value={show?.event_date ? dayjs(show.event_date) : null}
                        onChange={(date) =>
                            setShow({ ...show, event_date: date })
                        }
                    />
                </DemoContainer>
            </LocalizationProvider>

            <FormControl fullWidth>
                <InputLabel id="demo-simple-select-label">Venue</InputLabel>
                <Select
                    labelId="venue"
                    id="venue"
                    value={show?.venue?.name ? show.venue.name : ""}
                    label="Venue"
                    onChange={(e) =>
                        setShow({
                            ...show,
                            venue: { name: e.target.value },
                        } as Show)
                    }
                >
                    <MenuItem value={10}>The Fillmore</MenuItem>
                    <MenuItem value={20}>La Laiterie</MenuItem>
                    <MenuItem value={"E-Werk"}>E-Werk</MenuItem>
                </Select>
            </FormControl>
        </Box>
    )
}

export default ShowEdit
