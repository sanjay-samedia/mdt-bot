"use client"

import { Snackbar as MuiSnackbar, Alert } from "@mui/material"

const Snackbar = ({ open, message, severity, onClose }) => {
  return (
    <MuiSnackbar
      open={open}
      autoHideDuration={6000}
      onClose={onClose}
      anchorOrigin={{ vertical: "bottom", horizontal: "center" }}
    >
      <Alert onClose={onClose} severity={severity} sx={{ width: "100%" }} variant="filled">
        {message}
      </Alert>
    </MuiSnackbar>
  )
}

export default Snackbar
