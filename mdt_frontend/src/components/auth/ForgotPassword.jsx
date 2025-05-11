"use client"

import { useState } from "react"
import { TextField, Button, Box, Typography, CircularProgress, Alert } from "@mui/material"
import { motion } from "framer-motion"

const ForgotPassword = ({ onSubmit }) => {
  const [email, setEmail] = useState("")
  const [isLoading, setIsLoading] = useState(false)
  const [errors, setErrors] = useState({})
  const [isSubmitted, setIsSubmitted] = useState(false)

  const validate = () => {
    const newErrors = {}

    if (!email) {
      newErrors.email = "Email is required"
    } else if (!/\S+@\S+\.\S+/.test(email)) {
      newErrors.email = "Email is invalid"
    }

    setErrors(newErrors)
    return Object.keys(newErrors).length === 0
  }

  const handleSubmit = async (e) => {
    e.preventDefault()

    if (!validate()) return

    setIsLoading(true)

    try {
      await new Promise((resolve) => setTimeout(resolve, 800))
      setIsSubmitted(true)
    } catch (error) {
      console.error("Forgot password error:", error)
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <Box component="form" onSubmit={handleSubmit} noValidate>
      <Typography component="h2" variant="h5" sx={{ mb: 3, textAlign: "center" }}>
        Reset Password
      </Typography>

      {isSubmitted ? (
        <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ duration: 0.5 }}>
          <Alert severity="success" sx={{ mb: 3 }}>
            If an account exists with email {email}, you will receive password reset instructions.
          </Alert>
          <Button fullWidth variant="outlined" onClick={() => setIsSubmitted(false)} sx={{ mt: 2 }}>
            Try Another Email
          </Button>
        </motion.div>
      ) : (
        <>
          <Typography variant="body2" sx={{ mb: 3 }}>
            Enter your email address and we'll send you instructions to reset your password.
          </Typography>

          <motion.div initial={{ y: 10, opacity: 0 }} animate={{ y: 0, opacity: 1 }} transition={{ duration: 0.3 }}>
            <TextField
              margin="normal"
              required
              fullWidth
              id="email"
              label="Email Address"
              name="email"
              autoComplete="email"
              autoFocus
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              error={!!errors.email}
              helperText={errors.email}
            />
          </motion.div>

          <motion.div
            initial={{ y: 10, opacity: 0 }}
            animate={{ y: 0, opacity: 1 }}
            transition={{ duration: 0.3, delay: 0.1 }}
          >
            <Button type="submit" fullWidth variant="contained" sx={{ mt: 3, mb: 2, py: 1.2 }} disabled={isLoading}>
              {isLoading ? <CircularProgress size={24} /> : "Send Reset Link"}
            </Button>
          </motion.div>
        </>
      )}
    </Box>
  )
}

export default ForgotPassword
