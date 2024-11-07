import React from "react"
import {
    BrowserRouter as Router,
    Route,
    Routes,
    useParams,
} from "react-router-dom"
import Home from "./pages/Home"
import ShowList from "./pages/ShowList"
import ShowEdit from "./pages/ShowEdit"

const App: React.FC = () => {
    return (
        <Router>
            <Routes>
                <Route path="/" element={<ShowList />} />
                <Route path="/edit/:id" element={<ShowEditWrapper />} />
                <Route path="/home" element={<Home />} />
            </Routes>
        </Router>
    )
}

const ShowEditWrapper: React.FC = () => {
    const params = useParams<{ id: string }>()
    const showId = params.id ? parseInt(params.id) : 0
    return <ShowEdit showId={showId} />
}

export default App
