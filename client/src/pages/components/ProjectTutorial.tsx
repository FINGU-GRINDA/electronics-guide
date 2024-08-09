import React, { useEffect, useRef, useState } from 'react';
import {
	Card,
	CardContent,
	Typography,
	Box,
	IconButton,
	Button,
} from '@mui/material';
import { ZoomIn, ZoomOut, Refresh } from '@mui/icons-material';
import parse, { domToReact, HTMLReactParserOptions } from 'html-react-parser';
import jsPDF from 'jspdf';
import { TransformWrapper, TransformComponent } from 'react-zoom-pan-pinch';
import ReactMarkdown from 'react-markdown';

interface ProjectTutorialProps {
	tutorial: string;
}

const options: HTMLReactParserOptions = {
	replace: (domNode, index) => {
		if (!domNode) {
			return;
		}
		if (domNode instanceof Text && domNode.nodeValue) {
			return <ReactMarkdown>{domNode.nodeValue}</ReactMarkdown>;
		}

		return domToReact([domNode]);
	},
};

const ProjectTutorial: React.FC<ProjectTutorialProps> = ({ tutorial }) => {
	const tutorialRef = useRef<HTMLDivElement>(null);
	const [tutorialContent, setTutorialContent] = useState('');

	useEffect(() => {
		setTutorialContent(tutorial);
	}, [tutorial]);

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
						position: 'relative',
						maxHeight: '700px',
						overflow: 'hidden',
						border: '1px solid #ccc',
						borderRadius: '8px',
						padding: '16px',
						backgroundColor: '#f9f9f9',
						boxShadow: '0 0 10px rgba(0, 0, 0, 0.1)',
						fontFamily: 'monospace',
					}}
				>
					<TransformWrapper wheel={{ disabled: true }}>
						{({ zoomIn, zoomOut, resetTransform }) => (
							<>
								<Box
									sx={{
										position: 'absolute',
										top: '8px',
										right: '8px',
										display: 'flex',
										flexDirection: 'column',
										gap: '8px',
									}}
								>
									<IconButton
										onClick={() => zoomIn()}
										color='primary'
										aria-label='zoom in'
									>
										<ZoomIn />
									</IconButton>
									<IconButton
										onClick={() => zoomOut()}
										color='primary'
										aria-label='zoom out'
									>
										<ZoomOut />
									</IconButton>
									<IconButton
										onClick={() => resetTransform()}
										color='primary'
										aria-label='reset'
									>
										<Refresh />
									</IconButton>
								</Box>
								<TransformComponent>
									<Box
										ref={tutorialRef}
										sx={{
											maxHeight: '700px',
											overflowY: 'auto',
											border: '1px solid #ccc',
											borderRadius: '8px',
											padding: '16px',
											backgroundColor: '#f9f9f9',
											boxShadow: '0 0 10px rgba(0, 0, 0, 0.1)',
											fontFamily: 'monospace',
										}}
									>
										{parse(tutorialContent, options)}
									</Box>
								</TransformComponent>
							</>
						)}
					</TransformWrapper>
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
