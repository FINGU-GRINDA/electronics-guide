import React, { useState } from "react";
import { analyzeImage, getProjectDetails } from "../services/api";
import ReactMarkdown from "react-markdown";
import { ClipLoader } from "react-spinners";

const FileUpload: React.FC = () => {
  const [file, setFile] = useState<File | null>(null);
  const [description, setDescription] = useState<string>("");
  const [projectIdeas, setProjectIdeas] = useState<string[]>([]);
  const [selectedProject, setSelectedProject] = useState<string>("");
  const [tutorial, setTutorial] = useState<string>("");
  const [loading, setLoading] = useState<boolean>(false);

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    if (event.target.files) {
      setFile(event.target.files[0]);
    }
  };

  const handleAnalyzeImage = async (event: React.FormEvent) => {
    event.preventDefault();
    if (file) {
      setLoading(true);
      const data = await analyzeImage(file);
      setDescription(data.project_ideas[0]); // Assuming the first item is the description
      const cleanedData = data.project_ideas
        .slice(1)
        .filter((idea: string) => idea.trim() !== "");
      setProjectIdeas(cleanedData);
      setLoading(false);
    }
  };

  const handleGetProjectDetails = async () => {
    if (file && selectedProject) {
      setLoading(true);
      const data = await getProjectDetails(file, selectedProject);
      setTutorial(data.tutorial);
      setLoading(false);
    }
  };

  return (
    <div className="p-4 max-w-3xl mx-auto bg-white rounded-lg shadow-md">
      <form onSubmit={handleAnalyzeImage} className="mb-4">
        <div className="mb-4">
          <input
            type="file"
            onChange={handleFileChange}
            className="p-2 border border-gray-300 rounded w-full"
          />
        </div>
        <button
          type="submit"
          className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
        >
          Upload
        </button>
      </form>
      {loading && (
        <div className="mt-4 flex justify-center">
          <ClipLoader color="#4A90E2" />
        </div>
      )}
      <div className="mt-4">
        {description && (
          <div className="p-4 mb-4 border border-gray-300 rounded bg-gray-50">
            <ReactMarkdown>{description}</ReactMarkdown>
          </div>
        )}
        {projectIdeas.length > 0 && (
          <div>
            <h2 className="text-2xl font-bold mb-4 text-gray-800">
              Project Ideas
            </h2>
            <div className="space-y-4">
              {projectIdeas.map((idea, index) => (
                <div
                  key={index}
                  className="cursor-pointer p-4 border border-gray-300 rounded hover:bg-gray-100"
                  onClick={() => setSelectedProject(idea)}
                >
                  <ReactMarkdown>{idea}</ReactMarkdown>
                </div>
              ))}
            </div>
            {selectedProject && (
              <button
                onClick={handleGetProjectDetails}
                className="mt-4 px-4 py-2 bg-green-600 text-white rounded hover:bg-green-700"
              >
                Get Project Details
              </button>
            )}
          </div>
        )}
      </div>
      <div className="mt-4">
        {tutorial && (
          <div className="p-4 border rounded bg-gray-50 shadow-lg">
            <h2 className="text-2xl font-bold mb-4">Project Tutorial</h2>
            <ReactMarkdown className="prose">{tutorial}</ReactMarkdown>
          </div>
        )}
      </div>
    </div>
  );
};

export default FileUpload;
