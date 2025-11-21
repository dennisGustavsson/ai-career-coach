import React, { useState, useCallback } from "react";
import { Upload, FileText, CheckCircle, AlertCircle } from "lucide-react";
import { uploadCV } from "@/lib/api";

interface CVUploadProps {
	onAnalysisComplete: (analysis: any) => void;
}

export default function CVUpload({ onAnalysisComplete }: CVUploadProps) {
	const [isDragging, setIsDragging] = useState(false);
	const [isUploading, setIsUploading] = useState(false);
	const [error, setError] = useState<string | null>(null);
	const [fileName, setFileName] = useState<string | null>(null);

	const handleFile = async (file: File) => {
		if (file.type !== "application/pdf") {
			setError("Endast PDF-filer stöds.");
			return;
		}
		setError(null);
		setFileName(file.name);
		setIsUploading(true);
		try {
			const result = await uploadCV(file);
			onAnalysisComplete(result.analysis);
		} catch (err: any) {
			const errorMessage =
				err?.response?.data?.detail || "Kunde inte analysera CV. Försök igen.";
			setError(errorMessage);
			console.error(err);
		} finally {
			setIsUploading(false);
		}
	};

	const onDrop = useCallback((e: React.DragEvent) => {
		e.preventDefault();
		setIsDragging(false);
		if (e.dataTransfer.files && e.dataTransfer.files[0]) {
			handleFile(e.dataTransfer.files[0]);
		}
	}, []);

	return (
		<div className='w-full max-w-2xl mx-auto'>
			<div
				onDragOver={(e) => {
					e.preventDefault();
					setIsDragging(true);
				}}
				onDragLeave={() => setIsDragging(false)}
				onDrop={onDrop}
				className={`border-2 border-dashed rounded-2xl p-10 text-center transition-all cursor-pointer
          ${
						isDragging
							? "border-blue-500 bg-blue-50 scale-105"
							: "border-gray-300 hover:border-blue-400 hover:bg-gray-50"
					}
          ${
						fileName
							? "bg-green-50 border-green-400 shadow-lg shadow-green-100"
							: "shadow-md"
					}
        `}
			>
				<input
					type='file'
					accept='.pdf'
					className='hidden'
					id='cv-upload'
					onChange={(e) => e.target.files?.[0] && handleFile(e.target.files[0])}
				/>
				<label
					htmlFor='cv-upload'
					className='cursor-pointer flex flex-col items-center gap-4'
				>
					{isUploading ? (
						<div className='animate-spin rounded-full h-14 w-14 border-4 border-blue-600 border-t-transparent'></div>
					) : fileName ? (
						<>
							<div className='bg-green-500 rounded-full p-3'>
								<CheckCircle className='w-12 h-12 text-white' />
							</div>
							<span className='text-green-700 font-semibold text-lg'>
								{fileName} uppladdad!
							</span>
						</>
					) : (
						<>
							<div className='bg-linear-to-br from-blue-100 to-indigo-100 rounded-2xl p-4'>
								<Upload className='w-12 h-12 text-blue-600' />
							</div>
							<div>
								<p className='text-xl font-bold text-gray-900 mb-1'>
									Ladda upp ditt CV
								</p>
								<p className='text-sm text-gray-700'>
									Släpp din PDF här eller klicka för att välja
								</p>
							</div>
						</>
					)}
				</label>
			</div>
			{error && (
				<div className='flex items-center gap-2 text-red-600 mt-4 justify-center bg-red-50 p-3 rounded-lg border border-red-200'>
					<AlertCircle size={18} />
					<span className='text-sm font-medium'>{error}</span>
				</div>
			)}
		</div>
	);
}
