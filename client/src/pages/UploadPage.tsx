import React, { useState } from "react";
import { Box, CircularProgress, IconButton, Divider } from "@mui/material";
import StopIcon from "@mui/icons-material/Stop";
import { analyzeImage, getProjectDetails } from "../services/api";
import FileUpload from "./components/FileUpload";
import ComponentList from "./components/ComponentList";
import ProjectIdeasList from "./components/ProjectIdeasList";
import ProjectTutorial from "./components/ProjectTutorial";
import { motion } from "framer-motion";
import robot from "../assets/Bot.webp";

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
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
    >
      <Box sx={{ display: "flex", gap: 4 }}>
        <Box sx={{ display: "flex", flexDirection: "column", gap: 4 }}>
          <FileUpload
            onFileChange={handleFileChange}
            onAnalyzeImage={handleAnalyzeImage}
            file={file}
            loading={loading}
          />

          {components.length > 0 && <ComponentList components={components} />}

          {projectIdeas.length > 0 && (
            <ProjectIdeasList
              projectIdeas={projectIdeas}
              selectedProject={selectedProject}
              onSelectProject={setSelectedProject}
              onGetProjectDetails={handleGetProjectDetails}
              onRefreshIdeas={handleRefreshIdeas}
              loading={ideasLoading}
            />
          )}

          {tutorial && <ProjectTutorial tutorial={tutorial} />}

          {loading && (
            <Box display="flex" justifyContent="center" mt={4}>
              <CircularProgress sx={{ color: "#00bfa5" }} />
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
                  color: "#00bfa5",
                  borderColor: "#00bfa5",
                }}
              >
                <StopIcon />
              </IconButton>
            </Box>
          )}
        </Box>
        <Divider orientation="vertical" flexItem />

        {/* Right side: Before and After Image */}
        <img
          src={robot}
          alt="robot"
          style={{
            maxWidth: "400px", // Fixed width
            height: "460px", // Maintain aspect ratio
            borderRadius: "50px", // Curved corners
            boxShadow: "0px 8px 15px rgba(0, 0, 0, 0.3)", // Shadow effect
            transition: "transform 0.3s ease",
          }}
          // onMouseOver={(e) => {
          //   (e.currentTarget as HTMLElement).style.transform = "scale(1.05)";
          // }}
          // onMouseOut={(e) => {
          //   (e.currentTarget as HTMLElement).style.transform = "scale(1)";
          // }}
        />
      </Box>
    </motion.div>
  );
};

export default UploadPage;
