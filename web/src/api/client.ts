import axios, { type AxiosError, type AxiosRequestConfig } from "axios";

const api = axios.create({
	baseURL: "http://localhost:8000",
});

api.interceptors.request.use((config) => {
	const token = localStorage.getItem("accessToken");
	if (token) {
		config.headers.Authorization = `Bearer ${token}`;
	}
	return config;
});

export const apiClient = <T>(config: AxiosRequestConfig): Promise<T> => {
	return api<T>(config)
		.then((response) => response.data)
		.catch((error: AxiosError) => {
			// Extract error message from FastAPI response
			if (error.response?.data) {
				const data = error.response.data as { detail?: string | unknown };
				if (typeof data.detail === "string") {
					throw new Error(data.detail);
				}
				// Handle validation errors
				if (typeof data.detail === "object" && Array.isArray(data.detail)) {
					const firstError = data.detail[0];
					if (
						firstError &&
						typeof firstError === "object" &&
						"msg" in firstError
					) {
						throw new Error(String(firstError.msg));
					}
				}
			}
			// Fallback to axios error message
			throw new Error(error.message || "Request failed");
		});
};
