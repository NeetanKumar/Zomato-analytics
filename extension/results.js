const ORDERS_ENDPOINT = "https://www.zomato.com/webroutes/user/orders";

const analyzeBtn = document.getElementById("analyze-btn");
const printBtn = document.getElementById("print-btn");
const statusEl = document.getElementById("status");
const resultsEl = document.getElementById("results");

analyzeBtn.addEventListener("click", runAnalysis);
printBtn.addEventListener("click", () => window.print());

async function runAnalysis() {
  analyzeBtn.disabled = true;
  printBtn.hidden = true;
  resultsEl.hidden = true;
  setStatus("Fetching your orders...");

  try {
    const orders = await fetchAllOrders();
    if (orders.length === 0) {
      setStatus(
        "No orders found. Make sure you're logged into zomato.com in " +
          "this browser, then try again."
      );
      return;
    }
    setStatus(`Loaded ${orders.length} orders.`);
    render(orders);
  } catch (err) {
    console.error(err);
    setStatus(
      "Couldn't reach Zomato. Make sure you're logged into zomato.com " +
        "in this browser, then try again."
    );
  } finally {
    analyzeBtn.disabled = false;
  }
}

function setStatus(text) {
  statusEl.textContent = text;
}

async function fetchAllOrders() {
  const allOrders = [];
  let page = 1;

  while (true) {
    setStatus(`Fetching page ${page}...`);
    const resp = await fetch(`${ORDERS_ENDPOINT}?page=${page}`, {
      credentials: "include",
      headers: { accept: "application/json" },
    });
    if (!resp.ok) break;

    let data;
    try {
      data = await resp.json();
    } catch {
      break; // likely got redirected to an HTML login page
    }

    const entities = data?.entities?.ORDER;
    const orderValues = entities
      ? Array.isArray(entities)
        ? entities
        : Object.values(entities)
      : [];
    if (orderValues.length === 0) break;

    for (const order of orderValues) {
      const resInfo = order.resInfo || {};
      const establishment = resInfo.establishment || [];
      allOrders.push({
        orderId: order.orderId,
        date: order.orderDate,
        cost: normalizeCost(order.totalCost),
        restaurantName: resInfo.name || "Unknown",
        establishment: establishment[0] || "",
      });
    }

    page += 1;
    await sleep(300); // be polite to Zomato's servers
  }

  return allOrders;
}

function normalizeCost(raw) {
  if (typeof raw !== "string") return Number(raw) || 0;
  const cleaned = raw.replace(/[₹,]/g, "").trim();
  return parseFloat(cleaned) || 0;
}

function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

function render(orders) {
  const totalSpent = sum(orders.map((o) => o.cost));
  const avgOrder = totalSpent / orders.length;
  const dates = orders.map((o) => new Date(o.date)).filter((d) => !isNaN(d));
  const minDate = dates.length ? new Date(Math.min(...dates)) : null;
  const maxDate = dates.length ? new Date(Math.max(...dates)) : null;

  document.getElementById("overview").innerHTML = [
    statCard("Total orders", orders.length),
    statCard("Total spent", `₹${formatNum(totalSpent)}`),
    statCard("Average order", `₹${formatNum(avgOrder)}`),
    statCard(
      "Date range",
      minDate && maxDate
        ? `${formatDate(minDate)} – ${formatDate(maxDate)}`
        : "—"
    ),
  ].join("");

  const byRestaurant = groupBy(orders, (o) => o.restaurantName);
  const countRows = Object.entries(byRestaurant)
    .map(([name, list]) => [name, list.length])
    .sort((a, b) => b[1] - a[1])
    .slice(0, 10);
  renderTable("top-by-count", countRows, (n) => `${n}x`);

  const spendRows = Object.entries(byRestaurant)
    .map(([name, list]) => [name, sum(list.map((o) => o.cost))])
    .sort((a, b) => b[1] - a[1])
    .slice(0, 10);
  renderTable("top-by-spend", spendRows, (n) => `₹${formatNum(n)}`);

  const byMonth = groupBy(orders, (o) => {
    const d = new Date(o.date);
    return isNaN(d) ? "unknown" : `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, "0")}`;
  });
  const monthRows = Object.entries(byMonth)
    .filter(([month]) => month !== "unknown")
    .map(([month, list]) => [month, sum(list.map((o) => o.cost))])
    .sort((a, b) => (a[0] > b[0] ? 1 : -1));
  renderTable("monthly", monthRows, (n) => `₹${formatNum(n)}`);

  const byEstablishment = groupBy(orders, (o) => o.establishment || "(unspecified)");
  const establishmentRows = Object.entries(byEstablishment)
    .map(([type, list]) => [type, list.length])
    .sort((a, b) => b[1] - a[1])
    .slice(0, 10);
  renderTable("establishment", establishmentRows, (n) => `${n}x`);

  resultsEl.hidden = false;
  printBtn.hidden = false;
}

function statCard(label, value) {
  return `<div class="stat"><div class="label">${label}</div><div class="value">${value}</div></div>`;
}

function renderTable(elementId, rows, formatValue) {
  const table = document.getElementById(elementId);
  table.innerHTML = rows
    .map(
      ([name, value]) =>
        `<tr><td>${escapeHtml(name)}</td><td class="num">${formatValue(value)}</td></tr>`
    )
    .join("");
}

function groupBy(items, keyFn) {
  const groups = {};
  for (const item of items) {
    const key = keyFn(item);
    (groups[key] = groups[key] || []).push(item);
  }
  return groups;
}

function sum(nums) {
  return nums.reduce((a, b) => a + b, 0);
}

function formatNum(n) {
  return Math.round(n).toLocaleString("en-IN");
}

function formatDate(d) {
  return d.toISOString().slice(0, 10);
}

function escapeHtml(str) {
  const div = document.createElement("div");
  div.textContent = str;
  return div.innerHTML;
}
