"use client"

import { createContext, useContext, useState, useCallback } from "react"
import Snackbar from "../components/common/SnackBar"

const SnackbarContext = createContext(null)

export const SnackbarProvider = ({ children }) => {
  const [snackbar, setSnackbar] = useState({
    open: false,
    message: "",
    severity: "info", // 'success', 'error', 'warning', 'info'
  })

  const showSnackbar = useCallback((message, severity = "info") => {
    setSnackbar({
      open: true,
      message,
      severity,
    })
  }, [])

  const hideSnackbar = useCallback(() => {
    setSnackbar((prev) => ({
      ...prev,
      open: false,
    }))
  }, [])

  const value = {
    snackbar,
    showSnackbar,
    hideSnackbar,
  }

  return (
    <SnackbarContext.Provider value={value}>
      {children}
      <Snackbar open={snackbar.open} message={snackbar.message} severity={snackbar.severity} onClose={hideSnackbar} />
    </SnackbarContext.Provider>
  )
}

export const useSnackbar = () => {
  const context = useContext(SnackbarContext)
  if (!context) {
    throw new Error("useSnackbar must be used within a SnackbarProvider")
  }
  return context
}
