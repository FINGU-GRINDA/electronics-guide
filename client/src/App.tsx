import React from "react";
import FileUpload from "./components/FileUpload";
import { Container, CssBaseline, Typography, Box } from "@mui/material";
import { ThemeProvider, createTheme } from "@mui/material/styles";
import UploadPage from "./pages/UploadPage";

const theme = createTheme({
  palette: {
    background: {
      default: "#f5f5f5",
    },
  },
  typography: {
    h1: {
      fontSize: "2rem",
      fontWeight: 700,
      textAlign: "center",
      marginBottom: "1.5rem",
      color: "#333",
    },
  },
});

const App: React.FC = () => {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Container maxWidth="md">
        <Box py={10}>
          <Typography variant="h1">Electronics Project Generator</Typography>
          <UploadPage />
        </Box>
      </Container>
    </ThemeProvider>
  );
};

export default App;
