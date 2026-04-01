import React from "react"

const ShowEditRow: React.FC<{ label: string; children?: React.ReactNode }> = ({
	label,
	children
}) => {
	return (
		<tr>
			<td className="font-semibold w-1 whitespace-nowrap pr-6">{label}</td>
			<td>{children}</td>
		</tr>
	)
}

export default ShowEditRow
