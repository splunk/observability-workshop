const state = {
  products: [],
  category: "All",
  search: "",
  wideOnly: false,
  inStockOnly: true,
  sort: "featured",
  cart: [],
  chatHistory: [],
  sessionTokens: 0,
};

const els = {
  productGrid: document.querySelector("#productGrid"),
  productCount: document.querySelector("#productCount"),
  categoryFilters: document.querySelector("#categoryFilters"),
  searchInput: document.querySelector("#searchInput"),
  wideOnly: document.querySelector("#wideOnly"),
  inStockOnly: document.querySelector("#inStockOnly"),
  sortSelect: document.querySelector("#sortSelect"),
  cartCount: document.querySelector("#cartCount"),
  chatPanel: document.querySelector("#chatPanel"),
  chatLog: document.querySelector("#chatLog"),
  chatForm: document.querySelector("#chatForm"),
  chatInput: document.querySelector("#chatInput"),
  sessionTokens: document.querySelector("#sessionTokens"),
  lastTokens: document.querySelector("#lastTokens"),
  lastLatency: document.querySelector("#lastLatency"),
  nimStatus: document.querySelector("#nimStatus"),
  productDialog: document.querySelector("#productDialog"),
  dialogContent: document.querySelector("#dialogContent"),
  dialogClose: document.querySelector("#dialogClose"),
  heroChatButton: document.querySelector("#heroChatButton"),
};

const swatchColors = {
  Black: "#111418",
  Blue: "#0a60ff",
  Cobalt: "#084fc7",
  Copper: "#b46a3c",
  Cream: "#eee5d5",
  Cyan: "#02b8df",
  Forest: "#24523a",
  Graphite: "#4d545c",
  Green: "#1f7a54",
  Magenta: "#e4006d",
  Navy: "#1c2c46",
  Orange: "#f28c28",
  Rose: "#d5778a",
  Sand: "#c9b89d",
  Sky: "#7fc9f1",
  Slate: "#687484",
  Volt: "#c8ff00",
  White: "#ffffff",
};

function money(value) {
  return new Intl.NumberFormat("en-US", {
    style: "currency",
    currency: "USD",
  }).format(value);
}

async function loadHealth() {
  try {
    const response = await fetch("/healthz");
    const health = await response.json();
    els.nimStatus.textContent = health.nim_configured ? "NIM live" : "Local mode";
    els.nimStatus.classList.toggle("is-live", Boolean(health.nim_configured));
  } catch {
    els.nimStatus.textContent = "Offline";
  }
}

async function loadProducts() {
  const response = await fetch("/api/products");
  const data = await response.json();
  state.products = data.products || [];
  renderCategoryFilters();
  renderProducts();
}

function categories() {
  return ["All", ...Array.from(new Set(state.products.map((product) => product.category)))];
}

function renderCategoryFilters() {
  els.categoryFilters.innerHTML = "";
  categories().forEach((category) => {
    const button = document.createElement("button");
    button.type = "button";
    button.textContent = category;
    button.classList.toggle("is-active", category === state.category);
    button.addEventListener("click", () => {
      state.category = category;
      document.querySelectorAll("[data-nav-category]").forEach((navButton) => {
        navButton.classList.toggle("is-active", navButton.dataset.navCategory === category);
      });
      renderCategoryFilters();
      renderProducts();
    });
    els.categoryFilters.append(button);
  });
}

function filteredProducts() {
  const query = state.search.toLowerCase();
  const products = state.products.filter((product) => {
    const matchesCategory = state.category === "All" || product.category === state.category;
    const haystack = [
      product.name,
      product.category,
      product.audience,
      product.description,
      product.tags.join(" "),
      product.colors.join(" "),
    ]
      .join(" ")
      .toLowerCase();
    const matchesSearch = !query || haystack.includes(query);
    const matchesWide = !state.wideOnly || product.widths.includes("Wide");
    const matchesStock = !state.inStockOnly || product.stock > 0;
    return matchesCategory && matchesSearch && matchesWide && matchesStock;
  });

  if (state.sort === "price-low") return products.sort((a, b) => a.price - b.price);
  if (state.sort === "price-high") return products.sort((a, b) => b.price - a.price);
  if (state.sort === "rating") return products.sort((a, b) => b.rating - a.rating);
  return products;
}

function renderProducts() {
  const products = filteredProducts();
  els.productCount.textContent = `${products.length} product${products.length === 1 ? "" : "s"}`;
  els.productGrid.innerHTML = "";

  products.forEach((product) => {
    const card = document.createElement("article");
    card.className = "product-card";
    card.innerHTML = `
      <div class="product-media">
        <img src="${product.image}" alt="${product.name}" loading="lazy" />
        <span class="stock-badge">${product.stock} in stock</span>
      </div>
      <div class="product-body">
        <div class="product-meta">
          <span>${product.category}</span>
          <span>${product.rating.toFixed(1)} / 5</span>
        </div>
        <h3>${product.name}</h3>
        <p>${product.description}</p>
        <div class="swatches" aria-label="${product.name} colors">
          ${product.colors
            .map(
              (color) =>
                `<span class="swatch" title="${color}" style="background: ${swatchColors[color] || "#d7dde5"}"></span>`,
            )
            .join("")}
        </div>
        <div class="product-footer">
          <span class="price">${money(product.price)}</span>
          <button type="button" data-add="${product.id}">Add</button>
        </div>
      </div>
    `;

    card.addEventListener("click", (event) => {
      if (event.target.closest("button")) return;
      openProduct(product);
    });
    card.querySelector("[data-add]").addEventListener("click", () => addToCart(product));
    els.productGrid.append(card);
  });
}

function addToCart(product) {
  state.cart.push(product.id);
  els.cartCount.textContent = String(state.cart.length);
}

function openProduct(product) {
  els.dialogContent.innerHTML = `
    <div class="dialog-product">
      <img src="${product.image}" alt="${product.name}" />
      <div class="dialog-copy">
        <p class="eyebrow">${product.category} / ${product.audience}</p>
        <h2>${product.name}</h2>
        <p>${product.description}</p>
        <div class="detail-list">
          <div><span>Price</span><strong>${money(product.price)}</strong></div>
          <div><span>Rating</span><strong>${product.rating.toFixed(1)} / 5</strong></div>
          <div><span>Sizes</span><strong>${product.sizes.join(", ")}</strong></div>
          <div><span>Widths</span><strong>${product.widths.length ? product.widths.join(", ") : "Standard fit"}</strong></div>
          <div><span>Colors</span><strong>${product.colors.join(", ")}</strong></div>
          <div><span>Stock</span><strong>${product.stock}</strong></div>
        </div>
        <div class="dialog-actions">
          <button type="button" data-dialog-add="${product.id}">Add to cart</button>
          <button class="secondary" type="button" data-ask="${product.id}">Ask about it</button>
        </div>
      </div>
    </div>
  `;
  els.dialogContent.querySelector("[data-dialog-add]").addEventListener("click", () => addToCart(product));
  els.dialogContent.querySelector("[data-ask]").addEventListener("click", () => {
    els.productDialog.close();
    focusChat(`Can you help me decide if the ${product.name} is right for me?`);
  });
  els.productDialog.showModal();
}

function focusChat(text = "") {
  els.chatPanel.scrollIntoView({ behavior: "smooth", block: "start" });
  if (text) els.chatInput.value = text;
  els.chatInput.focus();
}

function appendMessage(role, text, meta = "") {
  const message = document.createElement("div");
  message.className = `message ${role}`;
  const metaNode = document.createElement("div");
  metaNode.className = "message-meta";
  metaNode.textContent = meta || (role === "user" ? "You" : "ShopMate");
  const bodyNode = document.createElement("div");
  bodyNode.className = "message-text";
  bodyNode.textContent = text;
  message.append(metaNode, bodyNode);
  els.chatLog.append(message);
  els.chatLog.scrollTop = els.chatLog.scrollHeight;
}

function updateTokenMeter(usage, latencyMs) {
  const total = usage?.total_tokens || 0;
  state.sessionTokens += total;
  els.sessionTokens.textContent = String(state.sessionTokens);
  els.lastTokens.textContent = String(total);
  els.lastLatency.textContent = `${latencyMs || 0} ms`;
}

async function sendChat(message) {
  const trimmed = message.trim();
  if (!trimmed) return;

  appendMessage("user", trimmed);
  els.chatInput.value = "";
  els.chatForm.querySelector("button").disabled = true;

  const historyForServer = state.chatHistory.slice(-8);
  state.chatHistory.push({ role: "user", content: trimmed });

  try {
    const response = await fetch("/api/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        message: trimmed,
        history: historyForServer,
      }),
    });
    const data = await response.json();
    if (!response.ok) throw new Error(data.error || "Chat request failed");
    appendMessage("assistant", data.reply, `${data.nim_enabled ? "NIM" : "Local"} / ${data.usage.total_tokens} tokens`);
    state.chatHistory.push({ role: "assistant", content: data.reply });
    updateTokenMeter(data.usage, data.latency_ms);
  } catch (error) {
    appendMessage("assistant", "I could not reach the assistant service. Try again in a moment.", "Error");
    console.error(error);
  } finally {
    els.chatForm.querySelector("button").disabled = false;
    els.chatInput.focus();
  }
}

function bindEvents() {
  els.searchInput.addEventListener("input", () => {
    state.search = els.searchInput.value.trim();
    renderProducts();
  });

  els.wideOnly.addEventListener("change", () => {
    state.wideOnly = els.wideOnly.checked;
    renderProducts();
  });

  els.inStockOnly.addEventListener("change", () => {
    state.inStockOnly = els.inStockOnly.checked;
    renderProducts();
  });

  els.sortSelect.addEventListener("change", () => {
    state.sort = els.sortSelect.value;
    renderProducts();
  });

  document.querySelectorAll("[data-nav-category]").forEach((button) => {
    button.addEventListener("click", () => {
      state.category = button.dataset.navCategory;
      document.querySelectorAll("[data-nav-category]").forEach((navButton) => {
        navButton.classList.toggle("is-active", navButton === button);
      });
      renderCategoryFilters();
      renderProducts();
    });
  });

  document.querySelectorAll(".prompt-chips button").forEach((button) => {
    button.addEventListener("click", () => {
      sendChat(button.textContent);
    });
  });

  els.heroChatButton.addEventListener("click", () => focusChat());
  els.dialogClose.addEventListener("click", () => els.productDialog.close());
  els.productDialog.addEventListener("click", (event) => {
    if (event.target === els.productDialog) els.productDialog.close();
  });

  els.chatForm.addEventListener("submit", (event) => {
    event.preventDefault();
    sendChat(els.chatInput.value);
  });

  els.chatInput.addEventListener("keydown", (event) => {
    if (event.key === "Enter" && !event.shiftKey) {
      event.preventDefault();
      sendChat(els.chatInput.value);
    }
  });
}

async function boot() {
  bindEvents();
  appendMessage("assistant", "Tell me what you are shopping for and I will narrow the catalog.", "ShopMate");
  await Promise.all([loadHealth(), loadProducts()]);
}

boot();
