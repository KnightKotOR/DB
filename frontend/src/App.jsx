import { BrowserRouter as Router, Routes, Route, Navigate } from "react-router-dom";
import Layout from "./components/Layout";
import ImportPage from "./pages/ImportPage";
import AliasPage from "./pages/AliasPage";
import QueryPage from "./pages/QueryPage";

const App = () => {
  return (
    <Router>
      <Routes>
        {/* Все страницы внутри Layout получат общую шапку и сайдбар */}
        <Route path="/" element={<Layout />}>
          {/* Редирект с корня на импорт */}
          <Route index element={<Navigate to="/import" replace />} />
          
          <Route path="import" element={<ImportPage />} />
          <Route path="alias" element={<AliasPage />} />
          <Route path="queries" element={<QueryPage />} />
        </Route>
      </Routes>
    </Router>
  );
};

export default App;
