import React from "react";
import {
  PieChart,
  Pie,
  Cell,
  Label,
  BarChart,
  Bar,
  XAxis,
  YAxis,
} from "recharts";

const COLORS = ["#0088FE", "#00C49F", "#FFBB28", "#FF8042"];

export const DataVisual = ({ replay_data }) => {
  return (
    <div className="recharts-wrapper">
      <PieChart width={500} height={400} className="chart">
        <Pie
          data={replay_data.my_chars.filter((e) => e.value > 0)}
          innerRadius={125}
          outerRadius={150}
          fill="#8884d8"
          dataKey="value"
          blendStroke
          label={(e) => e.name}
        >
          {replay_data.my_chars.map((entry, index) => (
            <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
          ))}
          <Label
            value="My Characters"
            position="center"
            className="chartTitle"
          />
        </Pie>
      </PieChart>

      <PieChart width={500} height={400} className="chart">
        <Pie
          data={replay_data.opp_chars.filter((e) => e.value > 0)}
          innerRadius={125}
          outerRadius={150}
          fill="#8884d8"
          dataKey="value"
          blendStroke
          label={(e) => e.name}
        >
          {replay_data.opp_chars.map((entry, index) => (
            <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
          ))}
          <Label
            value="Opponent Characters"
            position="center"
            className="chartTitle"
          />
        </Pie>
      </PieChart>
      <div>
        <h3>Stage Usage</h3>
        <BarChart
          width={800}
          height={300}
          data={replay_data.stage_count}
          className="chart"
        >
          <Bar dataKey="value" fill="#8884d8" />
          <XAxis
            dataKey="name"
            interval={0}
            angle={-45}
            textAnchor="end"
            height={100}
          />
          <YAxis />
        </BarChart>
      </div>
      <h3
        style={{
          outline: "solid 5px",
          background: "#c3b9ed",
          width: "300px",
          margin: "40px auto",
        }}
      >
        Actions per minute: {replay_data.apm}
      </h3>
    </div>
  );
};
