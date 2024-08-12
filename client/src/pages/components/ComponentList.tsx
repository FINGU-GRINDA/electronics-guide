import React from "react";
import { Box, Typography, List, ListItem, ListItemText } from "@mui/material";
import { motion } from "framer-motion";

interface ComponentListProps {
  components: string[];
}

const ComponentList: React.FC<ComponentListProps> = ({ components }) => {
  return (
    <Box
      sx={{
        mb: 4,
        mx: "auto",
        width: "100%", // Set the width to 100% to make it as wide as possible
        padding: 3,
        backgroundColor: "#1e1e1e",
        borderRadius: "16px",
        boxShadow: "0 8px 20px rgba(0, 0, 0, 0.7)",
        transition: "transform 0.3s ease-in-out",
        "&:hover": {
          transform: "translateY(-5px)",
          boxShadow: "0 12px 30px rgba(0, 0, 0, 0.9)",
        },
      }}
    >
      <Typography
        variant="h5"
        align="center"
        sx={{
          fontWeight: 600,
          color: "#00bfa5", // Updated to match the teal color
          letterSpacing: "0.05rem",
          marginBottom: 3,
          textTransform: "uppercase",
          fontSize: "1.5rem",
        }}
      >
        Components
      </Typography>
      <List>
        {components.map((component, index) => (
          <motion.div
            key={index}
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: index * 0.1 }}
          >
            <ListItem
              sx={{
                padding: "12px 24px",
                backgroundColor: index % 2 === 0 ? "#2e2e2e" : "#252525",
                borderRadius: "8px",
                marginBottom: "8px",
                transition: "background-color 0.3s ease-in-out",
                "&:hover": {
                  backgroundColor: "#333",
                },
              }}
            >
              <ListItemText
                primary={component}
                primaryTypographyProps={{
                  align: "center",
                  sx: {
                    color: "#fffb", // Updated to match the teal color
                    fontWeight: "medium",
                    fontSize: "1.1rem",
                  },
                }}
              />
            </ListItem>
          </motion.div>
        ))}
      </List>
    </Box>
  );
};

export default ComponentList;
