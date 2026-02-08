import { createFileRoute, useNavigate } from "@tanstack/react-router";
import React from "react";
import { toast } from "sonner";
import * as z from "zod";

import { useStore } from "@/store";

const googleCallbackSearchSchema = z.object({
	access_token: z.string().optional(),
	token_type: z.string().optional(),
	error: z.string().optional(),
});

export const Route = createFileRoute("/auth/google/callback")({
	validateSearch: googleCallbackSearchSchema,
	component: RouteComponent,
});

function RouteComponent() {
	const { access_token, error } = Route.useSearch();
	const navigate = useNavigate();
	const setToken = useStore((state) => state.setToken);
	const processed = React.useRef(false);

	React.useEffect(() => {
		if (processed.current) return;
		processed.current = true;

		if (error) {
			toast.error("Google sign-in was cancelled or failed.");
			navigate({ to: "/login" });
			return;
		}

		if (!access_token) {
			toast.error("Missing access token.");
			navigate({ to: "/login" });
			return;
		}

		setToken(access_token);
		toast.success("Signed in with Google!");
		navigate({ to: "/", replace: true });
	}, [access_token, error, navigate, setToken]);

	return (
		<div className="flex min-h-screen items-center justify-center">
			<p className="text-neutral-500">Completing sign in...</p>
		</div>
	);
}
