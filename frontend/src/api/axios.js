import axios from "axios";

const api = axios.create({
    baseURL: import.meta.env.VITE_API_URL || "http://localhost:8010/api",
    withCredentials: true,
});

api.interceptors.request.use((config) => {
    const auth = JSON.parse(localStorage.getItem("auth") || "null");

    // Check if auth exists AND if auth.access exists
    if (auth && auth.access) {
        config.headers.Authorization = `Bearer ${auth.access}`;
    }

    return config;
});

api.interceptors.response.use(
    (res) => res,
    async(error) => {
        const original = error.config;
        const auth = JSON.parse(localStorage.getItem("auth") || "null");

        // Safely check error.response and auth before reading their properties
        if (
            error.response &&
            error.response.status === 401 &&
            auth &&
            auth.refresh &&
            !original._retry
        ) {
            original._retry = true;
            try {
                const { data } = await axios.post(
                    `${import.meta.env.VITE_API_URL || "http://localhost:8010/api"}/auth/token/refresh/`, { refresh: auth.refresh }
                );
                localStorage.setItem("auth", JSON.stringify({...auth, access: data.access }));
                original.headers.Authorization = `Bearer ${data.access}`;
                return api(original);
            } catch {
                localStorage.removeItem("auth");
                window.location.href = "/login";
            }
        }
        return Promise.reject(error);
    }
);

export default api;