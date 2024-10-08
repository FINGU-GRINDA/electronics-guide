import React from "react";
import {
  Box,
  Button,
  List,
  ListItem,
  ListItemText,
  Divider,
  Typography,
  Card,
  CardContent,
  IconButton,
  CircularProgress,
} from "@mui/material";
import ReactMarkdown from "react-markdown";
import { motion } from "framer-motion";
import RefreshIcon from "@mui/icons-material/Refresh";

interface ProjectIdeasListProps {
  projectIdeas: string[];
  selectedProject: string | null;
  onSelectProject: (idea: string) => void;
  onGetProjectDetails: () => void;
  onRefreshIdeas: () => void;
  loading: boolean; // Loading state specific to this component
}

const ProjectIdeasList: React.FC<ProjectIdeasListProps> = ({
  projectIdeas,
  selectedProject,
  onSelectProject,
  onGetProjectDetails,
  onRefreshIdeas,
  loading, // Receive the loading state specific to this component
}) => {
  return (
    <Box className="p-6 bg-gray-100 shadow-lg rounded-xl">
      <motion.div
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
      >
        <Card className="mb-4">
          <CardContent>
            <Box
              display="flex"
              justifyContent="space-between"
              alignItems="center"
            >
              <Typography
                variant="h5"
                className="text-center text-2xl font-bold text-gray-700"
              >
                Project Ideas
              </Typography>
              <IconButton
                onClick={onRefreshIdeas}
                color="primary"
                className="transition duration-300 ease-in-out transform hover:scale-110"
                disabled={loading} // Disable the button during loading
              >
                {loading ? (
                  <CircularProgress size={24} /> // Show loading spinner during refresh
                ) : (
                  <RefreshIcon />
                )}
              </IconButton>
            </Box>
          </CardContent>
        </Card>
      </motion.div>
      <List className="space-y-2">
        {projectIdeas.map((idea, index) => (
          <React.Fragment key={index}>
            <motion.div
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.5, delay: index * 0.1 }}
            >
              <ListItem
                button
                onClick={() => onSelectProject(idea)}
                selected={selectedProject === idea}
                className={`bg-white hover:bg-gray-100 rounded-lg shadow-md transition duration-300 ease-in-out transform ${
                  selectedProject === idea ? "bg-blue-50" : ""
                }`}
              >
                <ListItemText
                  primary={<ReactMarkdown>{idea}</ReactMarkdown>}
                  primaryTypographyProps={{ className: "text-gray-600" }}
                />
              </ListItem>
              {index < projectIdeas.length - 1 && <Divider />}
            </motion.div>
          </React.Fragment>
        ))}
      </List>
      {selectedProject && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 0.5 }}
        >
          <Button
            onClick={onGetProjectDetails}
            variant="contained"
            color="primary"
            fullWidth
            className="mt-4 py-2 text-lg font-semibold transition duration-300 ease-in-out transform hover:scale-105"
            sx={{
              backgroundColor: "#3f51b5",
              "&:hover": {
                backgroundColor: "#303f9f",
              },
            }}
          >
            Get Project Details
          </Button>
        </motion.div>
      )}
    </Box>
  );
};

export default ProjectIdeasList;
