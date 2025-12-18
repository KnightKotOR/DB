import { createContext, useContext, useEffect, useState } from "react";
import api from "../api";

const DatabaseContext = createContext();

export const DatabaseProvider = ({ children }) => {
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
    <DatabaseContext.Provider value={{ databases, fetchDatabases }}>
      {children}
    </DatabaseContext.Provider>
  );
};

export const useDatabases = () => {
  const context = useContext(DatabaseContext);
  if (!context) throw new Error("useDatabases must be used within DatabaseProvider");
  return context;
};
