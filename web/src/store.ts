import { create } from "zustand";
import { devtools, persist, subscribeWithSelector } from "zustand/middleware";
import { immer } from "zustand/middleware/immer";

import { createAuthSlice } from "./features/auth/store/auth";
import type { Store } from "./types/store";

export const useStore = create<Store>()(
	devtools(
		persist(
			subscribeWithSelector(
				immer((...args) => ({
					...createAuthSlice(...args),
				})),
			),
			{
				name: "auth-storage",
				partialize: (state) => ({
					token: state.token,
				}),
			},
		),
	),
);
