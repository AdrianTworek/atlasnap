import { useQuery } from "@tanstack/react-query";
import * as React from "react";
import { useShallow } from "zustand/react/shallow";
import { getUsersCurrentUserApiV1AuthMeGetQueryOptions } from "@/api/generated/api";

import { useStore } from "@/store";

export const useAuth = () => {
	const { token, setUser, logout } = useStore(
		useShallow((state) => ({
			token: state.token,
			setUser: state.setUser,
			logout: state.logout,
		})),
	);

	const {
		data: user,
		isLoading,
		error,
	} = useQuery(
		getUsersCurrentUserApiV1AuthMeGetQueryOptions({
			query: {
				enabled: !!token,
				retry: false,
			},
		}),
	);

	React.useEffect(() => {
		if (user) {
			setUser(user);
		}
	}, [user, setUser]);

	React.useEffect(() => {
		if (token && error && !isLoading) {
			logout();
		}
	}, [token, error, isLoading, logout]);

	return {
		user,
		isLoading,
		isAuthenticated: !!user && !!token,
	};
};
