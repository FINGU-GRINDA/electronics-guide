import React from "react";
import { Card, CardContent, Typography } from "@mui/material";
import ReactMarkdown from "react-markdown";

interface ProjectTutorialProps {
  tutorial: string;
}

const ProjectTutorial: React.FC<ProjectTutorialProps> = ({ tutorial }) => {
  return (
    <Card variant="outlined">
      <CardContent>
        <Typography variant="h6" gutterBottom>
          Project Tutorial
        </Typography>
        <ReactMarkdown className="prose">{tutorial}</ReactMarkdown>
      </CardContent>
    </Card>
  );
};

export default ProjectTutorial;
