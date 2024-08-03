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
    <Box>
      <Typography variant="h5" gutterBottom>
        Project Ideas
      </Typography>
      <List>
        {projectIdeas.map((idea, index) => (
          <React.Fragment key={index}>
            <ListItem
              button
              onClick={() => onSelectProject(idea)}
              selected={selectedProject === idea}
            >
              <ListItemText primary={<ReactMarkdown>{idea}</ReactMarkdown>} />
            </ListItem>
            {index < projectIdeas.length - 1 && <Divider />}
          </React.Fragment>
        ))}
      </List>
      {selectedProject && (
        <Button
          onClick={onGetProjectDetails}
          variant="contained"
          color="secondary"
          fullWidth
          sx={{ mt: 2 }}
        >
          Get Project Details
        </Button>
      )}
    </Box>
  );
};

export default ProjectIdeasList;
