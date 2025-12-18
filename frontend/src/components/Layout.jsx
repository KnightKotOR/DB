import { useEffect, useState } from "react";
import { Outlet, Link } from "react-router-dom";
import api from "../api";

const Layout = () => {
  const [databases, setDatabases] = useState([]);

  // Функция загрузки баз данных (вызывается при старте и после импорта)
  const fetchDatabases = () => {
    api.get("/databases")
      .then((res) => setDatabases(res.data))
      .catch((err) => console.error("Error fetching databases:", err));
  };

  useEffect(() => {
    fetchDatabases();
  }, []);

  return (
    <div className="min-h-screen bg-gray-900 text-gray-100 flex flex-col">
      {/* --- ШАПКА (Header) --- */}
      <header className="p-4 bg-gray-800 border-b border-gray-700 flex justify-between items-center shadow-md">
        <h1 className="text-xl font-bold text-blue-400">Metadata</h1>
        <nav className="flex gap-4">
          <Link to="/import">
            <button className="px-4 py-2 bg-gray-700 hover:bg-gray-600 rounded transition">Import DB</button>
          </Link>
          <Link to="/alias">
            <button className="px-4 py-2 bg-gray-700 hover:bg-gray-600 rounded transition">Aliases</button>
          </Link>
          <Link to="/queries">
            <button className="px-4 py-2 bg-gray-700 hover:bg-gray-600 rounded transition">Queries</button>
          </Link>
        </nav>
      </header>

      {/* --- ОСНОВНОЙ КОНТЕЙНЕР --- */}
      <div className="flex h-screen" style={{ height: 'calc(100vh - 80px)' }}>  {/* Фиксируем высоту минус хедер */}
  
        {/* ЛЕВАЯ ЧАСТЬ: Контент текущей страницы */}
        <main className="flex-1 p-8 overflow-y-auto bg-gray-900">
          <Outlet context={{ refreshDatabases: fetchDatabases }} />
        </main>

        {/* ПРАВАЯ ЧАСТЬ: Сайдбар с базами данных (фиксированная ширина 350px) */}
        <aside 
          className="w-[350px] bg-gray-800 border-l border-gray-700 p-6 overflow-y-auto shadow-xl flex flex-col"
          style={{ minHeight: '100%' }}
        >
          {/* Контент сайдбара как раньше */}
          <h3 className="text-lg font-semibold mb-6 text-blue-300 border-b border-gray-600 pb-3 sticky top-0 bg-gray-800 z-10">
            Metadata Catalog
          </h3>
          
          {/* Databases */}
          <section className="flex-1 mb-6">
            <h4 className="text-sm font-medium mb-4 text-gray-300 uppercase tracking-wider border-b border-gray-700 pb-2">
              Databases
            </h4>
            {databases.length ? (
              <ul className="space-y-2 max-h-96 overflow-y-auto">
                {databases.map((db) => (
                  <li key={db.db_id} className="p-3 bg-gray-750/50 hover:bg-gray-700 rounded-lg flex items-center justify-between transition-all group border border-gray-600">
                    <span className="font-medium truncate">{db.db_name}</span>
                    <span className="text-xs px-2 py-1 bg-green-900/50 text-green-300 rounded-full border border-green-700">active</span>
                  </li>
                ))}
              </ul>
            ) : (
              <div className="text-center py-8">
                <p className="text-gray-500 mb-2">No databases.</p>
                <button 
                  onClick={fetchDatabases}
                  className="text-xs bg-blue-600 hover:bg-blue-500 px-3 py-1 rounded transition"
                >
                  Refresh
                </button>
              </div>
            )}
          </section>

          {/* Aliases задел */}
          <section>
            <h4 className="text-sm font-medium mb-3 text-gray-300 uppercase tracking-wider border-t border-gray-700 pt-4">
              Aliases
            </h4>
            <p className="text-gray-500 text-xs">Configure aliases here.</p>
          </section>
        </aside>
      </div>
    </div>
  );
};

export default Layout;
