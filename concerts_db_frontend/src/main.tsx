import { StrictMode } from "react"
import { createRoot } from "react-dom/client"
import { createBrowserRouter, RouterProvider } from "react-router-dom"
import "./index.css"
import Home from "./pages/Home.tsx"
import ShowList from "./pages/ShowList.tsx"

const routes = [
	{ path: "/", element: <Home /> },
	{ path: "/list", element: <ShowList /> }
]

const router = createBrowserRouter(routes)

createRoot(document.getElementById("root")!).render(
	<StrictMode>
		<RouterProvider router={router} />
	</StrictMode>
)
