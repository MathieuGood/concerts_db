import { StrictMode } from "react"
import { createRoot } from "react-dom/client"
import { createBrowserRouter, RouterProvider } from "react-router-dom"
import "./index.css"
import ShowList from "./pages/ShowList.tsx"
import ShowEdit from "./pages/ShowEdit.tsx"
import "dayjs/locale/fr"
import { Navigate } from "react-router-dom"
import { LocalizationProvider } from "@mui/x-date-pickers"
import { AdapterDayjs } from "@mui/x-date-pickers/AdapterDayjs"

const routes = [
	{ path: "/", element: <Navigate to="/list" /> },
	{ path: "/list", element: <ShowList /> },
	{ path: "/edit/:showId", element: <ShowEdit /> }
]

const router = createBrowserRouter(routes)

createRoot(document.getElementById("root")!).render(
	<StrictMode>
		<LocalizationProvider dateAdapter={AdapterDayjs}>
			<RouterProvider router={router} />
		</LocalizationProvider>
	</StrictMode>
)
