import React, { useEffect, useState } from "react";
import {
  Card,
  CardContent,
  Typography,
  Box,
  Button,
  IconButton,
} from "@mui/material";
import parse, {
  domToReact,
  HTMLReactParserOptions,
  Element,
} from "html-react-parser";
import jsPDF from "jspdf";
import ContentCopyIcon from "@mui/icons-material/ContentCopy";

interface ProjectTutorialProps {
  tutorial: string;
}

const ProjectTutorial: React.FC<ProjectTutorialProps> = ({ tutorial }) => {
  const [tutorialContent, setTutorialContent] = useState("");

  useEffect(() => {
    setTutorialContent(formatTutorial(tutorial));
  }, [tutorial]);
  const formatTutorial = (content: string): string => {
    const lines = content.split("\n");
    let formattedContent = "";
    let inCodeBlock = false;
    let codeBlockContent = "";
    let codeLanguage = "";

    const processCodeBlock = () => {
      if (codeBlockContent.trim()) {
        formattedContent += `<pre class="code-block" data-language="${codeLanguage}"><code>${codeBlockContent.trim()}</code></pre>`;
      }
      inCodeBlock = false;
      codeBlockContent = "";
      codeLanguage = "";
    };

    for (let i = 0; i < lines.length; i++) {
      const line = lines[i].trim();

      if (line.startsWith("```") || line.startsWith("'''")) {
        if (inCodeBlock) {
          processCodeBlock();
        } else {
          inCodeBlock = true;
          codeLanguage = line.slice(3).trim();
        }
      } else if (inCodeBlock) {
        codeBlockContent += line + "\n";
      } else {
        // Improved normal text processing
        const processedLine = line
          .replace(
            /^(#{1,6})\s(.+)$/,
            (_, hashes, text) =>
              `<h${hashes.length} class="title">${text}</h${hashes.length}>`
          )
          .replace(/^([A-Z][\w\s]+:)$/, '<h2 class="subtitle">$1</h2>')
          .replace(
            /^(\d+\.?\s?)(.+)$/,
            '<div class="list-item"><strong>$1</strong> $2</div>'
          )
          .replace(/^-\s(.+)$/, "<li>$1</li>")
          .replace(/`([^`\n]+)`/g, '<code class="inline-code">$1</code>');

        formattedContent += processedLine + "\n";
      }

      // Check for potential unlabeled code blocks
      if (!inCodeBlock && i < lines.length - 3) {
        const nextLines = lines.slice(i + 1, i + 4).join("\n");
        if (
          nextLines.match(/^\s*(var|let|const|function|if|for|while|class)\s/m)
        ) {
          inCodeBlock = true;
          codeLanguage = "javascript"; // Assume JavaScript as default
          i++; // Skip the next line as it's the start of the code block
        }
      }
    }

    // Process any remaining code block
    if (inCodeBlock) {
      processCodeBlock();
    }

    return formattedContent.replace(/\n\n+/g, "</p><p>").replace(/\n/g, "<br>");
  };
  const handleDownloadPDF = () => {
    const doc = new jsPDF();
    const pageWidth = doc.internal.pageSize.getWidth();
    const pageHeight = doc.internal.pageSize.getHeight();
    const margin = 10;
    const maxWidth = pageWidth - 2 * margin;

    let y = margin;
    const lines = tutorial.split("\n");

    doc.setFont("helvetica");
    doc.setFontSize(12);

    lines.forEach((line) => {
      if (y > pageHeight - margin) {
        doc.addPage();
        y = margin;
      }

      const words = line.split(" ");
      let currentLine = "";

      words.forEach((word) => {
        const testLine = currentLine + (currentLine ? " " : "") + word;
        const testWidth = doc.getTextWidth(testLine);

        if (testWidth > maxWidth) {
          doc.text(currentLine, margin, y);
          y += 7;
          currentLine = word;

          if (y > pageHeight - margin) {
            doc.addPage();
            y = margin;
          }
        } else {
          currentLine = testLine;
        }
      });

      if (currentLine) {
        doc.text(currentLine, margin, y);
        y += 7;
      }

      y += 3; // Add extra space between paragraphs
    });

    doc.save("tutorial.pdf");
  };

  const copyToClipboard = (text: string) => {
    navigator.clipboard.writeText(text).then(() => {
      alert("Code copied to clipboard!");
    });
  };

  const parseOptions: HTMLReactParserOptions = {
    replace: (domNode) => {
      if (domNode instanceof Element) {
        const { attribs, children, name } = domNode;

        if (
          name === "h1" ||
          name === "h2" ||
          name === "h3" ||
          name === "h4" ||
          name === "h5" ||
          name === "h6"
        ) {
          return (
            <Typography
              variant={`h${name.charAt(1)}` as any}
              component={name}
              className={attribs.class}
            >
              {domToReact(children as any)}
            </Typography>
          );
        }

        if (name === "p") {
          return (
            <Typography variant="body1" component="p" className="paragraph">
              {domToReact(children as any)}
            </Typography>
          );
        }

        if (name === "pre" && attribs.class === "code-block") {
          const codeElement = children.find(
            (child) => child instanceof Element && child.name === "code"
          ) as Element;
          const code =
            codeElement?.children[0] instanceof Text
              ? codeElement.children[0].data
              : "";
          const language = attribs["data-language"];
          return (
            <Box className="code-block-container" sx={{ position: "relative" }}>
              <IconButton
                onClick={() => copyToClipboard(code)}
                sx={{ position: "absolute", top: 5, right: 5 }}
              >
                <ContentCopyIcon />
              </IconButton>
              <pre className={`code-block language-${language}`}>
                <code>{code}</code>
              </pre>
            </Box>
          );
        }
        if (name === "code" && attribs.class === "inline-code") {
          return (
            <code className="inline-code">{domToReact(children as any)}</code>
          );
        }

        if (name === "li") {
          return <li className="list-item">{domToReact(children as any)}</li>;
        }
      }
    },
  };

  return (
    <Card variant="outlined">
      <CardContent>
        <Typography variant="h6" gutterBottom>
          Project Tutorial
        </Typography>
        <Box
          sx={{
            maxHeight: "700px",
            overflowY: "auto",
            border: "1px solid #ccc",
            borderRadius: "8px",
            padding: "16px",
            backgroundColor: "#f9f9f9",
            boxShadow: "0 0 10px rgba(0, 0, 0, 0.1)",
          }}
        >
          {parse(tutorialContent, parseOptions)}
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
