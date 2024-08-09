import React, { useEffect, useState } from 'react';
import {
	Card,
	CardContent,
	Typography,
	Box,
	Button,
	IconButton,
} from '@mui/material';
import parse, {
	domToReact,
	HTMLReactParserOptions,
	Element,
} from 'html-react-parser';
import jsPDF from 'jspdf';
import ContentCopyIcon from '@mui/icons-material/ContentCopy';
import ReactMarkdown from 'react-markdown';
import rehypeRaw from 'rehype-raw';
import remarkGfm from 'remark-gfm';
import { MuiMarkdown, getOverrides } from 'mui-markdown';
import { Highlight, themes } from 'prism-react-renderer';
import { HighlightRounded } from '@mui/icons-material';

interface ProjectTutorialProps {
	tutorial: string;
}

const ProjectTutorial: React.FC<ProjectTutorialProps> = ({ tutorial }) => {
	const [tutorialContent, setTutorialContent] = useState('');

	useEffect(() => {
		setTutorialContent(tutorial);
		console.log(tutorial);
	}, [tutorial]);
	const formatTutorial = (content: string): string => {
		const lines = content.split('\n');
		let formattedContent = '';
		let inCodeBlock = false;
		let codeBlockContent = '';
		let codeLanguage = '';

		const processCodeBlock = () => {
			if (codeBlockContent.trim()) {
				formattedContent += `<pre class="code-block" data-language="${codeLanguage}"><code>${codeBlockContent.trim()}</code></pre>`;
			}
			inCodeBlock = false;
			codeBlockContent = '';
			codeLanguage = '';
		};

		for (let i = 0; i < lines.length; i++) {
			const line = lines[i].trim();

			if (line.startsWith('```') || line.startsWith("'''")) {
				if (inCodeBlock) {
					processCodeBlock();
				} else {
					inCodeBlock = true;
					codeLanguage = line.slice(3).trim();
				}
			} else if (inCodeBlock) {
				codeBlockContent += line + '\n';
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
					.replace(/^-\s(.+)$/, '<li>$1</li>')
					.replace(/`([^`\n]+)`/g, '<code class="inline-code">$1</code>');

				formattedContent += processedLine + '\n';
			}

			// Check for potential unlabeled code blocks
			if (!inCodeBlock && i < lines.length - 3) {
				const nextLines = lines.slice(i + 1, i + 4).join('\n');
				if (
					nextLines.match(/^\s*(var|let|const|function|if|for|while|class)\s/m)
				) {
					inCodeBlock = true;
					codeLanguage = 'javascript'; // Assume JavaScript as default
					i++; // Skip the next line as it's the start of the code block
				}
			}
		}

		// Process any remaining code block
		if (inCodeBlock) {
			processCodeBlock();
		}

		return formattedContent.replace(/\n\n+/g, '</p><p>').replace(/\n/g, '<br>');
	};
	const handleDownloadPDF = () => {
		const doc = new jsPDF();
		const pageWidth = doc.internal.pageSize.getWidth();
		const pageHeight = doc.internal.pageSize.getHeight();
		const margin = 10;
		const maxWidth = pageWidth - 2 * margin;

		let y = margin;
		const lines = tutorial.split('\n');

		doc.setFont('helvetica');
		doc.setFontSize(12);

		lines.forEach((line) => {
			if (y > pageHeight - margin) {
				doc.addPage();
				y = margin;
			}

			const words = line.split(' ');
			let currentLine = '';

			words.forEach((word) => {
				const testLine = currentLine + (currentLine ? ' ' : '') + word;
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

		doc.save('tutorial.pdf');
	};

	const copyToClipboard = (text: string) => {
		navigator.clipboard.writeText(text).then(() => {
			alert('Code copied to clipboard!');
		});
	};

	const parseOptions: HTMLReactParserOptions = {
		replace: (domNode) => {
			if (!domNode) {
				return;
			}
			if (domNode instanceof Text) {
				return (
					<ReactMarkdown
						rehypePlugins={[rehypeRaw]}
						remarkPlugins={[remarkGfm]}
					>
						{domNode.nodeValue ? domNode.nodeValue : ''}
					</ReactMarkdown>
				);
			}
			return domToReact([domNode]);
		},
	};

	return (
		<Card variant='outlined'>
			<CardContent>
				<Typography
					variant='h6'
					gutterBottom
				>
					Project Tutorial
				</Typography>
				<Box
					sx={{
						maxHeight: '700px',
						overflowY: 'auto',
						border: '1px solid #ccc',
						borderRadius: '8px',
						padding: '16px',
						backgroundColor: '#f9f9f9',
						boxShadow: '0 0 10px rgba(0, 0, 0, 0.1)',
            position: 'relative',
            display: 'flex',
            justifyContent: 'center',
					}}
				>
					<ReactMarkdown
						remarkPlugins={[remarkGfm]}
						className='prose w-full'
						// rehypePlugins={[rehypeRaw]}
					>
						{tutorialContent}
					</ReactMarkdown>
						{/* <MuiMarkdown
							Highlight={Highlight}
							themes={themes}
							prismTheme={themes.github}
						>
							{tutorialContent}
						</MuiMarkdown> */}
				</Box>
				<Button
					variant='contained'
					color='primary'
					onClick={handleDownloadPDF}
					sx={{ marginTop: '16px' }}
				>
					Download PDF
				</Button>
			</CardContent>
		</Card>
	);
};

export default ProjectTutorial;
