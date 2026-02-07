import { createFileRoute } from "@tanstack/react-router";

import { Navbar } from "@/components/navbar";
import { useAuth } from "@/features/auth/hooks/use-auth";

export const Route = createFileRoute("/")({ component: App });

function App() {
	const { user, isAuthenticated, isLoading } = useAuth();

	if (isLoading) {
		return (
			<div className="min-h-screen">
				<Navbar />
				<div className="container mx-auto px-4 py-8">
					<p className="text-neutral-500">Loading...</p>
				</div>
			</div>
		);
	}

	return (
		<div className="min-h-screen">
			<Navbar />
			<main className="container mx-auto px-4 py-8">
				<h1 className="text-2xl font-bold mb-4">Welcome to Atlasnap</h1>
				{isAuthenticated && user ? (
					<div className="space-y-2">
						<p className="text-neutral-600">
							Logged in as <strong>{user.email}</strong>
						</p>
					</div>
				) : (
					<p className="text-neutral-600">
						Sign in to start organizing your travel memories.
					</p>
				)}
			</main>
		</div>
	);
}
