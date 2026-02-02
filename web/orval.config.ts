import { defineConfig } from "orval";

export default defineConfig({
	atlasnap: {
		input: "http://localhost:8000/openapi.json",
		output: {
			mode: "single",
			target: "src/api/generated/api.ts",
			schemas: "src/api/generated/models",
			client: "react-query",
			httpClient: "axios",
			baseUrl: "http://localhost:8000",
			override: {
				mutator: {
					path: "src/api/client.ts",
					name: "apiClient",
				},
				query: {
					useQuery: true,
					useMutation: true,
				},
			},
		},
	},
});
