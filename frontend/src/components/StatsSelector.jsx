import React from "react";

const statsOptions = [
  { key: "tables", label: "Tables count" },
  { key: "columns", label: "Columns count" },
  { key: "pk", label: "Primary keys count" },
  { key: "fk", label: "Foreign keys count" },
  { key: "uk", label: "Unique keys count" },
  { key: "records", label: "Records count" },
];

const StatsSelector = ({ selectedStats, onChange }) => {
  const handleChange = (key) => {
    onChange({
      ...selectedStats,
      [key]: !selectedStats[key],
    });
  };

  return (
    <div className="stats-selector">
      <h3>Select statistics to show:</h3>
      <ul style={{ listStyle: "none", padding: 0 }}>
        {statsOptions.map(({ key, label }) => (
          <li key={key}>
            <label>
              <input
                type="checkbox"
                checked={!!selectedStats[key]}
                onChange={() => handleChange(key)}
              />
              <span style={{ marginLeft: "8px" }}>{label}</span>
            </label>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default StatsSelector;
