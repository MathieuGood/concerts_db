import Modal from "@mui/material/Modal"

const BasicModal: React.FC<{ children: React.ReactNode; open: boolean; onClose: () => void }> = ({
	children,
	open,
	onClose
}) => {
	return (
		<Modal open={open} onClose={onClose}>
			<div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-96 bg-white border-2 border-black shadow-lg p-4">
				{children}
			</div>
		</Modal>
	)
}

export default BasicModal
