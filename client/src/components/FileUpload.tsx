import React, { useState } from "react";
import { analyzeImage, getProjectDetails } from "../services/api";
import ReactMarkdown from "react-markdown";
import { ClipLoader } from "react-spinners";
import {
  Box,
  Button,
  Card,
  CardContent,
  Container,
  Input,
  Typography,
  CircularProgress,
  List,
  ListItem,
  ListItemText,
  Divider,
} from "@mui/material";

const FileUpload: React.FC = () => {
  const [file, setFile] = useState<File | null>(null);
  const [description, setDescription] = useState<string>("");
  const [projectIdeas, setProjectIdeas] = useState<string[]>([]);
  const [selectedProject, setSelectedProject] = useState<string>("");
  const [tutorial, setTutorial] = useState<string>("");
  const [loading, setLoading] = useState<boolean>(false);

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    if (event.target.files) {
      setFile(event.target.files[0]);
    }
  };

  const handleAnalyzeImage = async (event: React.FormEvent) => {
    event.preventDefault();
    if (file) {
      setLoading(true);
      const data = await analyzeImage(file);
      setDescription(data.project_ideas[0]); // Assuming the first item is the description
      const cleanedData = data.project_ideas
        .slice(1)
        .filter((idea: string) => idea.trim() !== "");
      setProjectIdeas(cleanedData);
      setLoading(false);
    }
  };

  const handleGetProjectDetails = async () => {
    if (file && selectedProject) {
      setLoading(true);
      const data = await getProjectDetails(file, selectedProject);
      setTutorial(data.tutorial);
      setLoading(false);
    }
  };

  return (
    <Container maxWidth="md">
      <Card variant="outlined" sx={{ mt: 4, p: 2 }}>
        <CardContent>
          <form onSubmit={handleAnalyzeImage}>
            <Box mb={2}>
              <Input
                type="file"
                onChange={handleFileChange}
                fullWidth
                disableUnderline
              />
            </Box>
            <Button
              type="submit"
              variant="contained"
              color="primary"
              fullWidth
              disabled={!file}
            >
              Upload
            </Button>
          </form>
          {loading && (
            <Box display="flex" justifyContent="center" mt={2}>
              <CircularProgress />
            </Box>
          )}
          <Box mt={4}>
            {description && (
              <Card variant="outlined" sx={{ mb: 4 }}>
                <CardContent>
                  <Typography variant="h6">Project Description</Typography>
                  <ReactMarkdown>{description}</ReactMarkdown>
                </CardContent>
              </Card>
            )}
            {projectIdeas.length > 0 && (
              <Box>
                <Typography variant="h5" gutterBottom>
                  Project Ideas
                </Typography>
                <List>
                  {projectIdeas.map((idea, index) => (
                    <React.Fragment key={index}>
                      <ListItem
                        button
                        onClick={() => setSelectedProject(idea)}
                        selected={selectedProject === idea}
                      >
                        <ListItemText
                          primary={<ReactMarkdown>{idea}</ReactMarkdown>}
                        />
                      </ListItem>
                      {index < projectIdeas.length - 1 && <Divider />}
                    </React.Fragment>
                  ))}
                </List>
                {selectedProject && (
                  <Button
                    onClick={handleGetProjectDetails}
                    variant="contained"
                    color="secondary"
                    fullWidth
                    sx={{ mt: 2 }}
                  >
                    Get Project Details
                  </Button>
                )}
              </Box>
            )}
          </Box>
          <Box mt={4}>
            {tutorial && (
              <Card variant="outlined">
                <CardContent>
                  <Typography variant="h6" gutterBottom>
                    Project Tutorial
                  </Typography>
                  <ReactMarkdown className="prose">{tutorial}</ReactMarkdown>
                </CardContent>
              </Card>
            )}
          </Box>
        </CardContent>
      </Card>
    </Container>
  );
};

export default FileUpload;
