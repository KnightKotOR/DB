import { useOutletContext } from "react-router-dom";
import ImportForm from "../components/ImportForm";

const ImportPage = () => {
  // Получаем функцию обновления из Layout
  const { refreshDatabases } = useOutletContext();

  return (
    <div className="max-w-2xl mx-auto">
      <h2 className="text-3xl font-bold mb-6 text-white">Import Database</h2>
      <p className="text-gray-400 mb-8">
        Connect a new MySQL database to the metadata catalog.
      </p>

      {/* Передаем refreshDatabases в форму, чтобы вызвать её после успеха */}
      <ImportForm onImportSuccess={refreshDatabases} />
    </div>
  );
};

export default ImportPage;
