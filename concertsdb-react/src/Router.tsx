import React from "react"
import { BrowserRouter as Router, Route, Routes } from "react-router-dom"
import Home from "./pages/Home"
import ShowList from "./pages/ShowList"
import ShowEdit from "./pages/ShowEdit"

const App: React.FC = () => {
    return (
        <Router>
            <Routes>
                <Route path="/" element={<ShowList />} />
                <Route path="/edit/:id" element={<ShowEdit />} />
                <Route path="/home" element={<Home />} />
            </Routes>
        </Router>
    )
}

export default App
