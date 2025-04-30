/* public/user/js/ai.js
   ───────────────────────────────────────────────────────────── */
const API_BASE = '';                     // empty = same origin

export async function suggestLocation(lat, lng) {
  const res = await fetch(`${API_BASE}/api/ai/command`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ name: 'suggest_location', args: { lat, lng } })
  });
  if (!res.ok) throw new Error(await res.text());
  return (await res.json()).data;        // → array of 5 objects
}

export function openDrawer(items) {
  const drawer  = document.getElementById('infoDrawer');
  const content = document.getElementById('drawerContent');
  content.innerHTML = items.map(i => `
      <div class="card ${i.type}">
        <h4>${i.title}</h4>
        <p>${i.snippet}</p>
        <a href="${i.url}" target="_blank">More</a>
      </div>`).join('');
  drawer.classList.add('open');
}

export function closeDrawer() {
  document.getElementById('infoDrawer').classList.remove('open');
}

document.getElementById('drawerClose')
        ?.addEventListener('click', closeDrawer);
