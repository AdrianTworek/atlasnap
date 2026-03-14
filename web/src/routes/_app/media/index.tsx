import { createFileRoute } from "@tanstack/react-router";
import { XIcon } from "lucide-react";
import { Button } from "@/components/ui/button";
import { UploadProgress } from "@/features/media/components/upload-progress";
import { UploadZone } from "@/features/media/components/upload-zone";
import { useMediaUpload } from "@/features/media/hooks/use-media-upload";

export const Route = createFileRoute("/_app/media/")({
	component: MediaPage,
});

function MediaPage() {
	const { uploads, upload, totalProgress, isUploading, reset } =
		useMediaUpload();

	return (
		<div className="space-y-6">
			<h1 className="text-2xl font-bold">Upload Media</h1>

			<UploadZone onFiles={upload} disabled={isUploading} />

			{uploads.length > 0 && (
				<div className="rounded-md border p-4">
					<div className="mb-2 flex items-center justify-between">
						<h3 className="font-medium">Upload Progress</h3>
						{!isUploading && (
							<Button
								type="button"
								variant="ghost"
								size="sm"
								onClick={reset}
								disabled={isUploading}
							>
								<XIcon /> Clear
							</Button>
						)}
					</div>
					<UploadProgress uploads={uploads} totalProgress={totalProgress} />
				</div>
			)}
		</div>
	);
}
