"use client"

import { useState } from "react"
import { Box, Container, Paper, Typography, Button, useMediaQuery, useTheme } from "@mui/material"
import { motion } from "framer-motion"
import SignIn from "./Signin"
import SignUp from "./Signup"
import ForgotPassword from "./ForgotPassword"

const containerVariants = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: {
      duration: 0.5,
      when: "beforeChildren",
      staggerChildren: 0.1,
    },
  },
}

const itemVariants = {
  hidden: { y: 20, opacity: 0 },
  visible: {
    y: 0,
    opacity: 1,
    transition: { duration: 0.5 },
  },
}

const AuthScreen = ({ onLogin }) => {
  const [authMode, setAuthMode] = useState("signin")
  const theme = useTheme()
  const isMobile = useMediaQuery(theme.breakpoints.down("sm"))

  const handleModeChange = (mode) => {
    setAuthMode(mode)
  }

  const handleAuth = (credentials) => {
    console.log("Auth credentials:", credentials)
    onLogin("mock-jwt-token")
  }

  return (
    <Container component="main" maxWidth="sm">
      <motion.div initial="hidden" animate="visible" variants={containerVariants}>
        <Box
          sx={{
            display: "flex",
            flexDirection: "column",
            alignItems: "center",
            justifyContent: "center",
            minHeight: "100vh",
            py: 4,
          }}
        >
          <motion.div variants={itemVariants}>
            <Typography
              component="h1"
              variant="h4"
              sx={{
                mb: 4,
                fontFamily: '"Playfair Display", serif',
                fontStyle: "italic",
                fontWeight: 700,
              }}
            >
              Traffic Generator
            </Typography>
          </motion.div>

          <Paper
            elevation={3}
            sx={{
              p: 4,
              width: "100%",
              borderRadius: 2,
              boxShadow: "0 4px 20px rgba(0,0,0,0.08)",
            }}
          >
            <motion.div variants={itemVariants}>
              {authMode === "signin" && <SignIn onSubmit={handleAuth} />}
              {authMode === "signup" && <SignUp onSubmit={handleAuth} />}
              {authMode === "forgot" && <ForgotPassword onSubmit={handleAuth} />}
            </motion.div>

            <motion.div variants={itemVariants}>
              <Box
                sx={{
                  mt: 3,
                  display: "flex",
                  flexDirection: isMobile ? "column" : "row",
                  justifyContent: "center",
                  gap: 2,
                }}
              >
                {authMode !== "signin" && (
                  <Button onClick={() => handleModeChange("signin")} variant="text" fullWidth={isMobile}>
                    Sign In
                  </Button>
                )}
                {authMode !== "signup" && (
                  <Button onClick={() => handleModeChange("signup")} variant="text" fullWidth={isMobile}>
                    Create Account
                  </Button>
                )}
                {authMode !== "forgot" && (
                  <Button onClick={() => handleModeChange("forgot")} variant="text" fullWidth={isMobile}>
                    Forgot Password
                  </Button>
                )}
              </Box>
            </motion.div>
          </Paper>
        </Box>
      </motion.div>
    </Container>
  )
}

export default AuthScreen
