import { useForm } from "@tanstack/react-form";
import { Link, useNavigate } from "@tanstack/react-router";
import { FcGoogle } from "react-icons/fc";
import { toast } from "sonner";
import * as z from "zod";
import {
	oauthGoogleJwtAuthorizeApiV1AuthGoogleAuthorizeGet,
	useAuthJwtLoginApiV1AuthJwtLoginPost,
} from "@/api/generated/api";
import { Button } from "@/components/ui/button";
import {
	Card,
	CardContent,
	CardFooter,
	CardHeader,
	CardTitle,
} from "@/components/ui/card";
import { Field, FieldError, FieldLabel } from "@/components/ui/field";
import { Input } from "@/components/ui/input";
import { getErrorMessage } from "@/lib/errors";
import { useStore } from "@/store";

const loginFormSchema = z.object({
	email: z.email("Please enter a valid email address."),
	password: z.string().min(1, "Password is required."),
});

export const LoginForm = () => {
	const loginMutation = useAuthJwtLoginApiV1AuthJwtLoginPost();
	const navigate = useNavigate();
	const setToken = useStore((state) => state.setToken);

	const form = useForm({
		defaultValues: {
			email: "",
			password: "",
		},
		validators: {
			onSubmit: loginFormSchema,
		},
		onSubmit: async ({ value }) => {
			try {
				const response = await loginMutation.mutateAsync({
					data: {
						username: value.email,
						password: value.password,
					},
				});

				setToken(response.access_token);

				navigate({ to: "/" });
			} catch (error) {
				toast.error(getErrorMessage(error), { duration: 5000 });
			}
		},
	});

	const handleGoogleLogin = async () => {
		try {
			const { authorization_url } =
				await oauthGoogleJwtAuthorizeApiV1AuthGoogleAuthorizeGet();
			window.location.href = authorization_url;
		} catch {
			toast.error("Failed to initiate Google sign-in. Please try again.", {
				duration: 5000,
			});
		}
	};

	return (
		<Card className="w-full max-w-sm">
			<CardHeader>
				<CardTitle className="text-center text-2xl font-bold">Login</CardTitle>
			</CardHeader>
			<CardContent>
				<form
					id="login-form"
					onSubmit={(e) => {
						e.preventDefault();
						form.handleSubmit();
					}}
					className="space-y-4"
				>
					<form.Field name="email">
						{(field) => {
							const isInvalid =
								field.state.meta.isTouched && !field.state.meta.isValid;

							return (
								<Field data-invalid={isInvalid}>
									<FieldLabel htmlFor={field.name}>Email</FieldLabel>
									<Input
										id={field.name}
										type="email"
										name={field.name}
										value={field.state.value}
										onBlur={field.handleBlur}
										onChange={(e) => field.handleChange(e.target.value)}
										placeholder="Enter your email address"
										autoComplete="off"
										aria-invalid={isInvalid}
									/>

									{isInvalid && <FieldError errors={field.state.meta.errors} />}
								</Field>
							);
						}}
					</form.Field>

					<form.Field name="password">
						{(field) => {
							const isInvalid =
								field.state.meta.isTouched && !field.state.meta.isValid;

							return (
								<Field data-invalid={isInvalid}>
									<FieldLabel htmlFor={field.name}>Password</FieldLabel>
									<Input
										id={field.name}
										type="password"
										name={field.name}
										value={field.state.value}
										onBlur={field.handleBlur}
										onChange={(e) => field.handleChange(e.target.value)}
										placeholder="Enter your password"
										autoComplete="off"
										aria-invalid={isInvalid}
									/>

									{isInvalid && <FieldError errors={field.state.meta.errors} />}
								</Field>
							);
						}}
					</form.Field>

					<form.Subscribe
						selector={(state) => [state.isSubmitting, state.canSubmit]}
					>
						{([isSubmitting, canSubmit]) => (
							<Button
								type="submit"
								className="w-full"
								disabled={!canSubmit || isSubmitting}
							>
								{isSubmitting ? "Logging in..." : "Login"}
							</Button>
						)}
					</form.Subscribe>

					<div className="relative my-4">
						<div className="absolute inset-0 flex items-center">
							<span className="w-full border-t" />
						</div>
						<div className="relative flex justify-center text-xs uppercase">
							<span className="bg-card px-2 text-muted-foreground">or</span>
						</div>
					</div>

					<Button
						type="button"
						variant="outline"
						className="w-full"
						onClick={handleGoogleLogin}
					>
						<FcGoogle /> Continue with Google
					</Button>
				</form>
				<CardFooter className="flex justify-center mt-4">
					<Link to="/register" className="text-sm">
						Don't have an account? Register
					</Link>
				</CardFooter>
			</CardContent>
		</Card>
	);
};
