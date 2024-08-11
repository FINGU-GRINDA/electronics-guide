import React, { useState, useEffect } from "react";
import { Box, Button } from "@mui/material";
import { motion } from "framer-motion";

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

    return () => URL.revokeObjectURL(objectUrl);
  }, [file]);

  return (
    <form onSubmit={onAnalyzeImage} className="space-y-4">
      <Box
        className="flex items-center justify-center w-full"
        sx={{
          mb: 3,
          padding: "16px",
          backgroundColor: "#1c1c1c", // Updated background color to match the theme
          borderRadius: 2,
          border: "2px dashed #555", // Consistent with the rest of the dark theme
        }}
      >
        <motion.label
          whileHover={{
            scale: 0.97, // Slightly smaller on hover
            backgroundColor: "#2a2a2a", // Darker shade of black for hover effect
          }}
          transition={{ duration: 0.3 }}
          className="flex flex-col items-center justify-center w-full h-32 cursor-pointer rounded-lg"
          style={{ backgroundColor: "#1c1c1c" }} // Match the initial background color
        >
          <div className="flex flex-col items-center justify-center pt-5 pb-6">
            {preview ? (
              <img
                src={preview}
                alt="Preview"
                className="mb-3 w-24 h-24 object-cover"
                style={{
                  borderRadius: "8px",
                  boxShadow: "0 4px 12px rgba(0, 0, 0, 0.3)",
                }}
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
                <p className="mb-2 text-sm text-gray-400">
                  <span className="font-semibold">Click to upload</span> or drag
                  and drop
                </p>
                <p className="text-xs text-gray-400">
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
        </motion.label>
      </Box>
      <Button
        type="submit"
        variant="contained"
        color="primary"
        fullWidth
        disabled={!file || loading}
        sx={{
          backgroundColor: "#00bfa5", // Matching with the primary color in the theme
          "&:hover": {
            backgroundColor: "#00897b", // Consistent hover effect
          },
        }}
      >
        Upload
      </Button>
    </form>
  );
};

export default FileUpload;
