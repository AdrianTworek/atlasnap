import { Link } from "@tanstack/react-router";
import { Button } from "@/components/ui/button";
import {
	DropdownMenu,
	DropdownMenuContent,
	DropdownMenuItem,
	DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import { useAuth } from "@/features/auth/hooks/use-auth";
import { useStore } from "@/store";

export const Navbar = () => {
	const { user, isAuthenticated } = useAuth();
	const logout = useStore((state) => state.logout);

	const handleLogout = () => {
		logout();
		window.location.href = "/login";
	};

	return (
		<header className="border-b">
			<div className="container mx-auto flex h-16 items-center justify-between px-4">
				<Link to="/" className="text-xl font-bold">
					Atlasnap
				</Link>

				<nav className="flex items-center gap-4">
					{isAuthenticated && user ? (
						<DropdownMenu>
							<DropdownMenuTrigger asChild>
								<Button variant="ghost" className="gap-2">
									{user.avatar_url ? (
										<img
											src={user.avatar_url}
											alt={`${user.email}'s avatar`}
											className="h-8 w-8 rounded-full"
										/>
									) : (
										<span className="h-8 w-8 rounded-full bg-neutral-200 flex items-center justify-center text-sm font-medium">
											{user.email[0].toUpperCase()}
										</span>
									)}
									<span className="hidden sm:inline">{user.email}</span>
								</Button>
							</DropdownMenuTrigger>
							<DropdownMenuContent align="end" className="w-48">
								<DropdownMenuItem
									onClick={handleLogout}
									className="cursor-pointer"
								>
									Log out
								</DropdownMenuItem>
							</DropdownMenuContent>
						</DropdownMenu>
					) : (
						<div className="flex gap-2">
							<Button variant="ghost" asChild>
								<Link to="/login">Log in</Link>
							</Button>
							<Button asChild>
								<Link to="/register">Sign up</Link>
							</Button>
						</div>
					)}
				</nav>
			</div>
		</header>
	);
};
