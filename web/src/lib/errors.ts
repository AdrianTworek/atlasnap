type ErrorCode =
	| "REGISTER_USER_ALREADY_EXISTS"
	| "LOGIN_BAD_CREDENTIALS"
	| "LOGIN_INACTIVE_USER"
	| "LOGIN_USER_NOT_VERIFIED";

const ERROR_MESSAGES: Record<ErrorCode, string> = {
	REGISTER_USER_ALREADY_EXISTS:
		"An account with this email already exists. Please sign in instead.",
	LOGIN_BAD_CREDENTIALS: "Invalid email or password. Please try again.",
	LOGIN_INACTIVE_USER:
		"Your account has been deactivated. Please contact support if you believe this is an error.",
	LOGIN_USER_NOT_VERIFIED:
		"Please verify your email address before signing in. If you have not received a verification email, please check your spam folder or request a new verification email.",
};

export const getErrorMessage = (error: unknown): string => {
	if (error instanceof Error) {
		const message = error.message;

		if (message in ERROR_MESSAGES) {
			return ERROR_MESSAGES[message as ErrorCode];
		}

		if (message.includes("validation") || message.includes("field")) {
			return message;
		}

		return "Something went wrong.";
	}

	return "Something went wrong.";
};
