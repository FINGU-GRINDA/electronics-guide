import React from "react";
import {
  AppBar,
  Toolbar,
  CssBaseline,
  Typography,
  Box,
  IconButton,
} from "@mui/material";
import MenuIcon from "@mui/icons-material/Menu";
import { ThemeProvider, createTheme, styled } from "@mui/material/styles";
import UploadPage from "./pages/UploadPage";
import { motion } from "framer-motion";

const theme = createTheme({
  palette: {
    mode: "dark", // Set the theme to dark mode
    primary: {
      main: "#bb86fc",
    },
    background: {
      default: "#0d0d0d", // Adjusted to a more consistent black
      paper: "#1c1c1c", // Slightly lighter black for components
    },
    text: {
      primary: "#ffffff",
      secondary: "#b0b0b0",
    },
  },
  typography: {
    h1: {
      fontSize: "3rem",
      fontWeight: 800,
      color: "#ffffff",
      letterSpacing: "0.05rem",
      marginBottom: "20px",
    },
    h6: {
      fontSize: "1.2rem",
      fontWeight: 500,
      color: "#b0b0b0",
    },
  },
  components: {
    MuiAppBar: {
      styleOverrides: {
        root: {
          backgroundColor: "#1c1c1c",
          boxShadow: "none",
          borderBottom: "1px solid #333",
        },
      },
    },
  },
});

const CustomContainer = styled(Box)({
  padding: "40px",
  backgroundColor: "#1c1c1c", // Consistent with the app's overall theme
  borderRadius: "16px",
  boxShadow: "0 10px 30px rgba(0, 0, 0, 0.5)",
  maxWidth: "900px",
  width: "100%",
  margin: "auto",
});

const App: React.FC = () => {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <AppBar position="sticky">
        <Toolbar>
          <IconButton edge="start" color="inherit" aria-label="menu">
            <MenuIcon />
          </IconButton>
          <Typography variant="h6" style={{ flexGrow: 1 }}>
            TechBlueprint
          </Typography>
        </Toolbar>
      </AppBar>
      <Box
        sx={{
          backgroundColor: "#0d0d0d", // Updated to a deeper black
          minHeight: "100vh",
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          padding: "40px 0",
        }}
      >
        <motion.div
          initial={{ opacity: 0, scale: 0.95 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 0.8 }}
        >
          <CustomContainer>
            <Typography variant="h1" align="center">
              Welcome to TechBlueprint
            </Typography>
            <Typography variant="h6" align="center" paragraph>
              Upload your electronic component images to get project suggestions
              and step-by-step guides.
            </Typography>
            <UploadPage />
          </CustomContainer>
        </motion.div>
      </Box>
    </ThemeProvider>
  );
};

export default App;
