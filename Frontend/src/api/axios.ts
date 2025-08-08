import axios from "axios";

const api = axios.create({
    baseURL: "http://localhost:5000/",
    headers: {
        "Content-Type": "application/json",
        
    },
});
export const privateApi = axios.create({
  baseURL: "http://localhost:5000/",
  headers: {
    "Content-Type": "application/json",
  },
});

// Attach token dynamically using an interceptor
privateApi.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem("token"); // or wherever you store it
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

export default api;
