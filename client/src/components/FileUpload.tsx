import React from 'react';
import { Box, Button, Input } from '@mui/material';

interface FileUploadProps {
  onFileChange: (file: File | null) => void;
  onAnalyzeImage: (event: React.FormEvent) => void;
  file: File | null;
  loading: boolean;
}

const FileUpload: React.FC<FileUploadProps> = ({ onFileChange, onAnalyzeImage, file, loading }) => {
  return (
    <form onSubmit={onAnalyzeImage}>
      <Box mb={2}>
        <Input type="file" onChange={(e) => {
          const files = (e.target as HTMLInputElement).files;
          onFileChange(files ? files[0] : null);
        }} fullWidth disableUnderline />
      </Box>
      <Button type="submit" variant="contained" color="primary" fullWidth disabled={!file || loading}>
        Upload
      </Button>
    </form>
  );
};

export default FileUpload;
