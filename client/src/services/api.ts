import axios from "axios";

const api = axios.create({
  baseURL: "http://localhost:8000/api/v1",
});

export const analyzeImage = async (file: File) => {
  const formData = new FormData();
  formData.append("file", file);

  const response = await api.post("/analyze_image/", formData, {
    headers: {
      "Content-Type": "multipart/form-data",
    },
  });

  return response.data;
};

export const getProjectDetails = async (file: File, project: string) => {
  const formData = new FormData();
  formData.append("file", file);
  formData.append("project", project);

  const response = await api.post("/project_details/", formData, {
    headers: {
      "Content-Type": "multipart/form-data",
    },
  });

  return response.data;
};

export const runWorkflow = async (file: File) => {
  const formData = new FormData();
  formData.append("file", file);

  const response = await api.post("/workflow/", formData, {
    headers: {
      "Content-Type": "multipart/form-data",
    },
  });

  return response.data;
};
