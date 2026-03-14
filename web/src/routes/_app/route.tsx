import { createFileRoute, Outlet } from "@tanstack/react-router";
import { Navbar } from "@/components/navbar";

export const Route = createFileRoute("/_app")({
	component: AppLayout,
});

function AppLayout() {
	return (
		<div className="min-h-screen">
			<Navbar />
			<main className="container mx-auto px-4 py-8">
				<Outlet />
			</main>
		</div>
	);
}
