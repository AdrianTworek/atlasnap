import type { FileUploadState } from "../hooks/use-media-upload";

type UploadProgressProps = {
	uploads: FileUploadState[];
	totalProgress: number;
};

export const UploadProgress = ({
	uploads,
	totalProgress,
}: UploadProgressProps) => {
	if (!uploads.length) return null;

	return (
		<div className="space-y-3">
			<div className="flex items-center justify-between text-sm">
				<span>{uploads.length} files</span>
				<span>{totalProgress}%</span>
			</div>

			<div className="h-2 w-full rounded-full bg-neutral-200">
				<div
					className="h-2 rounded-full bg-black transition-all"
					style={{ width: `${totalProgress}%` }}
				/>
			</div>

			<div className="max-h-48 space-y-1 overflow-y-auto text-sm">
				{uploads.map((u) => (
					<div key={u.file.name} className="flex items-center justify-between">
						<span className="truncate">{u.file.name}</span>
						<span className="text-neutral-500">
							{u.status === "error" ? u.error : `${u.progress}%`}
						</span>
					</div>
				))}
			</div>
		</div>
	);
};
