import { useQueryClient } from "@tanstack/react-query";
import axios from "axios";
import * as React from "react";
import {
	getListMediaApiV1MediaGetQueryKey,
	useConfirmUploadsApiV1MediaUploadConfirmPost,
	useGetUploadUrlsApiV1MediaUploadUrlsPost,
} from "@/api/generated/api";
import type { UploadRequest, UploadResponse } from "@/api/generated/models";

type UploadStatus =
	| "pending"
	| "uploading"
	| "uploaded"
	| "confirming"
	| "done"
	| "error";

export type FileUploadState = {
	file: File;
	progress: number;
	status: UploadStatus;
	error?: string;
	key?: string;
};

const BATCH_SIZE = 5;

export const useMediaUpload = () => {
	const [uploads, setUploads] = React.useState<FileUploadState[]>([]);
	const queryClient = useQueryClient();

	const getUrlsMutation = useGetUploadUrlsApiV1MediaUploadUrlsPost();
	const confirmMutation = useConfirmUploadsApiV1MediaUploadConfirmPost();

	const updateUpload = (index: number, patch: Partial<FileUploadState>) => {
		setUploads((prev) =>
			prev.map((u, i) => (i === index ? { ...u, ...patch } : u)),
		);
	};

	const uploadToS3 = async (
		file: File,
		presigned: UploadResponse,
		index: number,
	) => {
		updateUpload(index, { status: "uploading", key: presigned.key });

		await axios.put(presigned.upload_url, file, {
			headers: { "Content-Type": file.type },
			onUploadProgress: (e) => {
				const progress = e.total ? Math.round((e.loaded / e.total) * 100) : 0;
				updateUpload(index, { progress });
			},
		});

		updateUpload(index, { status: "uploaded", progress: 100 });
	};

	const upload = async (files: File[]) => {
		if (!files.length) return;

		// init state
		setUploads(
			files.map((file) => ({
				file,
				progress: 0,
				status: "pending",
			})),
		);

		// Step 1: get presigned URLs
		const requestFiles: UploadRequest[] = files.map((f) => ({
			filename: f.name,
			content_type: f.type,
			file_size: f.size,
		}));

		let presigned: UploadResponse[];
		try {
			const res = await getUrlsMutation.mutateAsync({
				data: { files: requestFiles },
			});
			presigned = res.uploads;
		} catch (error) {
			console.error(error);
			setUploads((prev) =>
				prev.map((u) => ({
					...u,
					status: "error",
					error: "Failed to get upload URLs",
				})),
			);
			return;
		}

		// Step 2: upload to S3 in batches
		const successful: number[] = [];

		for (let i = 0; i < files.length; i += BATCH_SIZE) {
			const batch = files.slice(i, i + BATCH_SIZE);
			const results = await Promise.allSettled(
				batch.map((file, idx) => uploadToS3(file, presigned[i + idx], i + idx)),
			);

			results.forEach((result, idx) => {
				if (result.status === "fulfilled") {
					successful.push(i + idx);
				} else {
					updateUpload(i + idx, { status: "error", error: "Upload failed" });
				}
			});
		}

		if (!successful.length) return;

		// Step 3: confirm uploads
		successful.forEach((idx) => {
			updateUpload(idx, { status: "confirming" });
		});

		try {
			await confirmMutation.mutateAsync({
				data: {
					files: successful.map((idx) => ({
						key: presigned[idx].key,
						original_filename: files[idx].name,
						content_type: files[idx].type,
						file_size: files[idx].size,
					})),
				},
			});

			successful.forEach((idx) => {
				updateUpload(idx, { status: "done" });
			});

			// refresh media list
			queryClient.invalidateQueries({
				queryKey: getListMediaApiV1MediaGetQueryKey(),
			});
		} catch {
			successful.forEach((idx) => {
				updateUpload(idx, { status: "error", error: "Confirm failed" });
			});
		}
	};

	const totalProgress = React.useMemo(() => {
		if (!uploads.length) return 0;
		const sum = uploads.reduce((acc, u) => acc + u.progress, 0);
		return Math.round(sum / uploads.length);
	}, [uploads]);

	const reset = () => setUploads([]);

	const isUploading = uploads.some(
		(u) =>
			u.status === "pending" ||
			u.status === "uploading" ||
			u.status === "confirming",
	);

	return {
		uploads,
		upload,
		reset,
		totalProgress,
		isUploading,
	};
};
