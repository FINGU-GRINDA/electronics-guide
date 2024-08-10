import React, { useState } from "react";
import {
  Container,
  Card,
  CardContent,
  Box,
  CircularProgress,
  IconButton,
} from "@mui/material";
import StopIcon from "@mui/icons-material/Stop";
import { analyzeImage, getProjectDetails } from "../services/api";
import FileUpload from "./components/FileUpload";
import ComponentList from "./components/ComponentList";
import ProjectIdeasList from "./components/ProjectIdeasList";
import ProjectTutorial from "./components/ProjectTutorial";

const UploadPage: React.FC = () => {
  const [file, setFile] = useState<File | null>(null);
  const [components, setComponents] = useState<string[]>([]);
  const [projectIdeas, setProjectIdeas] = useState<string[]>([]);
  const [selectedProject, setSelectedProject] = useState<string | null>(null);
  const [tutorial, setTutorial] = useState<string>("");
  const [loading, setLoading] = useState<boolean>(false); // For image analysis and get project details
  const [ideasLoading, setIdeasLoading] = useState<boolean>(false); // For refreshing project ideas
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
      setLoading(true); // Only affect the loading for get project details
      setTutorial("");
      const controller = new AbortController();
      setAbortController(controller);

      try {
        await getProjectDetails(
          file,
          selectedProject,
          (data) => {
            if (data.project_overview) {
              // Handle the project overview first
              setTutorial((prev) => prev + data.project_overview);
            } else if (data.section && data.content) {
              // Handle the regular section content
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
      setLoading(false); // End the loading state for get project details
    }
  };

  const handleRefreshIdeas = async () => {
    if (file) {
      setIdeasLoading(true); // Start loading for refresh
      const data = await analyzeImage(file);
      console.log("Refreshed Project Ideas: ", data);

      const projectIdeasData = data.project_ideas || [];
      setProjectIdeas(projectIdeasData);
      setIdeasLoading(false); // Stop loading after refresh
    }
  };

  const handleStopStreaming = () => {
    if (abortController) {
      abortController.abort();
    }
  };

  return (
    <Container maxWidth="xl" className="bg-white shadow-md rounded-lg p-4 mt-4">
      <Card variant="outlined">
        <CardContent>
          <FileUpload
            onFileChange={handleFileChange}
            onAnalyzeImage={handleAnalyzeImage}
            file={file}
            loading={loading} // Linked to general analysis and get project details
          />

          <Box mt={4}>
            {components.length > 0 && <ComponentList components={components} />}
            {projectIdeas.length > 0 && (
              <ProjectIdeasList
                projectIdeas={projectIdeas}
                selectedProject={selectedProject}
                onSelectProject={setSelectedProject}
                onGetProjectDetails={handleGetProjectDetails} // Trigger original loading
                onRefreshIdeas={handleRefreshIdeas} // Separate refresh function with its own loading
                loading={ideasLoading} // Separate loading state for refreshing ideas
              />
            )}
          </Box>
          <Box mt={4}>
            {tutorial && <ProjectTutorial tutorial={tutorial} />}
          </Box>
          {loading && (
            <Box display="flex" justifyContent="center" mt={2}>
              <CircularProgress />
            </Box>
          )}
          {loading && (
            <Box mt={2} display="flex" justifyContent="center">
              <IconButton
                color="secondary"
                onClick={handleStopStreaming}
                sx={{ border: "1px solid", borderRadius: "8px" }}
              >
                <StopIcon />
              </IconButton>
            </Box>
          )}
        </CardContent>
      </Card>
    </Container>
  );
};

export default UploadPage;
