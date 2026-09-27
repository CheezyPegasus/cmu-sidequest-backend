// LOCAL TEST:
// const BACKEND_URL = "http://127.0.0.1:5000";

// AFTER RENDER DEPLOYMENT, replace this with your real URL:
const BACKEND_URL = "https://YOUR-RENDER-SERVICE.onrender.com";

const statusEl = document.querySelector("#status");
const resultEl = document.querySelector("#result");

document.querySelector("#go").addEventListener("click", async () => {
  const payload = {
    time: Number(document.querySelector("#time").value),
    distance: Number(document.querySelector("#distance").value),
    budget: document.querySelector("#budget").value,
    group: document.querySelector("#group").value,
  };

  statusEl.textContent = "Finding a sidequest...";
  resultEl.classList.add("hidden");

  try {
    const response = await fetch(`${BACKEND_URL}/recommend`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(payload),
    });

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.error || "The backend returned an error.");
    }

    const s = data.sidequest;

    document.querySelector("#category").textContent = s.category.toUpperCase();
    document.querySelector("#title").textContent = s.title;
    document.querySelector("#description").textContent = s.description;
    document.querySelector("#address").textContent = s.address;
    document.querySelector("#stats").textContent =
      `${s.difficulty} · ${s.time_hours} hr · ${s.distance_miles} mi · ${s.cost}`;

    statusEl.textContent = `Found ${data.match_count} matching sidequest(s).`;
    resultEl.classList.remove("hidden");
  } catch (error) {
    statusEl.textContent = `Error: ${error.message}`;
  }
});
