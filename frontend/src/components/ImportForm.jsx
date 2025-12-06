import { useState } from "react";
import api from "../api";

const ImportForm = ({ onImportSuccess }) => {
  const [input, setInput] = useState("");
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);

  const handleImport = async () => {
    const dbs = input
      .split(/\s+/)
      .map((s) => s.trim())
      .filter((s) => s.length > 0);

    if (!dbs.length) {
      alert("Enter at least one database name");
      return;
    }

    setLoading(true);
    setMessages([]);

    try {
      const res = await api.post("/metadata/import", { databases: dbs });
      setMessages(res.data);
      if (onImportSuccess) onImportSuccess();
    } catch (err) {
      console.error(err);
      alert("Error importing data.");
    } finally {
      setLoading(false);
    }
  };

  return (
  <div className="border-t pt-4">
    <h3 className="text-lg font-medium mb-2">Import new databases</h3>
    <div className="flex flex-col">
      <textarea
        style={{ width: "400px" }}
        className="border p-2 rounded mb-3"
        rows="1"
        placeholder="Enter names, example: products employees"
        value={input}
        onChange={(e) => setInput(e.target.value)}
      />
      <p></p>
      <button
        onClick={handleImport}
        disabled={loading}
        className="block bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded disabled:bg-gray-400 mt-2"
      >
        {loading ? "Importing..." : "Import"}
      </button>
    </div>

    {messages.length > 0 && (
      <div className="mt-4">
        <h4 className="font-medium mb-2">Result:</h4>
        <ul className="space-y-1">
          {messages.map((msg) => (
            <p key={msg.message} className={`message ${msg.status}`}>{msg.message}</p>
          ))}
        </ul>
      </div>
    )}
  </div>
);

};

export default ImportForm;
