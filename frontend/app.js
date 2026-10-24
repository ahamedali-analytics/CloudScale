const $ = (id) => document.getElementById(id);

function apiBase() {
  const value = $("apiUrl").value.trim().replace(/\/+$/, "");
  if (!value) throw new Error("Enter your deployed API base URL first.");
  if (!/^https:\/\/[a-z0-9.-]+\/[A-Za-z0-9_-]+$/i.test(value)) {
    throw new Error("Enter the HTTPS ApiUrl output from AWS SAM.");
  }
  return value;
}

$("submitBtn").addEventListener("click", async () => {
  const button = $("submitBtn");
  const message = $("submitMessage");
  button.disabled = true;
  message.textContent = "Submitting workload…";
  try {
    const records = JSON.parse($("records").value);
    if (!Array.isArray(records)) throw new Error("Input must be a JSON array.");
    const response = await fetch(`${apiBase()}/jobs`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ records })
    });
    const data = await response.json();
    if (!response.ok) throw new Error(data.error || `Request failed (${response.status}).`);
    $("jobId").value = data.jobId;
    message.textContent = `Job accepted: ${data.jobId} (${data.status})`;
    await checkJob();
  } catch (error) {
    message.textContent = error.message;
  } finally {
    button.disabled = false;
  }
});

async function checkJob() {
  const id = $("jobId").value.trim();
  if (!id) throw new Error("Enter a job ID.");
  const response = await fetch(`${apiBase()}/jobs/${encodeURIComponent(id)}`);
  const data = await response.json();
  if (!response.ok) throw new Error(data.error || `Request failed (${response.status}).`);
  $("jobStatus").textContent = `Status: ${data.status} · Job: ${data.jobId}`;
  $("result").hidden = !data.result && !data.error;
  $("result").textContent = JSON.stringify(data.result || data.error || {}, null, 2);
  return data;
}

$("checkBtn").addEventListener("click", async () => {
  $("jobStatus").textContent = "Checking…";
  try { await checkJob(); }
  catch (error) { $("jobStatus").textContent = error.message; $("result").hidden = true; }
});
