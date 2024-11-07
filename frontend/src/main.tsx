import { StrictMode } from "react"
import { createRoot } from "react-dom/client"
import { createBrowserRouter, RouterProvider } from "react-router-dom"
import "./index.css"
import Home from "./pages/Home.tsx"
import ShowList from "./pages/ShowList.tsx"
import ShowEdit from "./pages/ShowEdit.tsx"

const routes = [
	{ path: "/", element: <Home /> },
	{ path: "/list", element: <ShowList /> },
	{ path: "/edit/:showId", element: <ShowEdit showId={undefined} /> }
]

const router = createBrowserRouter(routes)

createRoot(document.getElementById("root")!).render(
	<StrictMode>
		<RouterProvider router={router} />
	</StrictMode>
)
