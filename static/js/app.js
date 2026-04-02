/* ── MediSense AI · Frontend JavaScript ─────────────────────────────────── */

// ── Navigation ───────────────────────────────────────────────────────────────
document.querySelectorAll('.nav-btn').forEach(btn => {
  btn.addEventListener('click', () => {
    const target = btn.dataset.section;
    document.querySelectorAll('.nav-btn').forEach(b => b.classList.remove('active'));
    document.querySelectorAll('.section').forEach(s => s.classList.remove('active'));
    btn.classList.add('active');
    document.getElementById(`section-${target}`).classList.add('active');

    if (target === 'history') loadHistory();
    if (target === 'reminders') loadReminders();
  });
});

// ── Health Tip ────────────────────────────────────────────────────────────────
async function loadTip() {
  try {
    const res = await fetch('/api/health-tip');
    const data = await res.json();
    document.getElementById('tipText').textContent = data.tip;
  } catch { }
}
loadTip();

// ── Quick-add chips ───────────────────────────────────────────────────────────
function addChip(symptom) {
  const ta = document.getElementById('symptomsInput');
  const val = ta.value.trim();
  if (val && !val.endsWith(',')) {
    ta.value = val + ', ' + symptom;
  } else if (val.endsWith(',')) {
    ta.value = val + ' ' + symptom;
  } else {
    ta.value = symptom;
  }
  ta.focus();
}

// ── Loader ────────────────────────────────────────────────────────────────────
function showLoader() { document.getElementById('loader').style.display = 'flex'; }
function hideLoader() { document.getElementById('loader').style.display = 'none'; }

// ── Symptom Analysis ──────────────────────────────────────────────────────────
async function analyzeSymptoms() {
  const symptoms = document.getElementById('symptomsInput').value.trim();
  const age = document.getElementById('ageInput').value || 30;
  const gender = document.getElementById('genderInput').value;

  if (!symptoms) {
    showResult(`<div class="result-card"><p style="color:var(--red)">⚠ Please describe your symptoms first.</p></div>`);
    return;
  }

  showLoader();
  try {
    const res = await fetch('/api/analyze', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ symptoms, age, gender }),
    });
    const data = await res.json();
    hideLoader();

    if (!data.success) {
      showResult(`<div class="result-card"><p style="color:var(--orange)">⚠ ${data.message}</p></div>`);
      return;
    }

    const urgencyEmoji = { high: '🔴', moderate: '🟠', low: '🟢' };

    const html = `
      <div class="result-card urgency-${data.urgency}">
        <div class="urgency-badge ${data.urgency}">
          ${urgencyEmoji[data.urgency]} ${data.urgency} urgency
        </div>

        <div class="result-section">
          <h4>Symptoms Detected</h4>
          <div class="tag-list">
            ${data.matched_symptoms.map(s => `<span class="tag">🩺 ${s}</span>`).join('')}
          </div>
        </div>

        <div class="result-section">
          <h4>Possible Conditions</h4>
          <div class="tag-list">
            ${data.possible_conditions.map(c => `<span class="tag">${c}</span>`).join('')}
          </div>
        </div>

        <div class="result-section">
          <h4>Medical Advice</h4>
          <div class="advice-box">${data.advice}</div>
        </div>

        <div class="result-section">
          <h4>Suggested Remedies</h4>
          <div class="tag-list">
            ${data.remedies.map(r => `<span class="tag">💊 ${r}</span>`).join('')}
          </div>
        </div>

        <p class="disclaimer">⚕ ${data.disclaimer}</p>
      </div>
    `;
    showResult(html);
  } catch (err) {
    hideLoader();
    showResult(`<div class="result-card"><p style="color:var(--red)">Error analyzing symptoms. Please try again.</p></div>`);
  }
}

function showResult(html) {
  const area = document.getElementById('resultArea');
  area.innerHTML = html;
  area.style.display = 'block';
  area.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

// ── BMI Calculator ────────────────────────────────────────────────────────────
async function calculateBMI() {
  const weight = document.getElementById('weightInput').value;
  const height = document.getElementById('heightInput').value;

  if (!weight || !height) {
    alert('Please enter both weight and height.');
    return;
  }

  showLoader();
  try {
    const res = await fetch('/api/bmi', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ weight: parseFloat(weight), height: parseFloat(height) }),
    });
    const data = await res.json();
    hideLoader();

    if (!data.success) {
      alert('Invalid input values.');
      return;
    }

    const colorMap = { green: 'var(--green)', blue: 'var(--blue)', orange: 'var(--orange)', red: 'var(--red)' };
    const c = colorMap[data.color] || 'var(--accent)';

    const el = document.getElementById('bmiResult');
    el.innerHTML = `
      <div class="bmi-number" style="color:${c}">${data.bmi}</div>
      <div class="bmi-category" style="color:${c}">${data.category}</div>
      <div class="bmi-advice">${data.advice}</div>
    `;
    el.style.display = 'block';
  } catch {
    hideLoader();
  }
}

// ── Medicine Reminders ────────────────────────────────────────────────────────
async function addReminder() {
  const medicine = document.getElementById('medName').value.trim();
  const dosage = document.getElementById('medDosage').value.trim();
  const time = document.getElementById('medTime').value;
  const frequency = document.getElementById('medFrequency').value;

  if (!medicine) { alert('Please enter medicine name.'); return; }

  try {
    const res = await fetch('/api/reminders', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ medicine, dosage, time, frequency }),
    });
    const data = await res.json();
    if (data.success) {
      document.getElementById('medName').value = '';
      document.getElementById('medDosage').value = '';
      document.getElementById('medTime').value = '';
      loadReminders();
    }
  } catch (err) {
    console.error(err);
  }
}

async function loadReminders() {
  try {
    const res = await fetch('/api/reminders');
    const data = await res.json();
    const list = document.getElementById('reminderList');

    if (!data.reminders.length) {
      list.innerHTML = `<div class="empty-state"><div class="empty-icon">💊</div><p>No reminders yet. Add your first medication above.</p></div>`;
      return;
    }

    list.innerHTML = data.reminders.map(r => `
      <div class="reminder-item" id="rem-${r.id}">
        <div class="reminder-info">
          <div class="reminder-med">💊 ${r.medicine}${r.dosage ? ` — ${r.dosage}` : ''}</div>
          <div class="reminder-meta">${r.frequency} · Added ${r.created}</div>
        </div>
        <div class="reminder-right">
          ${r.time ? `<div class="reminder-time">${formatTime(r.time)}</div>` : ''}
          <button class="btn-delete" onclick="deleteReminder('${r.id}')">✕ Remove</button>
        </div>
      </div>
    `).join('');
  } catch (err) {
    console.error(err);
  }
}

async function deleteReminder(id) {
  try {
    await fetch(`/api/reminders/${id}`, { method: 'DELETE' });
    loadReminders();
  } catch (err) {
    console.error(err);
  }
}

function formatTime(t) {
  if (!t) return '';
  const [h, m] = t.split(':').map(Number);
  const ampm = h >= 12 ? 'PM' : 'AM';
  const h12 = h % 12 || 12;
  return `${h12}:${m.toString().padStart(2, '0')} ${ampm}`;
}

// ── Health History ────────────────────────────────────────────────────────────
async function loadHistory() {
  try {
    const res = await fetch('/api/history');
    const data = await res.json();
    const list = document.getElementById('historyList');

    if (!data.history.length) {
      list.innerHTML = `<div class="empty-state"><div class="empty-icon">📋</div><p>No history yet. Run a symptom analysis to get started.</p></div>`;
      return;
    }

    list.innerHTML = [...data.history].reverse().map(h => `
      <div class="history-item">
        <div class="history-meta">
          <span class="history-date">🗓 ${h.date}${h.age ? ` · Age ${h.age}` : ''}${h.gender !== 'unknown' ? ` · ${h.gender}` : ''}</span>
          <span class="urgency-badge ${h.result.urgency}" style="font-size:0.7rem;padding:3px 10px;">${h.result.urgency}</span>
        </div>
        <div class="history-symptoms"><strong>Symptoms:</strong> ${h.symptoms}</div>
        <div class="history-conditions">
          ${h.result.possible_conditions.map(c => `<span class="tag" style="font-size:0.75rem;">${c}</span>`).join('')}
        </div>
      </div>
    `).join('');
  } catch (err) {
    console.error(err);
  }
}

// ── Enter key support ─────────────────────────────────────────────────────────
document.getElementById('symptomsInput').addEventListener('keydown', e => {
  if (e.key === 'Enter' && e.ctrlKey) analyzeSymptoms();
});
