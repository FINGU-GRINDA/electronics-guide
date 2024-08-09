import React, { useState, useEffect } from "react";
import { Box, Button } from "@mui/material";

interface FileUploadProps {
  onFileChange: (file: File | null) => void;
  onAnalyzeImage: (event: React.FormEvent) => void;
  file: File | null;
  loading: boolean;
}

const FileUpload: React.FC<FileUploadProps> = ({
  onFileChange,
  onAnalyzeImage,
  file,
  loading,
}) => {
  const [preview, setPreview] = useState<string | null>(null);

  useEffect(() => {
    if (!file) {
      setPreview(null);
      return;
    }

    const objectUrl = URL.createObjectURL(file);
    setPreview(objectUrl);

    // Cleanup the object URL
    return () => URL.revokeObjectURL(objectUrl);
  }, [file]);

  return (
    <form onSubmit={onAnalyzeImage} className="space-y-4">
      <Box className="flex items-center justify-center w-full">
        <label className="flex flex-col items-center justify-center w-full h-32 border-2 border-dashed border-gray-300 rounded-lg cursor-pointer bg-gray-50 hover:bg-gray-100">
          <div className="flex flex-col items-center justify-center pt-5 pb-6">
            {preview ? (
              <img
                src={preview}
                alt="Preview"
                className="mb-3 w-24 h-24 object-cover"
              />
            ) : (
              <>
                <svg
                  aria-hidden="true"
                  className="w-10 h-10 mb-3 text-gray-400"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                  xmlns="http://www.w3.org/2000/svg"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth="2"
                    d="M7 16V12m0 0l5-5m-5 5h8m-3 4h3M5 12H4a2 2 0 00-2 2v6a2 2 0 002 2h6a2 2 0 002-2v-1m0-6h3m0 0l-5 5m0-5v4"
                  ></path>
                </svg>
                <p className="mb-2 text-sm text-gray-500 dark:text-gray-400">
                  <span className="font-semibold">Click to upload</span> or drag
                  and drop
                </p>
                <p className="text-xs text-gray-500 dark:text-gray-400">
                  SVG, PNG, JPG or GIF (MAX. 800x400px)
                </p>
              </>
            )}
          </div>
          <input
            id="dropzone-file"
            type="file"
            className="hidden"
            onChange={(e) => {
              const files = (e.target as HTMLInputElement).files;
              onFileChange(files ? files[0] : null);
            }}
          />
        </label>
      </Box>
      <Button
        type="submit"
        variant="contained"
        color="primary"
        fullWidth
        disabled={!file || loading}
      >
        Upload
      </Button>
    </form>
  );
};

export default FileUpload;
