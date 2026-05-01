// ==================== Smart Agriculture JS ====================

// Language management
const LANG_KEY = 'agri_language';

function setLanguage(lang) {
  localStorage.setItem(LANG_KEY, lang);
  document.querySelectorAll('.lang-btn').forEach(btn => {
    btn.classList.toggle('active', btn.dataset.lang === lang);
  });
  fetch(`/auth/profile`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ language: lang })
  }).catch(() => {});
}

// Range input display
function initRangeInputs() {
  document.querySelectorAll('input[type=range]').forEach(input => {
    const display = document.querySelector(`[data-range="${input.id}"]`);
    if (display) {
      display.textContent = input.value;
      input.addEventListener('input', () => { display.textContent = input.value; });
    }
  });
}

// ==================== SOIL ANALYSIS ====================
async function submitSoilAnalysis(e) {
  e.preventDefault();
  const form = e.target;
  const btn = form.querySelector('button[type=submit]');
  const resultBox = document.getElementById('soil-result');

  btn.disabled = true;
  btn.innerHTML = '<span class="spinner" style="width:18px;height:18px;border-width:2px;display:inline-block;"></span> Analyzing...';

  const data = {
    ph: document.getElementById('ph').value,
    moisture: document.getElementById('moisture').value,
    nitrogen: document.getElementById('nitrogen').value,
    phosphorus: document.getElementById('phosphorus').value,
    potassium: document.getElementById('potassium').value
  };

  try {
    const res = await fetch('/soil/analyze', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    });
    const result = await res.json();
    renderSoilResult(result);
    resultBox.classList.remove('hidden');
    resultBox.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
  } catch (err) {
    showAlert('Error: ' + err.message, 'error');
  } finally {
    btn.disabled = false;
    btn.innerHTML = '🔍 Analyze Soil';
  }
}

function renderSoilResult(r) {
  const qualityColor = { Excellent: '#2D6A4F', Good: '#40916C', Average: '#D4A853', Poor: '#e74c3c' };
  const html = `
    <div class="result-title">📊 Soil Analysis Report</div>
    <div style="display:flex;gap:1rem;flex-wrap:wrap;margin-bottom:1rem;">
      <div style="flex:1;min-width:160px;">
        <div style="font-size:0.8rem;color:var(--text-light);text-transform:uppercase;letter-spacing:.5px">Quality</div>
        <div style="font-size:1.6rem;font-weight:700;font-family:'Playfair Display',serif;color:${qualityColor[r.quality] || '#2D6A4F'}">${r.quality}</div>
      </div>
      <div style="flex:1;min-width:160px;">
        <div style="font-size:0.8rem;color:var(--text-light);text-transform:uppercase;letter-spacing:.5px">pH Category</div>
        <div style="font-size:1.1rem;font-weight:600;color:var(--soil)">${r.ph_category}</div>
      </div>
      <div style="flex:2;min-width:200px;">
        <div style="font-size:0.8rem;color:var(--text-light);text-transform:uppercase;letter-spacing:.5px;margin-bottom:.4rem">Soil Score</div>
        <div class="score-meter"><div class="score-fill" style="width:${r.score}%"></div></div>
        <div style="font-size:0.85rem;color:var(--text-mid)">${r.score}/100</div>
      </div>
    </div>
    <div style="margin-bottom:1rem;">
      <div style="font-size:0.85rem;font-weight:600;color:var(--text-mid);margin-bottom:.5rem">🌾 Recommended Crops</div>
      ${(r.recommended_crops || []).map(c => `<span class="crop-tag">${c}</span>`).join('')}
    </div>
    ${r.issues && r.issues.length ? `
      <div style="margin-bottom:.75rem;">
        <div style="font-size:0.85rem;font-weight:600;color:#92400E;margin-bottom:.4rem">⚠️ Issues Found</div>
        ${r.issues.map(i => `<div style="font-size:0.88rem;color:#92400E">• ${i}</div>`).join('')}
      </div>
      <div>
        <div style="font-size:0.85rem;font-weight:600;color:var(--leaf);margin-bottom:.4rem">💡 Suggestions</div>
        ${(r.suggestions || []).map(s => `<div style="font-size:0.88rem;color:var(--text-mid)">• ${s}</div>`).join('')}
      </div>
    ` : '<div style="color:var(--leaf);font-weight:600">✅ Soil conditions are optimal!</div>'}
  `;
  document.getElementById('soil-result').innerHTML = html;
}

// ==================== PRICE PREDICTION ====================
async function submitPricePrediction(e) {
  e.preventDefault();
  const btn = e.target.querySelector('button[type=submit]');
  btn.disabled = true;
  btn.textContent = '⏳ Predicting...';

  const data = {
    crop_name: document.getElementById('crop_name').value,
    state: document.getElementById('state').value,
    market: document.getElementById('market').value,
    month: document.getElementById('month').value
  };

  try {
    const res = await fetch('/price/predict', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    });
    const result = await res.json();
    renderPriceResult(result);
    document.getElementById('price-result').classList.remove('hidden');
    document.getElementById('price-result').scrollIntoView({ behavior: 'smooth', block: 'nearest' });
  } catch (err) {
    showAlert('Prediction failed: ' + err.message, 'error');
  } finally {
    btn.disabled = false;
    btn.textContent = '📈 Predict Price';
  }
}

function renderPriceResult(r) {
  const trendIcon = r.trend === 'Rising' ? '📈' : '📉';
  const recColor = r.recommendation.includes('Good') ? 'var(--leaf)' : r.recommendation.includes('Hold') ? 'var(--wheat)' : 'var(--text-mid)';
  const html = `
    <div class="result-title">💰 Price Prediction — ${r.crop}</div>
    <div style="display:flex;gap:1rem;flex-wrap:wrap;margin-bottom:1rem;align-items:center">
      <div>
        <div style="font-size:0.8rem;color:var(--text-light);text-transform:uppercase;letter-spacing:.5px">Predicted Price</div>
        <div style="font-size:2.5rem;font-weight:700;font-family:'Playfair Display',serif;color:var(--soil)">₹${r.price.toLocaleString('en-IN', {maximumFractionDigits:0})}</div>
        <div style="font-size:0.85rem;color:var(--text-light)">${r.unit}</div>
      </div>
      <div style="flex:1;padding-left:1rem;border-left:2px solid #E0DDD5">
        <div style="margin-bottom:.5rem">${trendIcon} <strong>Trend:</strong> ${r.trend}</div>
        <div style="font-size:0.9rem;color:${recColor};font-weight:600">${r.recommendation}</div>
      </div>
    </div>
    <div style="font-size:0.85rem;color:var(--text-light)">📅 Month: ${r.month} &nbsp;|&nbsp; 📍 ${r.state || 'All India'}</div>
  `;
  document.getElementById('price-result').innerHTML = html;
}

// ==================== DISEASE DETECTION ====================
function initUploadArea() {
  const area = document.getElementById('upload-area');
  const input = document.getElementById('image-input');
  const preview = document.getElementById('img-preview');
  if (!area || !input) return;

  area.addEventListener('click', () => input.click());
  area.addEventListener('dragover', e => { e.preventDefault(); area.style.borderColor = 'var(--leaf)'; });
  area.addEventListener('dragleave', () => area.style.borderColor = '');
  area.addEventListener('drop', e => {
    e.preventDefault();
    input.files = e.dataTransfer.files;
    showPreview(input.files[0]);
  });
  input.addEventListener('change', () => showPreview(input.files[0]));

  function showPreview(file) {
    if (!file || !preview) return;
    const reader = new FileReader();
    reader.onload = e => {
      preview.src = e.target.result;
      preview.style.display = 'block';
      area.querySelector('.upload-placeholder').style.display = 'none';
    };
    reader.readAsDataURL(file);
  }
}

async function submitDiseaseDetection(e) {
  e.preventDefault();
  const btn = e.target.querySelector('button[type=submit]');
  const imageInput = document.getElementById('image-input');
  if (!imageInput.files[0]) {
    showAlert('Please upload a crop image', 'error');
    return;
  }

  btn.disabled = true;
  btn.textContent = '🔍 Detecting...';

  const formData = new FormData();
  formData.append('image', imageInput.files[0]);
  formData.append('crop_name', document.getElementById('crop_select').value);

  try {
    const res = await fetch('/disease/detect', { method: 'POST', body: formData });
    const result = await res.json();
    renderDiseaseResult(result);
    document.getElementById('disease-result').classList.remove('hidden');
    document.getElementById('disease-result').scrollIntoView({ behavior: 'smooth', block: 'nearest' });
  } catch (err) {
    showAlert('Detection failed: ' + err.message, 'error');
  } finally {
    btn.disabled = false;
    btn.textContent = '🔬 Detect Disease';
  }
}

function renderDiseaseResult(r) {
  const sevClass = { None: 'badge-none', Mild: 'badge-low', Moderate: 'badge-moderate', Severe: 'badge-severe' };
  const isHealthy = r.disease === 'No Disease Detected' || r.disease === 'Healthy';
  const html = `
    <div class="result-title">${isHealthy ? '✅' : '🦠'} Disease Detection Result</div>
    <div style="display:flex;gap:1rem;flex-wrap:wrap;margin-bottom:1rem">
      <div style="flex:1">
        <div style="font-size:0.8rem;color:var(--text-light);text-transform:uppercase;letter-spacing:.5px">Diagnosis</div>
        <div style="font-size:1.4rem;font-weight:700;font-family:'Playfair Display',serif;color:${isHealthy ? 'var(--leaf)' : 'var(--soil)'}">${r.disease}</div>
        <div style="margin-top:.3rem"><span class="badge ${sevClass[r.severity] || 'badge-moderate'}">${r.severity} Severity</span></div>
      </div>
      <div style="flex:1">
        <div style="font-size:0.8rem;color:var(--text-light);text-transform:uppercase;letter-spacing:.5px">Confidence</div>
        <div style="font-size:1.4rem;font-weight:700;color:var(--wheat)">${r.confidence}%</div>
        <div class="score-meter" style="margin-top:.5rem"><div class="score-fill" style="width:${r.confidence}%"></div></div>
      </div>
    </div>
    ${!isHealthy ? `
      <div style="background:var(--mist);padding:1rem;border-radius:8px;border-left:4px solid var(--leaf-bright)">
        <div style="font-size:0.85rem;font-weight:700;color:var(--leaf);margin-bottom:.5rem">💊 Treatment & Solution</div>
        <div style="font-size:0.92rem;color:var(--text-mid);line-height:1.7">${r.solution}</div>
      </div>
    ` : '<div style="color:var(--leaf);font-size:1rem">Your crop appears healthy! Keep up good practices.</div>'}
  `;
  document.getElementById('disease-result').innerHTML = html;
}

// ==================== STORAGE ====================
async function loadStorageInfo(crop) {
  document.querySelectorAll('.crop-btn').forEach(b => b.classList.toggle('active', b.dataset.crop === crop));
  const box = document.getElementById('storage-details');
  box.innerHTML = '<div class="spinner"></div>';

  try {
    const res = await fetch(`/storage/info?crop=${crop}`);
    const data = await res.json();
    box.innerHTML = `
      <div class="result-title">🌾 ${data.name} — Storage Guide</div>
      <div class="grid-2" style="margin-bottom:1rem">
        <div><span style="font-size:0.8rem;color:var(--text-light);text-transform:uppercase;letter-spacing:.5px">Temperature</span><div style="font-size:1.1rem;font-weight:600">🌡️ ${data.temperature}</div></div>
        <div><span style="font-size:0.8rem;color:var(--text-light);text-transform:uppercase;letter-spacing:.5px">Humidity</span><div style="font-size:1.1rem;font-weight:600">💧 ${data.humidity}</div></div>
        <div><span style="font-size:0.8rem;color:var(--text-light);text-transform:uppercase;letter-spacing:.5px">Storage Duration</span><div style="font-size:1.1rem;font-weight:600">📅 ${data.duration}</div></div>
        <div><span style="font-size:0.8rem;color:var(--text-light);text-transform:uppercase;letter-spacing:.5px">Method</span><div style="font-size:0.9rem;color:var(--text-mid)">${data.method}</div></div>
      </div>
      <div style="background:var(--mist);padding:1rem;border-radius:8px">
        <div style="font-weight:700;color:var(--leaf);margin-bottom:.6rem">💡 Best Practices</div>
        ${data.tips.map(t => `<div style="font-size:0.88rem;color:var(--text-mid);margin-bottom:.3rem">✓ ${t}</div>`).join('')}
      </div>
    `;
  } catch (err) {
    box.innerHTML = '<div class="alert alert-error">Failed to load storage info</div>';
  }
}

// ==================== LAND RECORDS ====================
async function addLandRecord(e) {
  e.preventDefault();
  const btn = e.target.querySelector('button[type=submit]');
  btn.disabled = true;
  btn.textContent = 'Saving...';

  const data = {
    area: document.getElementById('area').value,
    location: document.getElementById('location').value,
    soil_type: document.getElementById('soil_type').value,
    crop_grown: document.getElementById('crop_grown').value,
    notes: document.getElementById('notes').value
  };

  try {
    const res = await fetch('/land/add', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    });
    const result = await res.json();
    if (result.land_id) {
      showAlert('Land record added successfully!', 'success');
      e.target.reset();
      loadLandRecords();
    }
  } catch (err) {
    showAlert('Failed to save: ' + err.message, 'error');
  } finally {
    btn.disabled = false;
    btn.textContent = '➕ Add Record';
  }
}

async function loadLandRecords() {
  try {
    const res = await fetch('/land/list');
    const records = await res.json();
    const tbody = document.getElementById('land-table-body');
    if (!tbody) return;
    tbody.innerHTML = records.length ? records.map(r => `
      <tr>
        <td>${r.location}</td>
        <td>${r.area} acres</td>
        <td>${r.soil_type || '—'}</td>
        <td>${r.crop_grown || '—'}</td>
        <td>${r.created_at}</td>
        <td>
          <button class="btn btn-danger btn-sm" onclick="deleteLand(${r.land_id})">Delete</button>
        </td>
      </tr>
    `).join('') : '<tr><td colspan="6" style="text-align:center;color:var(--text-light);padding:2rem">No land records yet.</td></tr>';
  } catch {}
}

async function deleteLand(id) {
  if (!confirm('Delete this land record?')) return;
  await fetch(`/land/delete/${id}`, { method: 'DELETE' });
  loadLandRecords();
}

// ==================== HELPERS ====================
function showAlert(msg, type = 'info') {
  const icons = { success: '✅', error: '❌', info: 'ℹ️' };
  const el = document.createElement('div');
  el.className = `alert alert-${type}`;
  el.innerHTML = `${icons[type] || ''} ${msg}`;
  document.querySelector('.page-wrapper, main, .auth-right')?.prepend(el);
  setTimeout(() => el.remove(), 4000);
}

// ==================== INIT ====================
document.addEventListener('DOMContentLoaded', () => {
  initRangeInputs();
  initUploadArea();

  // Bind forms
  document.getElementById('soil-form')?.addEventListener('submit', submitSoilAnalysis);
  document.getElementById('price-form')?.addEventListener('submit', submitPricePrediction);
  document.getElementById('disease-form')?.addEventListener('submit', submitDiseaseDetection);
  document.getElementById('land-form')?.addEventListener('submit', addLandRecord);

  // Load land records if on that page
  if (document.getElementById('land-table-body')) loadLandRecords();

  // Load default storage info
  if (document.getElementById('storage-details')) loadStorageInfo('wheat');

  // Language buttons
  document.querySelectorAll('.lang-btn').forEach(btn => {
    btn.addEventListener('click', () => setLanguage(btn.dataset.lang));
  });
});
