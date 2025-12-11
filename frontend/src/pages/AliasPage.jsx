import { useState } from "react";
import api from "../api";

export default function AliasPage() {
  const [database, setDatabase] = useState("");
  const [table, setTable] = useState("");
  const [alias, setAlias] = useState("");
  const [message, setMessage] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await api.post("/alias/create", {
        database: database,
        table: table || "",
        alias: alias,
      });
      setMessage(response.data.message || "");
    } catch (error) {
      setMessage(error.response?.data?.detail || error.response?.data?.message || "Error occurred");
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50 p-6">
      <div className="w-full max-w-lg bg-white p-8 rounded-2xl shadow">
        <h2 className="text-2xl font-semibold mb-4">Assign alias</h2>
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block mb-1 font-medium">Database Name</label>
            <input
              type="text"
              value={database}
              onChange={(e) => setDatabase(e.target.value)}
              required
              className="w-full border rounded p-2"
            />
          </div>

          <div>
            <label className="block mb-1 font-medium">Table Name (optional)</label>
            <input
              type="text"
              value={table}
              onChange={(e) => setTable(e.target.value)}
              className="w-full border rounded p-2"
            />
          </div>

          <div>
            <label className="block mb-1 font-medium">Alias</label>
            <input
              type="text"
              value={alias}
              onChange={(e) => setAlias(e.target.value)}
              required
              className="w-full border rounded p-2"
            />
          </div>

          <button
            type="submit"
            className="w-full bg-blue-600 text-white py-2 rounded hover:bg-blue-700"
          >
            Submit
          </button>
        </form>

        {message && (
          <div className="mt-4 p-3 bg-gray-100 border rounded text-sm">
            {message}
          </div>
        )}
      </div>
    </div>
  );
}
