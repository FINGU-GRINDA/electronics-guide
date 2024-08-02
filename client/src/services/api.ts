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
  onData: (data: string, type: string) => void
) => {
  const formData = new FormData();
  formData.append("file", file);
  formData.append("project", project);

  const response = await fetch(
    "http://localhost:8000/api/v1/project_details/",
    {
      method: "POST",
      body: formData,
    }
  );

  if (!response.body) {
    throw new Error("No response body");
  }

  const reader = response.body.getReader();
  const decoder = new TextDecoder("utf-8");
  let result = "";
  let isJSON = true;

  while (true) {
    const { done, value } = await reader.read();
    if (done) break;
    const chunk = decoder.decode(value, { stream: true });
    result += chunk;

    // Check if the result is valid JSON
    if (isJSON) {
      try {
        JSON.parse(result);
      } catch (e) {
        isJSON = false;
      }
    }

    onData(result, isJSON ? "json" : "html");
  }

  return result;
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
