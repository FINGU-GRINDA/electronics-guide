import React, { useState } from "react";
import {
  Container,
  Box,
  CircularProgress,
  IconButton,
  Stack,
} from "@mui/material";
import StopIcon from "@mui/icons-material/Stop";
import { analyzeImage, getProjectDetails } from "../services/api";
import FileUpload from "./components/FileUpload";
import ComponentList from "./components/ComponentList";
import ProjectIdeasList from "./components/ProjectIdeasList";
import ProjectTutorial from "./components/ProjectTutorial";
import { motion } from "framer-motion";

const UploadPage: React.FC = () => {
  const [file, setFile] = useState<File | null>(null);
  const [components, setComponents] = useState<string[]>([]);
  const [projectIdeas, setProjectIdeas] = useState<string[]>([]);
  const [selectedProject, setSelectedProject] = useState<string | null>(null);
  const [tutorial, setTutorial] = useState<string>("");
  const [loading, setLoading] = useState<boolean>(false);
  const [ideasLoading, setIdeasLoading] = useState<boolean>(false);
  const [abortController, setAbortController] =
    useState<AbortController | null>(null);

  const handleFileChange = (file: File | null) => {
    setFile(file);
  };

  const handleAnalyzeImage = async (event?: React.FormEvent) => {
    if (event) event.preventDefault();
    if (file) {
      setLoading(true);
      const data = await analyzeImage(file);
      console.log("Project Ideas Response: ", data);

      const componentsData = data.components || [];
      const projectIdeasData = data.project_ideas || [];

      setComponents(componentsData);
      setProjectIdeas(projectIdeasData);
      setLoading(false);
    }
  };

  const handleGetProjectDetails = async () => {
    if (file && selectedProject !== null) {
      setLoading(true);
      setTutorial("");
      const controller = new AbortController();
      setAbortController(controller);

      try {
        await getProjectDetails(
          file,
          selectedProject,
          (data) => {
            if (data.project_overview) {
              setTutorial((prev) => prev + data.project_overview);
            } else if (data.section && data.content) {
              setTutorial((prev) => prev + data.content);
            }
          },
          controller.signal
        );
      } catch (error) {
        if ((error as Error).name === "AbortError") {
          console.log("Streaming aborted");
        } else {
          console.error("Error during streaming:", error);
        }
      }
      setLoading(false);
    }
  };

  const handleRefreshIdeas = async () => {
    if (file) {
      setIdeasLoading(true);
      const data = await analyzeImage(file);
      console.log("Refreshed Project Ideas: ", data);

      const projectIdeasData = data.project_ideas || [];
      setProjectIdeas(projectIdeasData);
      setIdeasLoading(false);
    }
  };

  const handleStopStreaming = () => {
    if (abortController) {
      abortController.abort();
    }
  };

  return (
    <Container maxWidth="md" sx={{ mt: 4 }}>
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
      >
        <Box sx={{ textAlign: "center", mb: 4 }}>
          {/* Add any additional content or headers here if needed */}
        </Box>
      </motion.div>
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.3, duration: 0.5 }}
      >
        <FileUpload
          onFileChange={handleFileChange}
          onAnalyzeImage={handleAnalyzeImage}
          file={file}
          loading={loading}
        />
      </motion.div>

      <Stack spacing={4} mt={4}>
        {components.length > 0 && (
          <motion.div
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.5 }}
          >
            <ComponentList components={components} />
          </motion.div>
        )}

        {projectIdeas.length > 0 && (
          <motion.div
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.5 }}
          >
            <ProjectIdeasList
              projectIdeas={projectIdeas}
              selectedProject={selectedProject}
              onSelectProject={setSelectedProject}
              onGetProjectDetails={handleGetProjectDetails}
              onRefreshIdeas={handleRefreshIdeas}
              loading={ideasLoading}
            />
          </motion.div>
        )}

        {tutorial && (
          <motion.div
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.5 }}
          >
            <ProjectTutorial tutorial={tutorial} />
          </motion.div>
        )}
      </Stack>

      {loading && (
        <Box display="flex" justifyContent="center" mt={4}>
          <CircularProgress sx={{ color: "#00bfa5" }} />{" "}
          {/* Updated to match the teal color */}
        </Box>
      )}
      {loading && (
        <Box mt={2} display="flex" justifyContent="center">
          <IconButton
            color="error"
            onClick={handleStopStreaming}
            sx={{
              border: "1px solid",
              borderRadius: "8px",
              color: "#00bfa5", // Updated to match the teal color
              borderColor: "#00bfa5", // Updated to match the teal color
            }}
          >
            <StopIcon />
          </IconButton>
        </Box>
      )}
    </Container>
  );
};

export default UploadPage;
