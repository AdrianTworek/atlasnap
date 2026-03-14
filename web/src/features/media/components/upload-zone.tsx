import * as React from "react";
import { Button } from "@/components/ui/button";
import { cn } from "@/lib/utils";

const ACCEPTED_TYPES = [
	"image/jpeg",
	"image/png",
	"image/webp",
	"image/gif",
	"image/heic",
	"video/mp4",
	"video/quicktime",
	"video/webm",
];

const MAX_FILES = 200;

type UploadZoneProps = {
	onFiles: (files: File[]) => void;
	disabled?: boolean;
	maxFiles?: number;
};

export const UploadZone = ({
	onFiles,
	disabled = false,
	maxFiles = MAX_FILES,
}: UploadZoneProps) => {
	const [isDragging, setIsDragging] = React.useState(false);
	const inputRef = React.useRef<HTMLInputElement>(null);
	const inputId = React.useId();

	const handleFiles = (fileList: FileList | null) => {
		if (!fileList) return;

		const files = Array.from(fileList)
			.filter((f) => ACCEPTED_TYPES.includes(f.type))
			.slice(0, maxFiles);

		if (files.length) {
			onFiles(files);
		}
	};

	const onDragOver = (e: React.DragEvent<HTMLLabelElement>) => {
		e.preventDefault();
		if (disabled) return;
		e.dataTransfer.dropEffect = "copy";
	};

	const onDragEnter = (e: React.DragEvent<HTMLLabelElement>) => {
		e.preventDefault();
		if (!disabled) setIsDragging(true);
	};

	const onDragLeave = (e: React.DragEvent<HTMLLabelElement>) => {
		e.preventDefault();
		// avoid flicker when moving over child elements
		if (e.currentTarget === e.target) setIsDragging(false);
	};

	const onDrop = (e: React.DragEvent<HTMLLabelElement>) => {
		e.preventDefault();
		setIsDragging(false);
		if (disabled) return;
		handleFiles(e.dataTransfer.files);
	};

	return (
		<label
			htmlFor={inputId}
			aria-disabled={disabled}
			onDragOver={onDragOver}
			onDragEnter={onDragEnter}
			onDragLeave={onDragLeave}
			onDrop={onDrop}
			className={cn(
				"block w-full rounded-lg border-2 border-dashed p-10 text-center transition-colors select-text",
				isDragging ? "border-black bg-neutral-50" : "border-neutral-300",
				disabled && "opacity-60 pointer-events-none",
			)}
		>
			<p className="text-lg font-medium">Drag & Drop media here</p>
			<p className="text-sm text-neutral-500">
				JPEG, PNG, WebP, GIF, HEIC, MP4, MOV, WebM
			</p>

			<Button
				type="button"
				variant="outline"
				className="mt-4"
				disabled={disabled}
				onClick={() => inputRef.current?.click()}
			>
				Browse files
			</Button>

			<input
				id={inputId}
				ref={inputRef}
				type="file"
				multiple
				accept={ACCEPTED_TYPES.join(",")}
				className="hidden"
				onChange={(e) => {
					handleFiles(e.target.files);
					e.target.value = "";
				}}
			/>
		</label>
	);
};
