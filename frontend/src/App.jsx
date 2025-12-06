import { BrowserRouter as Router, Routes, Route, Link } from "react-router-dom";
import ImportPage from "./pages/ImportPage";
import StatsPage from "./pages/StatsPage";
import TimestampsPage from "./pages/TimestampsPage";

const App = () => {
  return (
    <Router>
      <div className="app">
        <header className="p-4 bg-gray-800 text-white flex justify-between items-center">
          <h1 className="text-xl font-bold">Metadata Manager</h1>
          <nav className="flex gap-2">
            <Link to="/import">
              <button>Import database</button>
            </Link>
            <Link to="/stats">
              <button>Statistics</button>
            </Link>
            <Link to="/timestamps">
              <button>Timestamps</button>
            </Link>
          </nav>
        </header>

        <main className="p-6">
          <Routes>
            <Route path="/import" element={<ImportPage />} />
            <Route path="/stats" element={<StatsPage />} />
            <Route path="/timestamps" element={<TimestampsPage />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
};

export default App;
