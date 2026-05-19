// ── TAB SWITCHING ────────────────────────────────────────────────────────────
document.querySelectorAll('.tab-btn').forEach(btn => {
  btn.addEventListener('click', () => {
    document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
    document.querySelectorAll('.tab-content').forEach(c => c.style.display = 'none');
    btn.classList.add('active');
    document.getElementById('tab-' + btn.dataset.tab).style.display = 'block';
  });
});

// ── STATES / CITIES ──────────────────────────────────────────────────────────
async function loadStates() {
  const res = await fetch('/registry/states');
  const states = await res.json();
  const sel = document.getElementById('f-state');
  states.forEach(s => {
    const opt = document.createElement('option');
    opt.value = opt.textContent = s;
    sel.appendChild(opt);
  });
}

async function loadCities() {
  const state = document.getElementById('f-state').value;
  const res = await fetch('/registry/cities?state=' + encodeURIComponent(state));
  const cities = await res.json();
  const sel = document.getElementById('f-city');
  sel.innerHTML = '<option value="">All Cities</option>';
  cities.forEach(c => {
    const opt = document.createElement('option');
    opt.value = opt.textContent = c;
    sel.appendChild(opt);
  });
}

// ── SEARCH ───────────────────────────────────────────────────────────────────
let currentPage = 1;

async function searchRegistry(page = 1) {
  currentPage = page;
  const params = new URLSearchParams({
    state:      document.getElementById('f-state').value,
    city:       document.getElementById('f-city').value,
    khata_no:   document.getElementById('f-khata').value,
    khesra_no:  document.getElementById('f-khesra').value,
    owner_name: document.getElementById('f-owner').value,
    land_type:  document.getElementById('f-landtype').value,
    page,
    per_page: 15,
  });

  const res  = await fetch('/registry/search?' + params);
  const data = await res.json();

  const countEl = document.getElementById('result-count');
  const tbody   = document.getElementById('results-body');
  const noRes   = document.getElementById('no-results');
  const resDiv  = document.getElementById('search-results');

  countEl.textContent = data.total + ' records found';

  if (data.total === 0) {
    resDiv.style.display = 'none';
    noRes.style.display  = 'block';
    return;
  }

  noRes.style.display = 'none';
  resDiv.style.display = 'block';
  tbody.innerHTML = '';

  data.records.forEach(r => {
    const statusClass =
      r.land_status === 'Cultivated' ? 'badge-success' :
      r.land_status === 'Disputed'   ? 'badge-danger'  :
      r.land_status === 'Fallow'     ? 'badge-warning' : 'badge-default';
    tbody.innerHTML += `
      <tr>
        <td><code class="code-green">${r.khata_no}</code></td>
        <td><code class="code-yellow">${r.khesra_no}</code></td>
        <td style="font-size:.82rem;color:var(--text-mid)">${r.survey_no}</td>
        <td style="font-weight:500">${r.owner_name}</td>
        <td style="font-size:.82rem">${r.state}</td>
        <td style="font-size:.82rem">${r.city}</td>
        <td>${r.area} ac</td>
        <td style="font-size:.82rem">${r.soil_type}</td>
        <td><span class="badge badge-info">${r.land_type}</span></td>
        <td><span class="badge ${statusClass}">${r.land_status}</span></td>
        <td><button class="btn btn-sm btn-secondary"
              onclick="showDetail(${r.id})">View</button></td>
      </tr>`;
  });

  renderPagination(data.total_pages, page);
}

function renderPagination(totalPages, current) {
  const el = document.getElementById('pagination');
  if (totalPages <= 1) { el.innerHTML = ''; return; }
  let html = '';
  const prev = current > 1 ? current - 1 : 1;
  const next = current < totalPages ? current + 1 : totalPages;
  html += `<button class="page-btn" onclick="searchRegistry(${prev})" ${current===1?'disabled':''}>‹</button>`;
  for (let p = Math.max(1, current-3); p <= Math.min(totalPages, current+3); p++) {
    html += `<button class="page-btn${p===current?' active':''}" onclick="searchRegistry(${p})">${p}</button>`;
  }
  html += `<button class="page-btn" onclick="searchRegistry(${next})" ${current===totalPages?'disabled':''}>›</button>`;
  html += `<span class="page-info">Page ${current} / ${totalPages}</span>`;
  el.innerHTML = html;
}

function clearSearch() {
  ['f-state','f-city','f-khata','f-khesra','f-owner','f-landtype'].forEach(id => {
    const el = document.getElementById(id);
    if (el.tagName === 'SELECT') el.value = '';
    else el.value = '';
  });
  document.getElementById('result-count').textContent = '';
  document.getElementById('search-results').style.display = 'none';
  document.getElementById('no-results').style.display = 'none';
}

// ── RECORD DETAIL MODAL ──────────────────────────────────────────────────────
async function showDetail(id) {
  const res  = await fetch('/registry/detail/' + id);
  const r    = await res.json();
  const body = document.getElementById('modal-body');
  body.innerHTML = `
    <div class="detail-grid">
      ${detailRow('Khata No',  `<code class="code-green">${r.khata_no}</code>`)}
      ${detailRow('Khesra No', `<code class="code-yellow">${r.khesra_no}</code>`)}
      ${detailRow('Survey No', r.survey_no)}
      ${detailRow('Owner',     r.owner_name)}
      ${detailRow('State',     r.state)}
      ${detailRow('City',      r.city)}
      ${detailRow('Area',      r.area + ' acres')}
      ${detailRow('Soil Type', r.soil_type)}
      ${detailRow('Land Type', r.land_type)}
      ${detailRow('Status',    r.land_status)}
      ${detailRow('Water',     r.water_source)}
      ${detailRow('Crop History', r.crop_history)}
      ${detailRow('Reg. Year', r.registered_year)}
      ${detailRow('Soil pH',   r.ph_value)}
    </div>
    <div class="ph-bar-section">
      <strong>Soil pH Analysis: ${r.ph_value}</strong>
      <div class="score-meter" style="margin-top:.5rem">
        <div class="score-fill" style="width:${(r.ph_value/14)*100}%"></div>
      </div>
      <small style="color:var(--text-light)">
        ${r.ph_value < 6 ? 'Acidic — Add lime to improve' :
          r.ph_value > 7.5 ? 'Alkaline — Add sulfur or organic matter' :
          'Near neutral pH — Good for most crops'}
      </small>
    </div>`;
  document.getElementById('detail-modal').style.display = 'flex';
}

function detailRow(label, val) {
  return `<div class="detail-item"><div class="detail-label">${label}</div><div class="detail-val">${val}</div></div>`;
}

function closeModal() {
  document.getElementById('detail-modal').style.display = 'none';
}

// ── AI LAND IMAGE ANALYSIS ───────────────────────────────────────────────────
function previewImage(input) {
  const file = input.files[0];
  if (!file) return;
  const reader = new FileReader();
  reader.onload = e => {
    document.getElementById('upload-placeholder').style.display = 'none';
    const img = document.getElementById('preview-img');
    img.src = e.target.result;
    img.style.display = 'block';
    document.getElementById('analyze-btn').disabled = false;
  };
  reader.readAsDataURL(file);
}

async function analyzeLandImage() {
  const input = document.getElementById('land-img-input');
  const btn   = document.getElementById('analyze-btn');
  const errEl = document.getElementById('analysis-error');
  if (!input.files[0]) return;

  btn.disabled = true;
  btn.innerHTML = '<span class="spinner-sm"></span> Analyzing...';
  errEl.style.display = 'none';

  const formData = new FormData();
  formData.append('image', input.files[0]);

  try {
    const res  = await fetch('/land/analyze-image', { method: 'POST', body: formData });
    const data = await res.json();

    if (data.error) {
      errEl.textContent = data.error;
      errEl.style.display = 'block';
      return;
    }

    renderAnalysisResult(data);
    document.getElementById('analysis-result').style.display = 'block';
    document.getElementById('analysis-result').scrollIntoView({ behavior: 'smooth' });

  } catch (err) {
    errEl.textContent = 'Analysis failed. Please try again.';
    errEl.style.display = 'block';
  } finally {
    btn.disabled = false;
    btn.innerHTML = '🔬 Analyze Land Image';
  }
}

function renderAnalysisResult(r) {
  const qColors = { Excellent:'#2E7D32', Good:'#43A047', Average:'#F57F17', Poor:'#C62828' };
  const color = qColors[r.quality] || '#43A047';

  const metricBar = (label, val, max, unit='%') => `
    <div class="analysis-metric">
      <div style="display:flex;justify-content:space-between;font-size:.82rem;margin-bottom:.3rem">
        <span style="color:var(--text-mid);font-weight:600">${label}</span>
        <strong style="color:var(--leaf)">${val}${unit}</strong>
      </div>
      <div class="score-meter"><div class="score-fill" style="width:${(val/max)*100}%"></div></div>
    </div>`;

  document.getElementById('analysis-body').innerHTML = `
    <div style="background:#E8F5E9;border-radius:8px;padding:1rem;margin-bottom:1.25rem;display:flex;align-items:center;gap:1rem;flex-wrap:wrap">
      <div>
        <div style="font-size:.78rem;color:var(--text-mid);font-weight:600;text-transform:uppercase">Overall Quality</div>
        <div style="font-size:2rem;font-weight:700;color:${color}">${r.quality}</div>
      </div>
      <div style="flex:1;min-width:180px">
        <div style="font-size:.82rem;font-weight:600;color:var(--text-mid);margin-bottom:.3rem">Health Score: ${r.healthScore}/100</div>
        <div class="score-meter" style="height:12px"><div class="score-fill" style="width:${r.healthScore}%"></div></div>
      </div>
      ${r.texture ? `<span class="badge badge-info">${r.texture} soil</span>` : ''}
      ${r.soilColor ? `<span class="badge">${r.soilColor}</span>` : ''}
    </div>

    <div class="analysis-metrics">
      ${metricBar('pH Level', r.ph, 14, '')}
      ${metricBar('Nitrogen (N)', r.nitrogen, 100)}
      ${metricBar('Phosphorus (P)', r.phosphorus, 100)}
      ${metricBar('Potassium (K)', r.potassium, 100)}
      ${metricBar('Organic Matter', r.organicMatter, 10)}
      ${metricBar('Moisture', r.moisture, 100)}
    </div>

    ${r.summary ? `<div style="background:#F9FBF9;border-radius:8px;padding:1rem;margin-top:1rem">
      <div style="font-weight:700;margin-bottom:.4rem;color:var(--leaf)">📝 AI Assessment</div>
      <p style="font-size:.9rem;color:var(--text-mid);line-height:1.6">${r.summary}</p>
    </div>` : ''}

    ${r.suitableCrops?.length ? `<div style="background:#E8F5E9;border-radius:8px;padding:1rem;margin-top:1rem">
      <div style="font-weight:700;margin-bottom:.5rem;color:var(--leaf)">🌾 Suitable Crops</div>
      <div style="display:flex;flex-wrap:wrap;gap:.5rem">
        ${r.suitableCrops.map(c=>`<span class="badge badge-success">${c}</span>`).join('')}
      </div>
    </div>` : ''}

    ${r.fertilizer ? `<div style="background:#FFF9C4;border-radius:8px;padding:1rem;margin-top:1rem">
      <div style="font-weight:700;margin-bottom:.3rem;color:#F57F17">🧪 Fertilizer</div>
      <p style="font-size:.88rem;color:var(--text-mid)">${r.fertilizer}</p>
    </div>` : ''}

    ${r.irrigation ? `<div style="background:#E3F2FD;border-radius:8px;padding:1rem;margin-top:1rem">
      <div style="font-weight:700;margin-bottom:.3rem;color:#1565C0">💧 Irrigation</div>
      <p style="font-size:.88rem;color:var(--text-mid)">${r.irrigation}</p>
    </div>` : ''}

    ${r.issues?.length ? `<div style="background:#FFEBEE;border-radius:8px;padding:1rem;margin-top:1rem">
      <div style="font-weight:700;margin-bottom:.4rem;color:#C62828">⚠️ Issues</div>
      <ul style="padding-left:1.25rem;font-size:.88rem;color:var(--text-mid)">
        ${r.issues.map(i=>`<li>${i}</li>`).join('')}
      </ul>
    </div>` : ''}

    ${r.note ? `<div style="background:#F5F5F5;border-radius:8px;padding:.75rem;margin-top:1rem;font-size:.82rem;color:var(--text-mid)">ℹ️ ${r.note}</div>` : ''}
  `;
}

// Init: load states dropdown on page load
loadStates();