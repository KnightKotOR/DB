import React from "react";

const DatabaseStats = ({
  loading,
  tableCount,
  columnCount,
  pkCount,
  fkCount,
  ukCount,
  recordCount,
  selectedDb,
  selectedStats,
}) => {
  if (!selectedDb) return null;

  const rows = [];

  if (selectedStats.tables)
    rows.push(["Tables count", tableCount]);
  if (selectedStats.columns)
    rows.push(["Columns count", columnCount]);
  if (selectedStats.pk)
    rows.push(["Primary keys count", pkCount]);
  if (selectedStats.fk)
    rows.push(["Foreign keys count", fkCount]);
  if (selectedStats.uk)
    rows.push(["Unique keys count", ukCount]);
  if (selectedStats.records)
    rows.push(["Records count", recordCount]);

  return (
    <div className="db-stats">
      {loading && <p>Loading...</p>}

      {!loading && rows.length > 0 && (
        <table
          className="stats-table"
          >
          <tbody>
            {rows.map(([label, value]) => (
              <tr key={label}>
                <td>
                  {label}
                </td>
                <td>
                  {value !== null ? value : "-"}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}

      {!loading && rows.length === 0 && (
        <p style={{ color: "gray" }}>
          No statistics selected.
        </p>
      )}
    </div>
  );
};

export default DatabaseStats;
