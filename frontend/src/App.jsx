import React, { useState } from "react";
import axios from "axios";

export default function App() {
  const [file, setFile] = useState(null);
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [progress, setProgress] = useState(0);
  const [error, setError] = useState("");
  const [completed, setCompleted] = useState(false);

  const handleUpload = async () => {
    if (!file) {
      alert("Please upload a PDF first");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    setLoading(true);
    setProgress(0);
    setError("");
    setCompleted(false);
    setData(null);

    try {
      const res = await axios.post("http://127.0.0.1:8000/extract", formData, {
        headers: { "Content-Type": "multipart/form-data" },
        onUploadProgress: (e) => {
          if (e.total) {
            setProgress(Math.round((e.loaded * 100) / e.total));
          }
        },
      });

      setData(res.data);
      setCompleted(true);
    } catch (err) {
      console.error(err);
      setError("Extraction failed. Check backend logs.");
    } finally {
      setLoading(false);
    }
  };

  const handleDownload = () => {
    if (!data) return;
    const blob = new Blob([JSON.stringify(data, null, 2)], {
      type: "application/json",
    });
    const link = document.createElement("a");
    link.href = URL.createObjectURL(blob);
    link.download = `${data.file.split(".")[0]}_results.json`;
    link.click();
  };

  return (
    <div className="min-h-screen bg-gray-900 text-white flex flex-col items-center p-8">
      <h1 className="text-3xl font-bold mb-4 text-center">
        🧠 Tile Catalog Extractor
      </h1>

      <input
        type="file"
        accept="application/pdf"
        onChange={(e) => setFile(e.target.files[0])}
        className="mb-4 text-black p-2 rounded"
      />

      <button
        onClick={handleUpload}
        className="bg-blue-600 hover:bg-blue-700 px-4 py-2 rounded-lg disabled:opacity-50"
        disabled={loading}
      >
        {loading ? "Processing..." : "Upload & Extract"}
      </button>

      {loading && (
        <div className="mt-4 text-yellow-400 w-1/2">
          <p>⏳ Uploading PDF...</p>
          <div className="w-full bg-gray-700 rounded-full h-3 mt-2">
            <div
              className="bg-blue-500 h-3 rounded-full transition-all duration-300"
              style={{ width: `${progress}%` }}
            ></div>
          </div>
        </div>
      )}

      {error && <div className="text-red-400 mt-4">{error}</div>}

      {completed && data && (
        <div className="mt-6 text-center">
          <p className="text-green-400">
            ✅ Extraction complete for <strong>{data.file}</strong>
          </p>
          <div className="flex gap-4 mt-4 justify-center">
            <button
              onClick={handleDownload}
              className="bg-green-600 hover:bg-green-700 px-4 py-2 rounded"
            >
              Download JSON
            </button>
            <a
              href={`http://127.0.0.1:8000${data.download_url}`}
              download
              className="bg-indigo-600 hover:bg-indigo-700 px-4 py-2 rounded"
            >
              Download from Server
            </a>
          </div>
        </div>
      )}

      {data && data.products && (
        <div className="mt-8 w-full max-w-4xl">
          <h2 className="text-xl font-semibold mb-4 text-center">
            Extracted Products
          </h2>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
            {data.products.map((p, i) => (
              <div
                key={i}
                className="bg-gray-800 p-4 rounded-xl shadow-lg border border-gray-700"
              >
                <p className="font-bold text-lg">{p.name}</p>
                <p className="text-gray-300 text-sm">{p.dimensions}</p>
                {p.confidence_avg && (
                  <p className="text-yellow-400 text-sm">
                    Confidence: {Math.round(p.confidence_avg * 100)}%
                  </p>
                )}
                <div className="flex gap-3 mt-3 flex-wrap justify-center">
                  {p.images?.map((img, j) => (
                    <div key={j} className="flex flex-col items-center">
                      <img
                        src={`http://127.0.0.1:8000/${img}`}
                        alt="tile"
                        className="w-24 h-24 object-cover rounded border border-gray-600"
                      />
                      <div className="flex gap-2 mt-1">
                        <button
                          onClick={() =>
                            axios.post("http://127.0.0.1:8000/feedback", {
                              image: img,
                              correct: true,
                            })
                          }
                          className="bg-green-600 hover:bg-green-700 px-2 py-1 text-xs rounded"
                        >
                          ✅
                        </button>
                        <button
                          onClick={() =>
                            axios.post("http://127.0.0.1:8000/feedback", {
                              image: img,
                              correct: false,
                            })
                          }
                          className="bg-red-600 hover:bg-red-700 px-2 py-1 text-xs rounded"
                        >
                          ❌
                        </button>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
