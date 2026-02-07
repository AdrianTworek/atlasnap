import type { StateCreator } from "zustand";

import type { UserRead } from "@/api/generated/models";

type State = {
	user: UserRead | null;
	token: string | null;
	isAuthenticated: boolean;
	isLoading: boolean;
};

type Actions = {
	setUser: (user: UserRead | null) => void;
	setToken: (token: string | null) => void;
	logout: () => void;
};

export type AuthSlice = State & Actions;

export const createAuthSlice: StateCreator<
	AuthSlice,
	[["zustand/immer", never]],
	[],
	AuthSlice
> = (set) => ({
	user: null,
	token: null,
	isAuthenticated: false,
	isLoading: false,
	setUser: (user) =>
		set((state) => {
			state.user = user;
			state.isAuthenticated = !!user;
		}),
	setToken: (token) => {
		set((state) => {
			state.token = token;
		});
		if (typeof window !== "undefined") {
			if (token) {
				localStorage.setItem("accessToken", token);
			} else {
				localStorage.removeItem("accessToken");
			}
		}
	},
	logout: () => {
		set((state) => {
			state.user = null;
			state.token = null;
			state.isAuthenticated = false;
		});
		if (typeof window !== "undefined") {
			localStorage.removeItem("accessToken");
		}
	},
});
