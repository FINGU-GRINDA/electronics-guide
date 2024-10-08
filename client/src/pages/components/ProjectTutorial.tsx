import React, { useEffect, useState, useRef } from "react";
import { Card, CardContent, Typography, Box, Button } from "@mui/material";
import jsPDF from "jspdf";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import html2canvas from "html2canvas";

interface ProjectTutorialProps {
  tutorial: string;
}

const ProjectTutorial: React.FC<ProjectTutorialProps> = ({ tutorial }) => {
  const [tutorialContent, setTutorialContent] = useState("");
  const tutorialRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    setTutorialContent(tutorial);
  }, [tutorial]);

  const handleDownloadPDF = async () => {
    if (tutorialRef.current) {
      // Temporarily remove the overflow restriction and expand the element to fit all content
      const originalHeight = tutorialRef.current.style.height;
      tutorialRef.current.style.height = "auto";
      tutorialRef.current.style.maxHeight = "none";
      tutorialRef.current.style.overflowY = "visible";

      // Use html2canvas to capture the entire area
      const canvas = await html2canvas(tutorialRef.current, {
        scale: 1.5, // Reduced scale for smaller file size
        useCORS: true,
      });

      // Restore the original styles
      tutorialRef.current.style.height = originalHeight;
      tutorialRef.current.style.maxHeight = "700px";
      tutorialRef.current.style.overflowY = "auto";

      // Convert to JPEG format for smaller file size
      const imgData = canvas.toDataURL("image/jpeg", 0.75); // 0.75 is the quality level (0 to 1)

      const pdf = new jsPDF("p", "mm", "a4");
      const imgWidth = 210; // A4 width in mm
      const pageHeight = 297; // A4 height in mm
      const imgHeight = (canvas.height * imgWidth) / canvas.width;
      let heightLeft = imgHeight;

      let position = 0;

      pdf.addImage(
        imgData,
        "JPEG",
        0,
        position,
        imgWidth,
        imgHeight,
        undefined,
        "FAST"
      ); // 'FAST' for compression
      heightLeft -= pageHeight;

      while (heightLeft > 0) {
        position = heightLeft - imgHeight;
        pdf.addPage();
        pdf.addImage(
          imgData,
          "JPEG",
          0,
          position,
          imgWidth,
          imgHeight,
          undefined,
          "FAST"
        );
        heightLeft -= pageHeight;
      }

      pdf.save("tutorial.pdf");
    }
  };

  return (
    <Card variant="outlined">
      <CardContent>
        <Typography variant="h6" gutterBottom>
          Project Tutorial
        </Typography>
        <Box
          ref={tutorialRef}
          sx={{
            maxHeight: "700px",
            overflowY: "auto",
            border: "1px solid #ccc",
            borderRadius: "8px",
            padding: "16px",
            backgroundColor: "#f9f9f9",
            boxShadow: "0 0 10px rgba(0, 0, 0, 0.1)",
            position: "relative",
            display: "flex",
            justifyContent: "center",
          }}
        >
          <ReactMarkdown remarkPlugins={[remarkGfm]} className="prose w-full">
            {tutorialContent}
          </ReactMarkdown>
        </Box>
        <Button
          variant="contained"
          color="primary"
          onClick={handleDownloadPDF}
          sx={{ marginTop: "16px" }}
        >
          Download PDF
        </Button>
      </CardContent>
    </Card>
  );
};

export default ProjectTutorial;
