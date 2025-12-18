import { useState } from "react";
import { useDatabases } from "../contexts/DatabaseContext";
import api from "../api";

export default function QueryPage() {
  const [database, setDatabase] = useState("");
  const [table, setTable] = useState("");
  const [column, setColumn] = useState("");
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const handleExecute = async (e) => {
    e.preventDefault();
    setError(null);
    setResult(null);
    try {
      const response = await api.post("/query", {
        database: database,
        table: table,
        column: column,
      });
      setResult(response.data);
    } catch (err) {
      setError(err.response?.data?.detail || err.response?.data?.message || "Error occurred");
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50 p-6">
      <div className="w-full max-w-2xl bg-white p-8 rounded-2xl shadow space-y-6">
        <h1 className="text-2xl font-semibold">Query Executor</h1>

        <form onSubmit={handleExecute} className="space-y-6">
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

          <div className="space-y-3 p-4 border rounded-lg bg-gray-100">
            <div className="flex items-center space-x-2">
              <span className="font-mono">SELECT</span>
              <input
                type="text"
                placeholder="column"
                value={column}
                onChange={(e) => setColumn(e.target.value)}
                required
                className="flex-1 border rounded p-2"
              />
            </div>

            <div className="flex items-center space-x-2">
              <span className="font-mono">FROM</span>
              <input
                type="text"
                placeholder="table"
                value={table}
                onChange={(e) => setTable(e.target.value)}
                required
                className="flex-1 border rounded p-2"
              />
              <span className="font-mono">;</span>
            </div>
          </div>

          <button
            type="submit"
            className="w-full bg-blue-600 text-white py-2 rounded hover:bg-blue-700"
          >
            Execute
          </button>
        </form>

        {error && (
          <div className="p-3 bg-red-100 border border-red-300 rounded text-red-700 text-sm">
            {error}
          </div>
        )}

        {result && (
          <div className="overflow-x-auto mt-4">
            <table className="min-w-full border border-gray-300">
              <thead>
                <tr className="bg-gray-200">
                  <th className="border p-2 text-left">{result.column}</th>
                </tr>
              </thead>
              <tbody>
                {result.info.map((item, index) => (
                  <tr key={index}>
                    <td className="border p-2">{item}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
}