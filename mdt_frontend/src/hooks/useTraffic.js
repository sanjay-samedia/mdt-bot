"use client";

import { useState, useCallback, useEffect } from "react";
import { trafficAPI } from "../services/api";
import { useSnackbar } from "../context/SnackbarContext"; 

export const useTraffic = () => {
  const [trafficData, setTrafficData] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [isPolling, setIsPolling] = useState(false);
  const { showSnackbar } = useSnackbar();

  const fetchTrafficLogs = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await trafficAPI.getTrafficLogs();
      setTrafficData(data);
      return data;
    } catch (err) {
      const errorMessage =
        err.response?.data?.message || "Failed to fetch traffic logs";
      setError(errorMessage);
      showSnackbar(errorMessage, "error");
      throw err;
    } finally {
      setLoading(false);
    }
  }, [showSnackbar]);

  const startTraffic = useCallback(
    async (trafficParams) => {
      setLoading(true);
      setError(null);
      try {
        const newTraffic = await trafficAPI.startTraffic(trafficParams);
        await fetchTrafficLogs(); 
        showSnackbar("Traffic generation started successfully", "success");
        setIsPolling(true); 
        return newTraffic;
      } catch (err) {
        const errorMessage =
          err.response?.data?.message || "Failed to start traffic";
        setError(errorMessage);
        showSnackbar(errorMessage, "error");
        throw err;
      } finally {
        setLoading(false);
      }
    },
    [fetchTrafficLogs, showSnackbar]
  );

  const stopTraffic = useCallback(
    async (id) => {
      setLoading(true);
      setError(null);
      try {
        const result = await trafficAPI.stopTraffic(id);
        await fetchTrafficLogs(); // Refresh the list after stopping
        showSnackbar("Traffic generation stopped successfully", "success");
        return result;
      } catch (err) {
        const errorMessage =
          err.response?.data?.message || "Failed to stop traffic";
        setError(errorMessage);
        showSnackbar(errorMessage, "error");
        throw err;
      } finally {
        setLoading(false);
      }
    },
    [fetchTrafficLogs, showSnackbar]
  );

  useEffect(() => {
    let intervalId = null;

    if (isPolling) {
     
      intervalId = setInterval(async () => {
        try {
          const data = await trafficAPI.getTrafficLogs();
          setTrafficData(data);

          
          const hasRunningTraffic = data.some(
            (item) => item.status === "RUNNING"
          );

          
          if (!hasRunningTraffic) {
            setIsPolling(false);
            showSnackbar("All traffic generations completed", "info");
          }
        } catch (err) {
          console.error("Polling error:", err);
        }
      }, 10000); 
    }

    
    return () => {
      if (intervalId) {
        clearInterval(intervalId);
      }
    };
  }, [isPolling, showSnackbar]);

  
  useEffect(() => {
    fetchTrafficLogs()
      .then((data) => {
        
        const hasRunningTraffic = data.some(
          (item) => item.status === "RUNNING"
        );
        if (hasRunningTraffic) {
          setIsPolling(true);
        }
      })
      .catch((err) => console.error("Initial fetch error:", err));
  }, [fetchTrafficLogs]);

  return {
    trafficData,
    loading,
    error,
    fetchTrafficLogs,
    startTraffic,
    stopTraffic,
    isPolling,
  };
};
