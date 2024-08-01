import React, { useState, useEffect, useRef, useMemo } from "react";
import {
  analyzeImage,
  getProjectDetails,
  downloadTutorialPdf,
} from "../services/api";
import ReactMarkdown from "react-markdown";
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
import { Worker, Viewer } from "@react-pdf-viewer/core";
import "@react-pdf-viewer/core/lib/styles/index.css";
import { defaultLayoutPlugin } from "@react-pdf-viewer/default-layout";

const FileUpload: React.FC = () => {
  const [file, setFile] = useState<File | null>(null);
  const [components, setComponents] = useState<string[]>([]);
  const [projectIdeas, setProjectIdeas] = useState<string[]>([]);
  const [selectedProject, setSelectedProject] = useState<string | null>(null);
  const [tutorial, setTutorial] = useState<string>("");
  const [loading, setLoading] = useState<boolean>(false);
  const [pdfBlob, setPdfBlob] = useState<Blob | null>(null);
  const pdfBlobUrlRef = useRef<string | null>(null);

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
      console.log("Project Ideas Response: ", data);

      // Extract components from the response
      const componentsData = data.components;

      // Extract project ideas from the response
      const projectIdeasData = data.project_ideas;

      setComponents(componentsData);
      setProjectIdeas(projectIdeasData);
      setLoading(false);
    }
  };

  const handleGetProjectDetails = async () => {
    if (file && selectedProject !== null) {
      setLoading(true);
      setTutorial(""); // Reset tutorial before starting
      await getProjectDetails(file, selectedProject, (data) => {
        setTutorial((prev) => prev + data); // Append new data to the tutorial
      });
      setLoading(false);
      // Fetch the PDF file
      const pdfData = await downloadTutorialPdf();
      console.log("PDF Blob:", pdfData);
      setPdfBlob(pdfData);
    }
  };

  const defaultLayoutPluginInstance = defaultLayoutPlugin();

  useEffect(() => {
    if (pdfBlob) {
      // Revoke the previous object URL to avoid memory leaks
      if (pdfBlobUrlRef.current) {
        URL.revokeObjectURL(pdfBlobUrlRef.current);
      }
      pdfBlobUrlRef.current = URL.createObjectURL(pdfBlob);
      console.log("PDF Blob URL:", pdfBlobUrlRef.current);
    }
  }, [pdfBlob]);

  const pdfUrl = useMemo(() => pdfBlobUrlRef.current, [pdfBlob]);

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
            {components.length > 0 && (
              <Card variant="outlined" sx={{ mb: 4 }}>
                <CardContent>
                  <Typography variant="h6">Components</Typography>
                  <List>
                    {components.map((component, index) => (
                      <ListItem key={index}>
                        <ListItemText primary={component} />
                      </ListItem>
                    ))}
                  </List>
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
                        onClick={() => setSelectedProject(idea)} // Set the project string
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
            {pdfUrl && (
              <div>
                <Worker
                  workerUrl={`https://unpkg.com/pdfjs-dist@3.11.174/build/pdf.worker.min.js`}
                >
                  <Viewer
                    fileUrl={pdfUrl}
                    plugins={[defaultLayoutPluginInstance]}
                  />
                </Worker>
              </div>
            )}
          </Box>
        </CardContent>
      </Card>
    </Container>
  );
};

export default FileUpload;
