import { createFileRoute } from "@tanstack/react-router";

import { useAuth } from "@/features/auth/hooks/use-auth";

export const Route = createFileRoute("/_app/")({ component: HomePage });

function HomePage() {
	const { user, isAuthenticated, isLoading } = useAuth();

	if (isLoading) {
		return <p className="text-neutral-500">Loading...</p>;
	}

	return (
		<>
			<h1 className="mb-4 text-2xl font-bold">Welcome to Atlasnap</h1>
			{isAuthenticated && user ? (
				<p className="text-neutral-600">
					Logged in as <strong>{user.email}</strong>
				</p>
			) : (
				<p className="text-neutral-600">
					Sign in to start organizing your travel memories.
				</p>
			)}
		</>
	);
}
