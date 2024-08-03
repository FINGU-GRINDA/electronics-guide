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
  );
};

export default ComponentList;
