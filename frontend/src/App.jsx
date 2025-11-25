import { useEffect, useState } from "react";
import { Line } from "react-chartjs-2";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Tooltip,
  Legend,
} from "chart.js";
import "./App.css";

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Tooltip,
  Legend
);

const API_URL = "http://localhost:8000";

function App() {
  const [pontos, setPontos] = useState([]);

  useEffect(() => {
    const interval = setInterval(async () => {
      try {
        const res = await fetch(`${API_URL}/data`);
        const json = await res.json();
        setPontos(json);
      } catch (err) {
        console.error("Erro ao buscar dados:", err);
      }
    }, 1000);

    return () => clearInterval(interval);
  }, []);

  const labels = pontos.map((p) => p.t.toFixed(1));

  const data = {
    labels,
    datasets: [
      {
        label: "Temperatura (°C)",
        data: pontos.map((p) => p.temp),
        borderColor: "rgba(220, 53, 69, 1)",
        backgroundColor: "rgba(220, 53, 69, 0.15)",
        borderWidth: 2,
        tension: 0.25,
        pointRadius: 3,
        pointBackgroundColor: "rgba(220, 53, 69, 1)",
        pointBorderWidth: 1,
      },
    ],
  };

  const options = {
    responsive: true,
    maintainAspectRatio: false,
    scales: {
      x: {
        title: { display: true, text: "Tempo (s)", color: "#444" },
        ticks: { color: "#555" },
        grid: { color: "rgba(0,0,0,0.05)" },
      },
      y: {
        title: { display: true, text: "Temperatura (°C)", color: "#444" },
        ticks: { color: "#555" },
        grid: { color: "rgba(0,0,0,0.05)" },
      },
    },
    plugins: {
      legend: {
        labels: { color: "#333" },
      },
      tooltip: {
        mode: "index",
        intersect: false,
      },
    },
  };

  return (
    <div className="app">
      <div className="card">
        <h1>Temperatura LM35 (ESP32 via MQTT)</h1>
        <p className="subtitle">
          Leituras publicadas pelo ESP32, recebidas via MQTT e servidas pelo
          FastAPI.
        </p>

        <div className="chart-wrapper">
          <Line data={data} options={options} />
        </div>
      </div>
    </div>
  );
}

export default App;
