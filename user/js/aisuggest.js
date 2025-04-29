// user/js/aiSuggest.js
// -------------------------------------------------------
// Call the Spot-On backend to get AI suggestions for a lat/lng
// -------------------------------------------------------
const ENDPOINT = "https://spoton-backend.vercel.app/api/recommend";   // ← change after deploy

export async function fetchAISuggestion(lat, lng, zoom = 12) {
  const res = await fetch(ENDPOINT, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ lat, lng, zoom })
  });
  if (!res.ok) {
    const err = await res.text();
    throw new Error(`AI API ${res.status}: ${err}`);
  }
  return await res.json();   // { summary, suggested_title, suggested_description, tags }
}
