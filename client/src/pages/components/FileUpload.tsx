import React, { useState, useEffect } from "react";
import { Box, Button, Typography } from "@mui/material";
import { motion } from "framer-motion";
import CloudUploadIcon from "@mui/icons-material/CloudUpload";
import InfoOutlinedIcon from "@mui/icons-material/InfoOutlined";

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
        sx={{
          width: "100%",
          maxWidth: 600,
          margin: "0 auto",
          position: "relative",
        }}
      >
        {/* Vertical line */}
        <Box
          sx={{
            position: "absolute",
            left: 24, // Moved to the right
            top: 164,
            bottom: 50,
            width: 2,
            backgroundColor: "#e2e8f0",
          }}
        />

        {/* Your old upload button design */}
        <Box
          className="flex items-center justify-center w-full"
          sx={{
            mb: 3,
            padding: "16px",
            backgroundColor: "#1c1c1c",
            borderRadius: 2,
            border: "2px dashed #555",
          }}
        >
          <motion.label
            whileHover={{
              scale: 0.97,
              backgroundColor: "#2a2a2a",
            }}
            transition={{ duration: 0.3 }}
            className="flex flex-col items-center justify-center w-full h-32 cursor-pointer rounded-lg"
            style={{ backgroundColor: "#1c1c1c" }}
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
                  <CloudUploadIcon sx={{ color: "white", fontSize: 40 }} />
                  <Typography
                    variant="body2"
                    sx={{ color: "white", fontWeight: "bold", mt: 2 }}
                  >
                    Click to upload or drag and drop
                  </Typography>
                  <Typography variant="caption" sx={{ color: "#94a3b8" }}>
                    SVG, PNG, JPG or GIF (MAX. 800x400px)
                  </Typography>
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

        {/* Rest of your original design */}
        <Box sx={{ display: "flex", alignItems: "center", mb: 1, ml: 6 }}>
          <InfoOutlinedIcon sx={{ mr: 1, fontSize: 16, color: "#64748b" }} />
          <Typography variant="caption" sx={{ color: "#64748b" }}>
            Upload tips
          </Typography>
        </Box>

        <Typography
          variant="body2"
          sx={{ mb: 3, pl: 1, color: "#64748b", ml: 6 }}
        >
          No image? Try one of the demo images:
        </Typography>

        <Box sx={{ position: "relative", pl: 6, mb: 2, mt: 4 }}>
          <Box
            sx={{
              position: "absolute",
              left: 12,
              top: -2,
              width: 24,
              height: 24,
              borderRadius: "50%",
              backgroundColor: "white",
              border: "1px solid #000000",
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              zIndex: 2,
            }}
          >
            <Typography
              variant="body2"
              sx={{ fontWeight: "bold", color: "#4a5568" }}
            >
              2
            </Typography>
          </Box>
          <Typography variant="body1" sx={{ color: "#2d3748", ml: 2 }}>
            Choose from component cards
          </Typography>
        </Box>

        <Box sx={{ position: "relative", pl: 6, mt: 4 }}>
          <Box
            sx={{
              position: "absolute",
              left: 12,
              width: 24,
              height: 24,
              borderRadius: "50%",
              backgroundColor: "white",
              border: "1px solid #000000",
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              zIndex: 2,
            }}
          >
            <Typography
              variant="body2"
              sx={{ fontWeight: "bold", color: "#4a5568" }}
            >
              3
            </Typography>
          </Box>
          <Typography variant="body1" sx={{ color: "#2d3748", ml: 2 }}>
            Place components in the circuit
          </Typography>
        </Box>

        <Button
          type="submit"
          variant="contained"
          color="primary"
          fullWidth
          disabled={!file || loading}
          sx={{
            backgroundColor: "#00bfa5",
            "&:hover": {
              backgroundColor: "#00897b",
            },
          }}
        >
          Upload
        </Button>
      </Box>
    </form>
  );
};

export default FileUpload;
