import React from "react";
import {
  Box,
  Button,
  List,
  ListItem,
  ListItemText,
  Divider,
  Typography,
} from "@mui/material";
import ReactMarkdown from "react-markdown";

interface ProjectIdeasListProps {
  projectIdeas: string[];
  selectedProject: string | null;
  onSelectProject: (idea: string) => void;
  onGetProjectDetails: () => void;
}

const ProjectIdeasList: React.FC<ProjectIdeasListProps> = ({
  projectIdeas,
  selectedProject,
  onSelectProject,
  onGetProjectDetails,
}) => {
  return (
    <Box className="p-6 bg-white shadow-lg rounded-xl">
      <Typography
        variant="h5"
        className="text-center text-2xl font-bold text-gray-700 mb-4"
      >
        Project Ideas
      </Typography>
      <List className="space-y-2">
        {projectIdeas.map((idea, index) => (
          <React.Fragment key={index}>
            <ListItem
              button
              onClick={() => onSelectProject(idea)}
              selected={selectedProject === idea}
              className={`bg-gray-50 hover:bg-gray-100 rounded-lg ${
                selectedProject === idea ? "bg-blue-50" : ""
              }`}
            >
              <ListItemText
                primary={<ReactMarkdown>{idea}</ReactMarkdown>}
                primaryTypographyProps={{ className: "text-gray-600" }}
              />
            </ListItem>
            {index < projectIdeas.length - 1 && <Divider />}
          </React.Fragment>
        ))}
      </List>
      {selectedProject && (
        <Button
          onClick={onGetProjectDetails}
          variant="contained"
          color="primary"
          fullWidth
          className="mt-4"
        >
          Get Project Details
        </Button>
      )}
    </Box>
  );
};

export default ProjectIdeasList;
