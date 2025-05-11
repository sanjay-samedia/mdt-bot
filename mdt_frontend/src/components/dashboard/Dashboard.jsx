"use client";

import { useState, useEffect } from "react";
import {
  Box,
  Container,
  Typography,
  TextField,
  Button,
  Paper,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  IconButton,
  InputAdornment,
  AppBar,
  Toolbar,
  useMediaQuery,
  useTheme,
  Divider,
  CircularProgress,
  Tooltip,
} from "@mui/material";
import { Person, Clear, PlayArrow, Stop, Refresh } from "@mui/icons-material";
import { motion } from "framer-motion";
import { useAuth } from "../../context/AuthContext";
import { useTraffic } from "../../hooks/useTraffic";
import { useSnackbar } from "../../context/SnackbarContext";
import Snackbar from "../common/SnackBar";

const URL_REGEX =
  /^(https?:\/\/)?(www\.)?[-a-zA-Z0-9@:%._+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_+.~#?&//=]*)$/;

const Dashboard = () => {
  const [botName, setBotName] = useState("");
  const [botNameError, setBotNameError] = useState("");
  const [urlName, setUrlName] = useState("");
  const [urlNameError, setUrlNameError] = useState("");
  const [traffic, setTraffic] = useState("100");
  const [trafficError, setTrafficError] = useState("");
  const [url, setUrl] = useState("");
  const [urlError, setUrlError] = useState("");

  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down("sm"));

  const { user, logout } = useAuth();
  const {
    trafficData,
    loading,
    error,
    fetchTrafficLogs,
    startTraffic,
    stopTraffic,
    isPolling,
  } = useTraffic();
  const { snackbar, showSnackbar, hideSnackbar } = useSnackbar();

  const hasRunningTraffic = trafficData.some(
    (item) => item.status === "RUNNING"
  );
  const runningTraffic = trafficData.find((item) => item.status === "RUNNING");

  useEffect(() => {
    if (url) {
      validateUrl(url);
    } else {
      setUrlError("");
    }
  }, [url]);

  const validateUrl = (value) => {
    if (!value) {
      setUrlError("URL is required");
      return false;
    }

    if (!URL_REGEX.test(value)) {
      setUrlError("Please enter a valid URL (e.g., https://example.com)");
      return false;
    }

    if (!/^https?:\/\//i.test(value)) {
      setUrlError("URL must start with http:// or https://");
      return false;
    }

    setUrlError("");
    return true;
  };

  const validateForm = () => {
    let isValid = true;

    if (!botName.trim()) {
      setBotNameError("Bot Name is required");
      isValid = false;
    } else {
      setBotNameError("");
    }

    if (!urlName.trim()) {
      setUrlNameError("Website Name is required");
      isValid = false;
    } else {
      setUrlNameError("");
    }

    if (!traffic) {
      setTrafficError("Traffic value is required");
      isValid = false;
    } else if (!/^[0-9,]+$/.test(traffic)) {
      setTrafficError("Traffic must be a number");
      isValid = false;
    } else {
      setTrafficError("");
    }

    if (!validateUrl(url)) {
      isValid = false;
    }

    return isValid;
  };

  const handleRun = async () => {
    if (!validateForm()) {
      showSnackbar("Please fill all required fields correctly", "error");
      return;
    }

    try {
      await startTraffic({
        botName,
        urlName,
        url,
        traffic,
      });

      // setUrl("");
      // setBotName("");
      // setUrlName("");
      // setTraffic("100");
    } catch (err) {
      console.error("Failed to start traffic:", err);
    }
  };

  const handleStop = async (id) => {
    try {
      await stopTraffic(id);
    } catch (err) {
      console.error("Failed to stop traffic:", err);
    }
  };

  const handleRefresh = () => {
    fetchTrafficLogs();
    showSnackbar("Traffic data refreshed", "info");
  };

  const handleClearUrl = () => {
    setUrl("");
    setUrlError("");
  };

  const handleBotNameChange = (e) => {
    const value = e.target.value;
    setBotName(value);
    if (!value.trim()) {
      setBotNameError("Bot Name is required");
    } else {
      setBotNameError("");
    }
  };

  const handleUrlNameChange = (e) => {
    const value = e.target.value;
    setUrlName(value);
    if (!value.trim()) {
      setUrlNameError("Website Name is required");
    } else {
      setUrlNameError("");
    }
  };

  const handleTrafficChange = (e) => {
    const value = e.target.value;
    if (/^[0-9,]*$/.test(value)) {
      setTraffic(value);
      if (!value) {
        setTrafficError("Traffic value is required");
      } else {
        setTrafficError("");
      }
    }
  };

  const handleUrlChange = (e) => {
    const value = e.target.value;
    setUrl(value);
    validateUrl(value);
  };

  const getStatusColor = (status) => {
    switch (status) {
      case "RUNNING":
        return theme.palette.info.main;
      case "COMPLETED":
        return theme.palette.success.main;
      case "STOPPED":
        return theme.palette.warning.main;
      case "FAILED":
        return theme.palette.error.main;
      default:
        return theme.palette.text.primary;
    }
  };

  const formatDate = (dateString) => {
    if (!dateString) return "N/A";
    const date = new Date(dateString);
    return date.toLocaleString();
  };

  return (
    <Box sx={{ display: "flex", flexDirection: "column", minHeight: "100vh" }}>
      <AppBar
        position="static"
        color="transparent"
        elevation={0}
        sx={{ borderBottom: "1px solid rgba(0, 0, 0, 0.12)" }}
      >
        <Toolbar>
          <Typography
            variant="h5"
            component="div"
            sx={{
              flexGrow: 1,
              fontFamily: '"Playfair Display", serif',
              fontStyle: "italic",
              fontWeight: 700,
            }}
          >
            Traffic Generator
          </Typography>
          <Box sx={{ display: "flex", alignItems: "center" }}>
            <Person sx={{ mr: 1 }} />
            <Typography variant="body2" sx={{ mr: 2 }}>
              {user?.name || user?.username || "Admin"}
            </Typography>
            <Button
              variant="contained"
              color="primary"
              size="small"
              onClick={logout}
            >
              Logout
            </Button>
          </Box>
        </Toolbar>
      </AppBar>

      <Container maxWidth="lg" sx={{ py: 4, flex: 1 }}>
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
        >
          <Box
            component={Paper}
            sx={{ p: 3, mb: 4 }}
            elevation={0}
            variant="outlined"
          >
            <Box
              sx={{
                display: "flex",
                flexDirection: isMobile ? "column" : "row",
                gap: 2,
                mb: 3,
              }}
            >
              <TextField
                label="Bot Name"
                variant="outlined"
                fullWidth
                required
                value={botName}
                onChange={handleBotNameChange}
                placeholder="My Bot"
                size="small"
                error={!!botNameError}
                helperText={botNameError}
              />
              <TextField
                label="Website Name"
                variant="outlined"
                fullWidth
                required
                value={urlName}
                onChange={handleUrlNameChange}
                placeholder="My Website"
                size="small"
                error={!!urlNameError}
                helperText={urlNameError}
              />
              <TextField
                label="Traffic (Visits)"
                variant="outlined"
                fullWidth
                required
                value={traffic}
                onChange={handleTrafficChange}
                size="small"
                error={!!trafficError}
                helperText={trafficError}
                inputProps={{ inputMode: "numeric", pattern: "[0-9,]*" }}
              />
            </Box>

            <TextField
              label="URL"
              variant="outlined"
              fullWidth
              required
              value={url}
              onChange={handleUrlChange}
              placeholder="https://example.com"
              size="small"
              error={!!urlError}
              helperText={urlError}
              InputProps={{
                endAdornment: url && (
                  <InputAdornment position="end">
                    <IconButton
                      aria-label="clear url"
                      onClick={handleClearUrl}
                      edge="end"
                    >
                      <Clear />
                    </IconButton>
                  </InputAdornment>
                ),
              }}
              sx={{ mb: 3 }}
            />

            <Box sx={{ display: "flex", justifyContent: "center", gap: 2 }}>
              <Tooltip
                title={
                  hasRunningTraffic
                    ? "Stop the current traffic before starting a new one"
                    : ""
                }
              >
                <span>
                  <Button
                    variant="contained"
                    color="primary"
                    startIcon={
                      loading ? <CircularProgress size={20} /> : <PlayArrow />
                    }
                    onClick={handleRun}
                    disabled={!url || loading || hasRunningTraffic}
                    sx={{
                      bgcolor: "rgba(0,0,0,0.05)",
                      color: "text.primary",
                      "&:hover": {
                        bgcolor: "rgba(0,0,0,0.1)",
                      },
                    }}
                  >
                    Run
                  </Button>
                </span>
              </Tooltip>
              <Tooltip
                title={!runningTraffic ? "No running traffic to stop" : ""}
              >
                <span>
                  <Button
                    variant="contained"
                    color="primary"
                    startIcon={
                      loading ? <CircularProgress size={20} /> : <Stop />
                    }
                    onClick={() => handleStop(runningTraffic?.id)}
                    disabled={!runningTraffic || loading}
                    sx={{
                      bgcolor: "rgba(0,0,0,0.05)",
                      color: "text.primary",
                      "&:hover": {
                        bgcolor: "rgba(0,0,0,0.1)",
                      },
                    }}
                  >
                    Stop
                  </Button>
                </span>
              </Tooltip>
            </Box>
          </Box>
        </motion.div>

        <Divider sx={{ my: 4 }} />

        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 0.5, delay: 0.2 }}
        >
          <Box
            sx={{
              display: "flex",
              justifyContent: "space-between",
              alignItems: "center",
              mb: 2,
            }}
          >
            <Typography variant="h6">
              Traffic Log{" "}
              {isPolling && (
                <CircularProgress
                  size={16}
                  sx={{ ml: 1, verticalAlign: "middle" }}
                />
              )}
            </Typography>
            <Tooltip title="Refresh traffic data">
              <IconButton onClick={handleRefresh} disabled={loading}>
                <Refresh />
              </IconButton>
            </Tooltip>
          </Box>

          {loading && trafficData.length === 0 ? (
            <Box sx={{ display: "flex", justifyContent: "center", my: 4 }}>
              <CircularProgress />
            </Box>
          ) : (
            <TableContainer component={Paper} variant="outlined" sx={{ mb: 4 }}>
              <Table sx={{ minWidth: 650 }} size="small">
                <TableHead>
                  <TableRow sx={{ bgcolor: "rgba(0,0,0,0.02)" }}>
                    <TableCell>Bot Name</TableCell>
                    <TableCell>Website</TableCell>
                    <TableCell>URL</TableCell>
                    <TableCell>Requested Visits</TableCell>
                    <TableCell>Visits Sent</TableCell>
                    <TableCell>Start Time</TableCell>
                    <TableCell>Status</TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {trafficData.length === 0 ? (
                    <TableRow>
                      <TableCell colSpan={8} align="center">
                        No traffic data available
                      </TableCell>
                    </TableRow>
                  ) : (
                    trafficData.map((row) => (
                      <TableRow key={row.id}>
                        <TableCell>{row.name || row.bot_name}</TableCell>
                        <TableCell>{row.website?.name}</TableCell>
                        <TableCell>
                          <Tooltip title={row.website?.url} placement="top">
                            <span
                              style={{
                                display: "block",
                                maxWidth: "200px",
                                overflow: "hidden",
                                textOverflow: "ellipsis",
                                whiteSpace: "nowrap",
                              }}
                            >
                              {row.website?.url}
                            </span>
                          </Tooltip>
                        </TableCell>
                        <TableCell>{row.requested_visits}</TableCell>
                        <TableCell>{row.visits_sent}</TableCell>
                        <TableCell>{formatDate(row.start_time)}</TableCell>
                        <TableCell sx={{ color: getStatusColor(row.status) }}>
                          {row.status}
                        </TableCell>
                      </TableRow>
                    ))
                  )}
                </TableBody>
              </Table>
            </TableContainer>
          )}
        </motion.div>
      </Container>

      {/* Snackbar for notifications */}
      <Snackbar
        open={snackbar.open}
        message={snackbar.message}
        severity={snackbar.severity}
        onClose={hideSnackbar}
      />
    </Box>
  );
};

export default Dashboard;
