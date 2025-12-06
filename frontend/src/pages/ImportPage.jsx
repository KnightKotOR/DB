import { useEffect, useState } from "react";
import api from "../api";
import ImportForm from "../components/ImportForm";

const ImportPage = () => {
  const [databases, setDatabases] = useState([]);

  const fetchDatabases = () => {
    api.get("/databases")
      .then((res) => setDatabases(res.data))
      .catch((err) => console.error("Error fetching databases:", err));
  };

  useEffect(() => {
    fetchDatabases();
  }, []);

  return (
    <div>
      <h2 className="text-2xl font-semibold mb-4">Import databases</h2>

      <section className="mb-8">
        <h3 className="text-lg font-medium mb-2">Databases in metadata catalog:</h3>
        {databases.length ? (
          <ul className="list-disc pl-6">
            {databases.map((db) => (
              <li key={db.db_id}>{db.db_name}</li>
            ))}
          </ul>
        ) : (
          <p>No data.</p>
        )}
      </section>

      <ImportForm onImportSuccess={fetchDatabases} />
    </div>
  );
};

export default ImportPage;
