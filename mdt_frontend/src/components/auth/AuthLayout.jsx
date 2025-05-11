"use client"

import { Outlet, useNavigate } from "react-router-dom"
import { Box, Container, Paper, Typography, Button, useMediaQuery, useTheme } from "@mui/material"
import { motion } from "framer-motion"

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

const AuthLayout = () => {
  const theme = useTheme()
  const isMobile = useMediaQuery(theme.breakpoints.down("sm"))
  const navigate = useNavigate()

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
              <Outlet />
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
                <Button onClick={() => navigate("/login")} variant="text" fullWidth={isMobile}>
                  Sign In
                </Button>
                <Button onClick={() => navigate("/signup")} variant="text" fullWidth={isMobile}>
                  Create Account
                </Button>
                <Button onClick={() => navigate("/forgot-password")} variant="text" fullWidth={isMobile}>
                  Forgot Password
                </Button>
              </Box>
            </motion.div>
          </Paper>
        </Box>
      </motion.div>
    </Container>
  )
}

export default AuthLayout
