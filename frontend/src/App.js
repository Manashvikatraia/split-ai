import { useState, useEffect } from "react";
import "./App.css";

import {
  PieChart,
  Pie,
  Cell,
  Tooltip,
  ResponsiveContainer,
  Legend
} from "recharts";

function App() {

  const [text, setText] = useState("");
  const [balances, setBalances] = useState({});
  const [settlements, setSettlements] = useState([]);
  const [expenses, setExpenses] = useState([]);
  const [loading, setLoading] = useState(false);

  // 💰 Format currency
  const formatMoney = (amount) => {
    return Number(amount).toFixed(0);
  };

  // ➕ Add Expense
  const addExpense = async () => {

    if (!text.trim()) return;

    try {

      setLoading(true);

      await fetch("http://127.0.0.1:8000/add-expense", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },

        body: JSON.stringify({
          text: text,
        }),
      });

      await fetchBalances();
      await fetchSettlement();
      await fetchExpenses();

      setText("");

    } catch (error) {

      console.log(error);

    } finally {

      setLoading(false);

    }
  };

  // 💰 Balances
  const fetchBalances = async () => {

    const res = await fetch(
      "http://127.0.0.1:8000/balances"
    );

    const data = await res.json();

    setBalances(data);
  };

  // 🤝 Settlement
  const fetchSettlement = async () => {

    const res = await fetch(
      "http://127.0.0.1:8000/settle"
    );

    const data = await res.json();

    setSettlements(data);
  };

  // 🧾 Expenses
  const fetchExpenses = async () => {

    const res = await fetch(
      "http://127.0.0.1:8000/expenses"
    );

    const data = await res.json();

    setExpenses(data.reverse());
  };

  // 🚀 Initial load
  useEffect(() => {

    fetchBalances();
    fetchSettlement();
    fetchExpenses();

  }, []);

  // 📊 Analytics

  const totalExpense = expenses.reduce(
    (sum, exp) => sum + exp.amount,
    0
  );

  const totalUsers = Object.keys(balances).length;

  const spenderMap = {};

  expenses.forEach((exp) => {

    spenderMap[exp.payer] =
      (spenderMap[exp.payer] || 0) + exp.amount;

  });

  let biggestSpender = "None";
  let maxSpent = 0;

  Object.entries(spenderMap).forEach(
    ([user, amount]) => {

      if (amount > maxSpent) {

        maxSpent = amount;
        biggestSpender = user;

      }
    }
  );

  // 📈 Chart data
  const pieData = Object.entries(spenderMap).map(
    ([name, value]) => ({
      name:
        name.charAt(0).toUpperCase() +
        name.slice(1),

      value
    })
  );

  const COLORS = [
    "#22c55e",
    "#3b82f6",
    "#f59e0b",
    "#ef4444",
    "#a855f7",
    "#06b6d4"
  ];

  return (

    <div className="app">

      {/* HEADER */}
      <h1 className="title">
        💸 Split AI
      </h1>

      <p className="subtitle">
        AI-powered smart expense sharing
      </p>

      {/* INPUT */}
      <div className="input-section">

        <input
          className="input-box"
          placeholder="e.g. Yesterday Sai spent 4200 on dinner with Mia and Ria"
          value={text}
          onChange={(e) =>
            setText(e.target.value)
          }
        />

        <button
          className="add-btn"
          onClick={addExpense}
        >
          {loading
            ? "Adding..."
            : "Add"}
        </button>

      </div>

      {/* ANALYTICS */}
      <div className="analytics">

        <div className="analytics-card">

          <h3>Total Expenses</h3>

          <p>
            ₹{formatMoney(totalExpense)}
          </p>

        </div>

        <div className="analytics-card">

          <h3>Total Users</h3>

          <p>{totalUsers}</p>

        </div>

        <div className="analytics-card">

          <h3>Biggest Spender</h3>

          <p>
            {biggestSpender}
          </p>

        </div>

      </div>

      {/* CHART */}
      <div className="chart-card">

        <h2>
          📊 Spending Distribution
        </h2>

        {pieData.length === 0 ? (

          <p>No chart data yet</p>

        ) : (

          <ResponsiveContainer
            width="100%"
            height={320}
          >

            <PieChart>

              <Pie
                data={pieData}
                dataKey="value"
                outerRadius={110}
                label
              >

                {pieData.map(
                  (entry, index) => (

                    <Cell
                      key={index}
                      fill={
                        COLORS[
                          index %
                          COLORS.length
                        ]
                      }
                    />

                  )
                )}

              </Pie>

              <Tooltip />

              <Legend />

            </PieChart>

          </ResponsiveContainer>

        )}

      </div>

      {/* BALANCE + SETTLEMENT */}
      <div className="cards">

        {/* BALANCES */}
        <div className="card">

          <h2>
            💰 Balances
          </h2>

          {Object.entries(balances).length === 0 ? (

            <p>No balances yet</p>

          ) : (

            Object.entries(balances).map(
              ([name, amount]) => (

                <div
                  key={name}
                  className="balance-item"
                >

                  <span>
                    {
                      name.charAt(0)
                        .toUpperCase() +
                      name.slice(1)
                    }
                  </span>

                  <span
                    className={
                      amount >= 0
                        ? "positive"
                        : "negative"
                    }
                  >
                    ₹
                    {formatMoney(amount)}
                  </span>

                </div>

              )
            )

          )}

        </div>

        {/* SETTLEMENT */}
        <div className="card">

          <h2>
            🤝 Settlement
          </h2>

          {settlements.length === 0 ? (

            <p>No settlements yet</p>

          ) : (

            settlements.map((s, i) => (

              <div
                key={i}
                className="settlement-item"
              >

                <span>

                  {
                    s.from.charAt(0)
                      .toUpperCase() +
                    s.from.slice(1)
                  }

                  {" → "}

                  {
                    s.to.charAt(0)
                      .toUpperCase() +
                    s.to.slice(1)
                  }

                </span>

                <span>
                  ₹
                  {formatMoney(s.amount)}
                </span>

              </div>

            ))

          )}

        </div>

      </div>

      {/* HISTORY */}
      <div className="history-card">

        <h2>
          🧾 Recent Expenses
        </h2>

        {expenses.length === 0 ? (

          <p>No expenses added yet</p>

        ) : (

          expenses.map((exp, i) => (

            <div
              key={i}
              className="history-item"
            >

              <span>

                💸 {" "}

                {
                  exp.payer
                    .charAt(0)
                    .toUpperCase() +
                  exp.payer.slice(1)
                }

                {" "}paid

              </span>

              <span>
                ₹
                {formatMoney(exp.amount)}
              </span>

            </div>

          ))

        )}

      </div>

    </div>
  );
}

export default App;