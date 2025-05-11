import axios from "axios";

const getCsrfToken = () => {
  const name = "csrftoken=";
  const decodedCookie = decodeURIComponent(document.cookie);
  const cookieArray = decodedCookie.split(";");

  for (let i = 0; i < cookieArray.length; i++) {
    const cookie = cookieArray[i].trim();
    if (cookie.indexOf(name) === 0) {
      return cookie.substring(name.length, cookie.length);
    }
  }
  return "";
};

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || "http://localhost:3000",
  headers: {
    "Content-Type": "application/json",
  },
  withCredentials: true, 
});

api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem("authToken");
    if (token) {
      
      config.headers.Authorization = `Token ${token}`;
    }

    if (config.method !== "get") {
      const csrfToken = getCsrfToken();
      if (csrfToken) {
        config.headers["X-CSRFToken"] = csrfToken;
      }
    }

    return config;
  },
  (error) => Promise.reject(error)
);

api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response && error.response.status === 401) {
      localStorage.removeItem("authToken");
      localStorage.removeItem("userData");
      window.location.href = "/login";
    }
    if (error.response && error.response.status === 403) {
      console.error("CSRF validation might have failed:", error.response.data);
    }
    return Promise.reject(error);
  }
);

export const authAPI = {
  register: async (userData) => {
    const response = await api.post("/accounts/register/", {
      name: userData.name || `${userData.firstName} ${userData.lastName}`,
      username: userData.username || userData.email.split("@")[0],
      email: userData.email,
      user_type: userData.user_type || "USER",
      password: userData.password,
    });
    return response.data;
  },

  login: async (credentials) => {
    const response = await api.post("/accounts/login/", {
      username: credentials.username || credentials.email,
      password: credentials.password,
    });
    return response.data;
  },

  logout: async () => {
    const response = await api.post("/accounts/logout/");
    return response.data;
  },

  checkAuth: async () => {
    try {
      const response = await api.get("/accounts/me"); 
      return response.data;
    } catch (error) {
      throw error;
    }
  },
};

export const trafficAPI = {
  getTrafficLogs: async () => {
    const response = await api.get("/bot-instance/");
    return response.data;
  },

  startTraffic: async (trafficData) => {
    const response = await api.post("/bot-instance/simulate_traffic/", {
      url: trafficData.url,
      website_name:
        trafficData.urlName ||
        new URL(trafficData.url).hostname.replace("www.", ""),
      bot_name: trafficData.botName || `Bot-${new Date().getTime()}`,
      requested_visits:
        Number.parseInt(trafficData.traffic.replace(/,/g, ""), 10) || 1000,
    });
    return response.data;
  },

  stopTraffic: async (id) => {
    const response = await api.post(`/bot-instance/${id}/stop_traffic/`);
    return response.data;
  },
};

export default api;
