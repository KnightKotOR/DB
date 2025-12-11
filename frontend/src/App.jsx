import { BrowserRouter as Router, Routes, Route, Link } from "react-router-dom";
import ImportPage from "./pages/ImportPage";
import AliasPage from "./pages/AliasPage";
import QueryPage from "./pages/QueryPage";

const App = () => {
  return (
    <Router>
      <div className="app">
        <header className="p-4 bg-gray-800 text-white flex justify-between items-center">
          <h1 className="text-xl font-bold">Metadata</h1>
          <nav className="flex gap-2">
            <Link to="/import">
              <button>Import database</button>
            </Link>
            <Link to="/alias">
              <button>Aliases</button>
            </Link>
            <Link to="/queries">
              <button>Queries</button>
            </Link>
          </nav>
        </header>

        <main className="p-6">
          <Routes>
            <Route path="/import" element={<ImportPage />} />
          </Routes>
          <Routes>
            <Route path="/alias" element={<AliasPage />} />
          </Routes>
          <Routes>
            <Route path="/queries" element={<QueryPage />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
};

export default App;
