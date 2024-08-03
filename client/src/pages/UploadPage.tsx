import React, { useState } from "react";
import {
  Container,
  Card,
  CardContent,
  Box,
  CircularProgress,
} from "@mui/material";
import { analyzeImage, getProjectDetails } from "../services/api";
import FileUpload from "../components/FileUpload";
import ComponentList from "../components/ComponentList";
import ProjectIdeasList from "../components/ProjectIdeasList";
import ProjectTutorial from "../components/ProjectTutorial";

const UploadPage: React.FC = () => {
  const [file, setFile] = useState<File | null>(null);
  const [components, setComponents] = useState<string[]>([]);
  const [projectIdeas, setProjectIdeas] = useState<string[]>([]);
  const [selectedProject, setSelectedProject] = useState<string | null>(null);
  const [tutorial, setTutorial] = useState<string>("");
  const [loading, setLoading] = useState<boolean>(false);

  const handleFileChange = (file: File | null) => {
    setFile(file);
  };

  const handleAnalyzeImage = async (event: React.FormEvent) => {
    event.preventDefault();
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
      await getProjectDetails(file, selectedProject, (data) => {
        if (data.project_overview) {
          const markdown = convertJsonToMarkdown(data.project_overview);
          setTutorial((prev) => prev + markdown);
        } else if (data.section && data.content) {
          const sectionMarkdown = `${data.content}\n\n`;
          setTutorial((prev) => prev + sectionMarkdown);
        }
      });
      setLoading(false);
    }
  };

  const convertJsonToMarkdown = (json: string) => {
    return json.replace(/\\n/g, "\n").replace(/\* /g, "- ");
  };

  return (
    <Container maxWidth="md">
      <Card variant="outlined" sx={{ mt: 4, p: 2 }}>
        <CardContent>
          <FileUpload
            onFileChange={handleFileChange}
            onAnalyzeImage={handleAnalyzeImage}
            file={file}
            loading={loading}
          />
          {loading && (
            <Box display="flex" justifyContent="center" mt={2}>
              <CircularProgress />
            </Box>
          )}
          <Box mt={4}>
            {components.length > 0 && <ComponentList components={components} />}
            {projectIdeas.length > 0 && (
              <ProjectIdeasList
                projectIdeas={projectIdeas}
                selectedProject={selectedProject}
                onSelectProject={setSelectedProject}
                onGetProjectDetails={handleGetProjectDetails}
              />
            )}
          </Box>
          <Box mt={4}>
            {tutorial && <ProjectTutorial tutorial={tutorial} />}
          </Box>
        </CardContent>
      </Card>
    </Container>
  );
};

export default UploadPage;
