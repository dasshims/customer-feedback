import { ChangeEvent, FormEvent, useState } from "react";

interface FileUploadProps {
  onSubmit: (file: File) => Promise<void>;
  isLoading: boolean;
}

function FileUpload({ onSubmit, isLoading }: FileUploadProps) {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [validationMessage, setValidationMessage] = useState<string | null>(
    null
  );

  const handleFileChange = (event: ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (!file) {
      setSelectedFile(null);
      setValidationMessage(null);
      return;
    }

    if (!file.name.toLowerCase().endsWith(".csv")) {
      setSelectedFile(null);
      setValidationMessage("Please select a CSV file.");
      return;
    }

    setSelectedFile(file);
    setValidationMessage(null);
  };

  const handleSubmit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    if (!selectedFile) {
      setValidationMessage("Choose a CSV file before analyzing.");
      return;
    }

    await onSubmit(selectedFile);
  };

  return (
    <form onSubmit={handleSubmit} aria-label="Upload customer feedback CSV">
      <label htmlFor="feedback-file" style={{ display: "block" }}>
        Select feedback CSV file
      </label>
      <input
        id="feedback-file"
        className="file-input"
        type="file"
        accept=".csv,text/csv"
        onChange={handleFileChange}
        disabled={isLoading}
      />

      {validationMessage && (
        <p role="status" style={{ color: "#b91c1c", marginBottom: "1rem" }}>
          {validationMessage}
        </p>
      )}

      <button
        className="button"
        type="submit"
        disabled={!selectedFile || isLoading}
      >
        {isLoading ? "Uploading..." : "Analyze Feedback"}
      </button>
    </form>
  );
}

export default FileUpload;
