import React from "react";
import FileUpload from "./components/FileUpload";
import "./App.css";

const App: React.FC = () => {
  return (
    <div className="App min-h-screen bg-gray-200 py-10">
      <header className="max-w-3xl mx-auto">
        <h1 className="text-3xl font-bold mb-4 text-center text-gray-800">
          Electronics Project Generator
        </h1>
        <FileUpload />
      </header>
    </div>
  );
};

export default App;
