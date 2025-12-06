import React, { useEffect, useState } from "react";
import api from "../api";
import DatabaseSelector from "../components/DatabaseSelector";
import DatabaseStats from "../components/DatabaseStats";
import StatsSelector from "../components/StatsSelector";

const StatsPage = () => {
  const [databases, setDatabases] = useState([]);
  const [selectedDb, setSelectedDb] = useState(null);
  const [tableCount, setTableCount] = useState(null);
  const [columnCount, setColumnCount] = useState(null);
  const [pkCount, setPkCount] = useState(null);
  const [fkCount, setFkCount] = useState(null);
  const [ukCount, setUkCount] = useState(null);
  const [recordCount, setRecordCount] = useState(null);
  const [loading, setLoading] = useState(false);

  const [selectedStats, setSelectedStats] = useState({
    tables: false,
    columns: false,
    pk: false,
    fk: false,
    uk: false,
    records: false,
  });

  useEffect(() => {
    api.get("/databases/")
      .then((res) => setDatabases(res.data))
      .catch(console.error);
  }, []);

  const fetchers = {
    tables: async (dbId) => {
      const res = await api.get(`/databases/${dbId}/tables/count`);
      setTableCount(res.data.count);
    },
    columns: async (dbId) => {
      const res = await api.get(`/databases/${dbId}/columns/count`);
      setColumnCount(res.data.count);
    },
    pk: async (dbId) => {
      const res = await api.get(`/databases/${dbId}/keys/primary/count`);
      setPkCount(res.data.count);
    },
    fk: async (dbId) => {
      const res = await api.get(`/databases/${dbId}/keys/foreign/count`);
      setFkCount(res.data.count);
    },
    uk: async (dbId) => {
      const res = await api.get(`/databases/${dbId}/keys/unique/count`);
      setUkCount(res.data.count);
    },
    records: async (dbId) => {
      const res = await api.get(`/databases/${dbId}/records/count`);
      setRecordCount(res.data.count);
    },
  };

  // when user selects a new database
  const handleSelectChange = async (dbId) => {
    setSelectedDb(dbId);

    setTableCount(null);
    setColumnCount(null);
    setPkCount(null);
    setFkCount(null);
    setUkCount(null);
    setRecordCount(null);

    if (!dbId) return;

    // fetch all currently selected stats for new database
    const activeStats = Object.keys(selectedStats).filter((key) => selectedStats[key]);
    if (activeStats.length > 0) {
      setLoading(true);
      try {
        await Promise.all(activeStats.map((key) => fetchers[key](dbId)));
      } catch (err) {
        console.error(err);
      } finally {
        setLoading(false);
      }
    }
  };

  // when user toggles a stat checkbox
  const handleStatsChange = async (newSelectedStats) => {
    if (!selectedDb) {
      setSelectedStats(newSelectedStats);
      return;
    }

    // determine which stat was just toggled
    const changedKey = Object.keys(newSelectedStats).find(
      (key) => newSelectedStats[key] !== selectedStats[key]
    );

    setSelectedStats(newSelectedStats);

    if (changedKey) {
      if (newSelectedStats[changedKey]) {
        // checkbox checked - fetch new data
        setLoading(true);
        try {
          await fetchers[changedKey](selectedDb);
        } catch (err) {
          console.error(err);
        } finally {
          setLoading(false);
        }
      } else {
        // checkbox unchecked - clear the value immediately (looks ugly rn. maybe find way to refactor)
        switch (changedKey) {
          case "tables":
            setTableCount(null);
            break;
          case "columns":
            setColumnCount(null);
            break;
          case "pk":
            setPkCount(null);
            break;
          case "fk":
            setFkCount(null);
            break;
          case "uk":
            setUkCount(null);
            break;
          case "records":
            setRecordCount(null);
            break;
        }
      }
    }
  };

  const handleSaveStats = async () => {
    if (!selectedDb) {
      alert("Select a database first.");
      return;
    }

    const payload = {
      db_id: selectedDb,
      tables_count: selectedStats.tables ? tableCount : null,
      columns_count: selectedStats.columns ? columnCount : null,
      pk_count: selectedStats.pk ? pkCount : null,
      fk_count: selectedStats.fk ? fkCount : null,
      uk_count: selectedStats.uk ? ukCount : null,
      records_count: selectedStats.records ? recordCount : null,
    };

    // ensure user selected at least 1 stat
    const anySelected = Object.values(selectedStats).some((v) => v);
    if (!anySelected) {
      alert("Select at least one statistic.");
      return;
    }

    try {
      console.log(payload);
      await api.post("/timestamps/save", payload);
      alert("Statistics saved!");
    } catch (err) {
      console.error(err);
      alert("Failed to save statistics");
    }
  };

  return (
    <div>
      <h2 className="text-2xl font-semibold">Statistics</h2>

      <div className="database-container" style={{ display: "flex", gap: "2rem" }}>
        <div>
          <DatabaseSelector
            databases={databases}
            selectedDb={selectedDb}
            onSelect={handleSelectChange}
          />
          <StatsSelector
            selectedStats={selectedStats}
            onChange={handleStatsChange}
          />
        </div>

        <DatabaseStats
          loading={loading}
          tableCount={tableCount}
          columnCount={columnCount}
          pkCount={pkCount}
          fkCount={fkCount}
          ukCount={ukCount}
          recordCount={recordCount}
          selectedDb={selectedDb}
          selectedStats={selectedStats}
        />
      </div>
      <button
          className="bg-green-600 text-white px-4 py-2 rounded mt-4"
          onClick={handleSaveStats}
        >
          Save statistics
        </button>
    </div>
  );
};

export default StatsPage;
