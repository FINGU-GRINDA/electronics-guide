import React, { useEffect, useRef } from "react";
import { Card, CardContent, Typography, Box } from "@mui/material";
import parse from "html-react-parser";

interface ProjectTutorialProps {
  tutorial: string;
}

const ProjectTutorial: React.FC<ProjectTutorialProps> = ({ tutorial }) => {
  const tutorialRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (tutorialRef.current) {
      tutorialRef.current.scrollTop = tutorialRef.current.scrollHeight;
    }
  }, [tutorial]);

  return (
    <Card variant="outlined">
      <CardContent>
        <Typography variant="h6" gutterBottom>
          Project Tutorial
        </Typography>
        <Box
          ref={tutorialRef}
          sx={{
            maxHeight: "500px",
            overflowY: "auto",
            border: "1px solid #ccc",
            borderRadius: "8px",
            padding: "16px",
            backgroundColor: "#f9f9f9",
            boxShadow: "0 0 10px rgba(0, 0, 0, 0.1)",
            fontFamily: "monospace",
          }}
        >
          {parse(tutorial)}
        </Box>
      </CardContent>
    </Card>
  );
};

export default ProjectTutorial;
