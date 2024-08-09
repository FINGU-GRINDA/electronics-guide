import axios from "axios";

export const analyzeImage = async (file: File) => {
  const formData = new FormData();
  formData.append("file", file);

  const response = await axios.post(
    "http://localhost:8000/api/v1/analyze_image/",
    formData,
    {
      headers: { "Content-Type": "multipart/form-data" },
    }
  );

  return response.data;
};

export const getProjectDetails = async (
  file: File,
  project: string,
  onData: (data: any) => void,
  signal: AbortSignal
) => {
  const formData = new FormData();
  formData.append("file", file);
  formData.append("project", project);

  const response = await fetch(
    "http://localhost:8000/api/v1/project_details/",
    {
      method: "POST",
      body: formData,
      signal,
    }
  );

  if (!response.body) {
    throw new Error("No response body");
  }

  const reader = response.body.getReader();
  const decoder = new TextDecoder("utf-8");

  while (true) {
    const { done, value } = await reader.read();
    if (done) break;
    const chunk = decoder.decode(value, { stream: true });

    // Split the chunk by newline to handle multiple JSON objects
    const jsonStrings = chunk.split("\n").filter((str) => str.trim() !== "");

    for (const jsonString of jsonStrings) {
      try {
        const data = JSON.parse(jsonString);
        console.log("Received data chunk:", data); // Log the received data

        onData(data);
      } catch (error) {
        console.error("Error parsing JSON:", error);
        console.error("Problematic JSON string:", jsonString);
      }
    }
  }
};

export const downloadTutorialPdf = async () => {
  const response = await axios.get(
    "http://localhost:8000/api/v1/download_tutorial/",
    {
      responseType: "blob",
    }
  );
  return response.data;
};
