// App.tsx
import React from "react";
import {
  AppBar,
  Toolbar,
  Container,
  CssBaseline,
  Typography,
  Box,
  Button,
  IconButton,
} from "@mui/material";
import MenuIcon from "@mui/icons-material/Menu";
import { ThemeProvider, createTheme } from "@mui/material/styles";
import UploadPage from "./pages/UploadPage";

const theme = createTheme({
  palette: {
    primary: {
      main: "#1976d2",
    },
    background: {
      default: "#f5f5f5",
    },
  },
  typography: {
    h1: {
      fontSize: "2.5rem",
      fontWeight: 700,
      color: "#333",
    },
    h6: {
      fontSize: "1.25rem",
      fontWeight: 500,
    },
  },
});

const App: React.FC = () => {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <AppBar position="static">
        <Toolbar>
          <IconButton edge="start" color="inherit" aria-label="menu">
            <MenuIcon />
          </IconButton>
          <Typography variant="h6" style={{ flexGrow: 1 }}>
            TechBlueprint
          </Typography>
        </Toolbar>
      </AppBar>
      <Container maxWidth="xl" className="min-h-screen bg-gray-100 px-4 py-10">
        <Box textAlign="center" mb={4}>
          <Typography variant="h1">Welcome to TechBlueprint</Typography>
          <Typography variant="h6" color="textSecondary">
            Upload your electronic component images to get project suggestions
            and step-by-step guides.
          </Typography>
        </Box>
        <UploadPage />
      </Container>
    </ThemeProvider>
  );
};

export default App;
