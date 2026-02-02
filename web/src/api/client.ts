import axios, { type AxiosRequestConfig } from "axios";

const api = axios.create({
	baseURL: "http://localhost:8000",
});

api.interceptors.request.use((config) => {
	const token = localStorage.getItem("token");
	if (token) {
		config.headers.Authorization = `Bearer ${token}`;
	}
	return config;
});

export const apiClient = <T>(config: AxiosRequestConfig): Promise<T> => {
	return axios<T>(config).then((res) => res.data);
};
