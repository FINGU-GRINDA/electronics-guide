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
                  width="24"
                  height="26"
                  viewBox="0 0 24 26"
                  fill="none"
                  xmlns="http://www.w3.org/2000/svg"
                  className="m-4"
                >
                  <path
                    d="M19 7.16602C19.9036 7.35336 20.5853 7.66604 21.1332 8.18788C22.5 9.4898 22.5 11.5852 22.5 15.776C22.5 19.9668 22.5 22.0622 21.1332 23.3641C19.7663 24.666 17.5664 24.666 13.1667 24.666H10.8333C6.43356 24.666 4.23367 24.666 2.86684 23.3641C1.5 22.0622 1.5 19.9668 1.5 15.776C1.5 11.5852 1.5 9.4898 2.86684 8.18788C3.41471 7.66604 4.09642 7.35336 5 7.16602"
                    stroke="#C3C7D6"
                    strokeWidth="1.5"
                    strokeLinecap="round"
                  />
                  <path
                    d="M12.0295 1.33362L12 15.333M12.0295 1.33362C11.8398 1.32576 11.6489 1.39357 11.4789 1.53708C10.4213 2.42975 8.5 4.75001 8.5 4.75001M12.0295 1.33362C12.1996 1.34067 12.3689 1.40856 12.5213 1.53727C13.5786 2.4301 15.5 4.75001 15.5 4.75001"
                    stroke="#C3C7D6"
                    strokeWidth="1.5"
                    strokeLinecap="round"
                    strokeLinejoin="round"
                  />
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
