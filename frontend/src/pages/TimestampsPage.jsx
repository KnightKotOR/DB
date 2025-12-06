import React, { useEffect, useState } from "react";
import api from "../api";

const TimestampsPage = () => {
  const [records, setRecords] = useState([]);
  const [loading, setLoading] = useState(true);

  const formatTime = (isoString) => {
    const d = new Date(isoString);
    const pad = (n) => String(n).padStart(2, "0");

    return (
      `${pad(d.getDate())}.${pad(d.getMonth() + 1)}.${String(
        d.getFullYear()
      ).slice(2)} ` +
      `${pad(d.getHours())}:${pad(d.getMinutes())}:${pad(d.getSeconds())}`
    );
  };

  // rounds numbers and displays null as "—"
  const fmt = (value) => {
    if (value === null || value === undefined) return "—";
    return Math.round(value);
  };

    useEffect(() => {
    api
      .get("/timestamps")
      .then((res) => {
        const sorted = [...res.data].sort(
          (a, b) => new Date(b.time) - new Date(a.time)
        );
        setRecords(sorted);
      })
      .catch((err) => console.error("Failed to load stats:", err))
      .finally(() => setLoading(false));
  }, []);

  return (
    <div>
      <h2 className="text-2xl font-semibold mb-4">Saved Statistics</h2>

      {loading && <p>Loading...</p>}

      {!loading && (
        <table className="stats-table">
        <thead>
          <tr>
            <th>Time</th>
            <th>DB ID</th>
            <th>DB Name</th>
            <th>Tables</th>
            <th>Columns</th>
            <th>PK</th>
            <th>FK</th>
            <th>UK</th>
            <th>Records</th>
          </tr>
        </thead>

        <tbody>
          {records.map((r, idx) => (
            <tr key={idx}>
              <td>{formatTime(r.time)}</td>
              <td>{r.db_id}</td>
              <td>{r.db_name}</td>
              <td>{fmt(r.tables_count)}</td>
              <td>{fmt(r.columns_count)}</td>
              <td>{fmt(r.pk_count)}</td>
              <td>{fmt(r.fk_count)}</td>
              <td>{fmt(r.uk_count)}</td>
              <td>{fmt(r.records_count)}</td>
            </tr>
          ))}
        </tbody>
      </table>
      )}
    </div>
  );
};

export default TimestampsPage;
