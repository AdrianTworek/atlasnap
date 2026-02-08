import { useForm } from "@tanstack/react-form";
import { Link, useNavigate } from "@tanstack/react-router";
import { FcGoogle } from "react-icons/fc";
import { toast } from "sonner";
import * as z from "zod";
import {
	oauthGoogleJwtAuthorizeApiV1AuthGoogleAuthorizeGet,
	useRegisterRegisterApiV1AuthRegisterPost,
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

const registerFormSchema = z
	.object({
		email: z
			.email("Please enter a valid email address.")
			.max(255, "Email cannot be longer than 255 characters."),
		password: z
			.string()
			.min(8, "Password must be at least 8 characters.")
			.max(72, "Password cannot be longer than 72 characters."),
		confirmPassword: z.string().min(1, "Please confirm your password."),
	})
	.refine((data) => data.password === data.confirmPassword, {
		path: ["confirmPassword"],
		message: "Passwords do not match.",
	});

export const RegisterForm = () => {
	const registerMutation = useRegisterRegisterApiV1AuthRegisterPost();
	const navigate = useNavigate();

	const form = useForm({
		defaultValues: {
			email: "",
			password: "",
			confirmPassword: "",
		},
		validators: {
			onSubmit: registerFormSchema,
		},
		onSubmit: async ({ value }) => {
			try {
				await registerMutation.mutateAsync({
					data: {
						email: value.email,
						password: value.password,
					},
				});
				toast.success(
					"Account created successfully! Please check your email to verify your account.",
					{ duration: 5000 },
				);

				form.reset();

				setTimeout(() => {
					navigate({ to: "/login" });
				}, 1500);
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
				<CardTitle className="text-center text-2xl font-bold">
					Register
				</CardTitle>
			</CardHeader>
			<CardContent>
				<form
					id="register-form"
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

					<form.Field name="confirmPassword">
						{(field) => {
							const isInvalid =
								field.state.meta.isTouched && !field.state.meta.isValid;

							return (
								<Field data-invalid={isInvalid}>
									<FieldLabel htmlFor={field.name}>Confirm Password</FieldLabel>
									<Input
										id={field.name}
										type="password"
										name={field.name}
										value={field.state.value}
										onBlur={field.handleBlur}
										onChange={(e) => field.handleChange(e.target.value)}
										placeholder="Confirm your password"
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
								{isSubmitting ? "Creating account..." : "Create account"}
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
					<Link to="/login" className="text-sm">
						Already have an account? Login
					</Link>
				</CardFooter>
			</CardContent>
		</Card>
	);
};
