import React from "react";
import {
  Card,
  CardContent,
  Typography,
  List,
  ListItem,
  ListItemText,
  
} from "@mui/material";

interface ComponentListProps {
  components: string[];
}

const ComponentList: React.FC<ComponentListProps> = ({ components }) => {
  return (
    <Card
      variant="outlined"
      sx={{
        mb: 4,
        mx: "auto",
        maxWidth: 600,
        backgroundColor: "#f9f9f9",
        borderRadius: 4,
        boxShadow: 3,
      }}
    >
      <CardContent>
        <Typography
          variant="h6"
          align="center"
          sx={{ fontWeight: "bold", color: "#333" }}
        >
          Components
        </Typography>
        <List sx={{ mt: 2 }}>
          {components.map((component, index) => (
            <ListItem
              key={index}
              sx={{
                borderBottom: "1px solid #ddd",
                "&:last-child": { borderBottom: "none" },
              }}
            >
              <ListItemText
                primary={component}
                primaryTypographyProps={{
                  align: "center",
                  sx: { color: "#555", fontWeight: "medium" },
                }}
              />
            </ListItem>
          ))}
        </List>
      </CardContent>
    </Card>
  );
};

export default ComponentList;
