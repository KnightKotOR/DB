import React from "react";

const DatabaseSelector = ({ databases, selectedDb, onSelect }) => {
  return (
    <div className="db-selector">
      <h2>Select database:</h2>
      <select
        value={selectedDb || ""}
        onChange={(e) => onSelect(e.target.value)}
        className="db-select"
      >
        <option value="">-- Select database --</option>
        {databases.map((db) => (
          <option key={db.db_id} value={db.db_id}>
            {db.db_name}
          </option>
        ))}
      </select>
    </div>
  );
};

export default DatabaseSelector;
