const express = require("express");
const http = require("http");

const app = express();
const PORT = 3000;
const ORDER_PROCESSOR_URL =
  process.env.ORDER_PROCESSOR_URL || "http://order-processor:8080";

app.get("/", (_req, res) => {
  res.send(`
    <!DOCTYPE html>
    <html lang="en">
    <head>
      <meta charset="UTF-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <title>OBI Workshop - Order App</title>
      <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: system-ui, sans-serif; background: #0f172a; color: #e2e8f0; min-height: 100vh; display: flex; align-items: center; justify-content: center; }
        .card { background: #1e293b; border-radius: 12px; padding: 2.5rem; max-width: 480px; width: 90%; box-shadow: 0 4px 24px rgba(0,0,0,0.4); }
        h1 { font-size: 1.5rem; margin-bottom: 0.5rem; }
        p { color: #94a3b8; margin-bottom: 1.5rem; font-size: 0.95rem; }
        button { background: #6366f1; color: white; border: none; padding: 0.75rem 1.5rem; border-radius: 8px; font-size: 1rem; cursor: pointer; width: 100%; transition: background 0.2s; }
        button:hover { background: #4f46e5; }
        button:disabled { background: #475569; cursor: wait; }
        #result { margin-top: 1.25rem; padding: 1rem; background: #0f172a; border-radius: 8px; font-family: monospace; font-size: 0.85rem; white-space: pre-wrap; display: none; }
      </style>
    </head>
    <body>
      <div class="card">
        <h1>Order Service</h1>
        <p>Click below to create an order. This request flows through three services: Frontend &rarr; Order-Processor &rarr; Payment-Service.</p>
        <button id="btn" onclick="createOrder()">Create Order</button>
        <div id="result"></div>
      </div>
      <script>
        async function createOrder() {
          const btn = document.getElementById('btn');
          const result = document.getElementById('result');
          btn.disabled = true;
          btn.textContent = 'Processing...';
          result.style.display = 'none';
          try {
            const res = await fetch('/create-order');
            const data = await res.json();
            result.textContent = JSON.stringify(data, null, 2);
            result.style.display = 'block';
          } catch (err) {
            result.textContent = 'Error: ' + err.message;
            result.style.display = 'block';
          } finally {
            btn.disabled = false;
            btn.textContent = 'Create Order';
          }
        }
      </script>
    </body>
    </html>
  `);
});

app.get("/create-order", (_req, res) => {
  const url = `${ORDER_PROCESSOR_URL}/process-order`;
  http
    .get(url, (upstream) => {
      let body = "";
      upstream.on("data", (chunk) => (body += chunk));
      upstream.on("end", () => {
        try {
          res.json(JSON.parse(body));
        } catch {
          res.status(502).json({ error: "Bad response from order-processor" });
        }
      });
    })
    .on("error", (err) => {
      res.status(503).json({ error: `order-processor unreachable: ${err.message}` });
    });
});

app.get("/healthz", (_req, res) => res.send("ok"));

app.get("/metrics", (_req, res) => {
  res.set("Content-Type", "text/plain; charset=utf-8");
  res.send(
    "# HELP workshop_heartbeat App is alive\n# TYPE workshop_heartbeat gauge\nworkshop_heartbeat 1\n"
  );
});

app.listen(PORT, () => console.log(`frontend listening on :${PORT}`));
