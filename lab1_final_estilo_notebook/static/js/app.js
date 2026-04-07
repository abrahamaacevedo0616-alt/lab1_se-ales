// ═══════════════════════════════════════════════════════════════════════════
//  DOM references
// ═══════════════════════════════════════════════════════════════════════════
const catalog = window.__SIGNAL_CATALOG__;
const allowed  = window.__ALLOWED__;

const domainSelect    = document.getElementById('domain-select');
const signalSelect    = document.getElementById('signal-select');
const loadBtn         = document.getElementById('load-signal-btn');
const transformBtn    = document.getElementById('transform-btn');
const titleEl         = document.getElementById('signal-title');
const descriptionEl   = document.getElementById('signal-description');
const baseExpressionEl  = document.getElementById('base-expression');
const finalExpressionEl = document.getElementById('final-expression');
const transformNoteEl   = document.getElementById('transform-note');
const canvas  = document.getElementById('plot-canvas');
const ctx     = canvas.getContext('2d');
const methodSelect    = document.getElementById('method-select');
const scaleSignSelect = document.getElementById('scale-sign-select');
const scaleMagSelect  = document.getElementById('scale-mag-select');
const shiftSignSelect = document.getElementById('shift-sign-select');
const shiftMagSelect  = document.getElementById('shift-mag-select');
const interpModeSelect = document.getElementById('interp-mode-select');

const step1Canvas = document.getElementById('step-1-canvas');
const step2Canvas = document.getElementById('step-2-canvas');
const step1Ctx    = step1Canvas.getContext('2d');
const step2Ctx    = step2Canvas.getContext('2d');
const step1Title      = document.getElementById('step-1-title');
const step2Title      = document.getElementById('step-2-title');
const step1Expression = document.getElementById('step-1-expression');
const step2Expression = document.getElementById('step-2-expression');

const interpSignalSelect  = document.getElementById('interp-signal-select');
const interpFactorSelect  = document.getElementById('interp-factor-select');
const interpTypeSelect    = document.getElementById('interp-type-select');
const interpolateBtn      = document.getElementById('interpolate-btn');
const interpExpression    = document.getElementById('interp-expression');
const interpNote          = document.getElementById('interp-note');
const interpStep1Title      = document.getElementById('interp-step-1-title');
const interpStep2Title      = document.getElementById('interp-step-2-title');
const interpStep1Expression = document.getElementById('interp-step-1-expression');
const interpStep2Expression = document.getElementById('interp-step-2-expression');
const interpStep1Canvas = document.getElementById('interp-step-1-canvas');
const interpStep2Canvas = document.getElementById('interp-step-2-canvas');
const interpStep1Ctx    = interpStep1Canvas.getContext('2d');
const interpStep2Ctx    = interpStep2Canvas.getContext('2d');

const continuousOpSignalSelect   = document.getElementById('continuous-op-signal-select');
const continuousOpBtn            = document.getElementById('continuous-op-btn');
const continuousOpExpression     = document.getElementById('continuous-op-expression');
const continuousOpNote           = document.getElementById('continuous-op-note');
const continuousOpStep1Title      = document.getElementById('continuous-op-step-1-title');
const continuousOpStep2Title      = document.getElementById('continuous-op-step-2-title');
const continuousOpStep1Expression = document.getElementById('continuous-op-step-1-expression');
const continuousOpStep2Expression = document.getElementById('continuous-op-step-2-expression');
const continuousOpStep1Canvas = document.getElementById('continuous-op-step-1-canvas');
const continuousOpStep2Canvas = document.getElementById('continuous-op-step-2-canvas');
const continuousOpFinalCanvas = document.getElementById('continuous-op-final-canvas');
const continuousOpStep1Ctx = continuousOpStep1Canvas.getContext('2d');
const continuousOpStep2Ctx = continuousOpStep2Canvas.getContext('2d');
const continuousOpFinalCtx = continuousOpFinalCanvas.getContext('2d');

const file1Input           = document.getElementById('file1-input');
const file2Input           = document.getElementById('file2-input');
const fileInterpModeSelect = document.getElementById('file-interp-mode-select');
const fileSumBtn           = document.getElementById('file-sum-btn');
const fileSumExpression    = document.getElementById('file-sum-expression');
const fileSumNote          = document.getElementById('file-sum-note');
const fileOriginalsCanvas   = document.getElementById('file-originals-canvas');
const fileOversampledCanvas = document.getElementById('file-oversampled-canvas');
const fileSumCanvas         = document.getElementById('file-sum-canvas');
const fileOriginalsCtx   = fileOriginalsCanvas.getContext('2d');
const fileOversampledCtx = fileOversampledCanvas.getContext('2d');
const fileSumCtx         = fileSumCanvas.getContext('2d');

// ═══════════════════════════════════════════════════════════════════════════
//  Theme palette
// ═══════════════════════════════════════════════════════════════════════════
const CANVAS_BG       = '#060c18';
const GRID_COLOR      = 'rgba(28, 65, 110, 0.40)';
const AXIS_COLOR      = 'rgba(70, 140, 200, 0.80)';
const TICK_COLOR      = 'rgba(70, 140, 200, 0.50)';
const LABEL_COLOR     = '#5a90c8';
const ZERO_LINE_COLOR = 'rgba(60, 120, 180, 0.35)';

const COLOR_CONTINUOUS = '#00d4ff';   // cyan
const COLOR_STEM       = '#ff9500';   // orange
const COLOR_DOT        = '#ffcc44';   // amber
const MULTI_COLORS     = ['#00d4ff', '#ff9500', '#44ff88'];

// ═══════════════════════════════════════════════════════════════════════════
//  Canvas utilities
// ═══════════════════════════════════════════════════════════════════════════
function clearCanvas(ctxLocal, canvasLocal) {
  ctxLocal.fillStyle = CANVAS_BG;
  ctxLocal.fillRect(0, 0, canvasLocal.width, canvasLocal.height);
}

function plotBounds(canvasLocal) {
  return { left: 58, right: canvasLocal.width - 26, top: 22, bottom: canvasLocal.height - 34 };
}

/** Map a data value to pixel space (x axis). */
function toPixX(v, vMin, vMax, pLeft, pRight) {
  if (vMax === vMin) return (pLeft + pRight) / 2;
  return pLeft + (v - vMin) / (vMax - vMin) * (pRight - pLeft);
}

/** Map a data value to pixel space (y axis, inverted). */
function toPixY(v, vMin, vMax, pBottom, pTop) {
  if (vMax === vMin) return (pBottom + pTop) / 2;
  return pBottom + (v - vMin) / (vMax - vMin) * (pTop - pBottom);
}

function niceStep(range, maxTicks) {
  if (range === 0) return 1;
  const rough = range / maxTicks;
  const mag   = Math.pow(10, Math.floor(Math.log10(rough)));
  const norm  = rough / mag;
  let s;
  if      (norm < 1.5) s = 1;
  else if (norm < 3.5) s = 2;
  else if (norm < 7.5) s = 5;
  else                 s = 10;
  return s * mag;
}

function generateTicks(min, max, maxTicks = 10) {
  const step  = niceStep(max - min, maxTicks);
  const start = Math.ceil(min / step - 1e-9) * step;
  const ticks = [];
  for (let v = start; v <= max + 1e-9; v += step) {
    ticks.push(parseFloat(v.toPrecision(10)));
  }
  return ticks;
}

function fmtTick(v) {
  if (Math.abs(v) < 1e-9)  return '0';
  if (Number.isInteger(v))  return String(v);
  // try nice fractions
  for (const d of [2, 3, 4, 5, 8]) {
    const n = v * d;
    if (Math.abs(Math.round(n) - n) < 1e-6) return `${Math.round(n)}/${d}`;
  }
  return parseFloat(v.toPrecision(3)).toString();
}

function drawArrow(ctxLocal, x1, y1, x2, y2, color, sz = 7) {
  const ang = Math.atan2(y2 - y1, x2 - x1);
  ctxLocal.strokeStyle = color;
  ctxLocal.lineWidth   = 1.3;
  ctxLocal.beginPath();
  ctxLocal.moveTo(x1, y1);
  ctxLocal.lineTo(x2, y2);
  ctxLocal.stroke();
  ctxLocal.fillStyle = color;
  ctxLocal.beginPath();
  ctxLocal.moveTo(x2, y2);
  ctxLocal.lineTo(x2 - sz * Math.cos(ang - Math.PI / 6), y2 - sz * Math.sin(ang - Math.PI / 6));
  ctxLocal.lineTo(x2 - sz * Math.cos(ang + Math.PI / 6), y2 - sz * Math.sin(ang + Math.PI / 6));
  ctxLocal.closePath();
  ctxLocal.fill();
}

/**
 * Draw a full scientific axis system:
 *   - Dotted grid at tick positions
 *   - Zero lines (brighter)
 *   - Axes with arrowheads crossing at (0, 0)
 *   - Tick marks & numeric labels
 *   - Axis letter labels
 */
function drawAxesGrid(ctxLocal, bounds, xMin, xMax, yMin, yMax, xLabel) {
  const { left, right, top, bottom } = bounds;

  const xTicks = generateTicks(xMin, xMax, 12);
  const yTicks = generateTicks(yMin, yMax, 8);

  // Pixel position of the data origin
  const ox = Math.max(left, Math.min(right,  toPixX(0, xMin, xMax, left, right)));
  const oy = Math.max(top,  Math.min(bottom, toPixY(0, yMin, yMax, bottom, top)));

  // ── Grid ──────────────────────────────────────────────────────────
  ctxLocal.setLineDash([3, 6]);
  ctxLocal.lineWidth = 0.6;
  ctxLocal.strokeStyle = GRID_COLOR;

  xTicks.forEach(v => {
    const px = toPixX(v, xMin, xMax, left, right);
    if (px < left - 1 || px > right + 1) return;
    ctxLocal.beginPath(); ctxLocal.moveTo(px, top); ctxLocal.lineTo(px, bottom); ctxLocal.stroke();
  });
  yTicks.forEach(v => {
    const py = toPixY(v, yMin, yMax, bottom, top);
    if (py < top - 1 || py > bottom + 1) return;
    ctxLocal.beginPath(); ctxLocal.moveTo(left, py); ctxLocal.lineTo(right, py); ctxLocal.stroke();
  });
  ctxLocal.setLineDash([]);

  // ── Zero lines ───────────────────────────────────────────────────
  ctxLocal.strokeStyle = ZERO_LINE_COLOR;
  ctxLocal.lineWidth   = 0.8;
  if (ox >= left && ox <= right) {
    ctxLocal.beginPath(); ctxLocal.moveTo(ox, top); ctxLocal.lineTo(ox, bottom); ctxLocal.stroke();
  }
  if (oy >= top && oy <= bottom) {
    ctxLocal.beginPath(); ctxLocal.moveTo(left, oy); ctxLocal.lineTo(right, oy); ctxLocal.stroke();
  }

  // ── Axes with arrows ─────────────────────────────────────────────
  drawArrow(ctxLocal, left - 2,  oy, right + 18, oy, AXIS_COLOR, 7);
  drawArrow(ctxLocal, ox, bottom + 2,  ox, top - 16, AXIS_COLOR, 7);

  // ── Ticks & labels ───────────────────────────────────────────────
  ctxLocal.font          = '10.5px "Courier New", monospace';
  ctxLocal.fillStyle     = LABEL_COLOR;
  ctxLocal.strokeStyle   = TICK_COLOR;
  ctxLocal.lineWidth     = 1;

  ctxLocal.textAlign     = 'center';
  ctxLocal.textBaseline  = 'top';
  xTicks.forEach(v => {
    const px = toPixX(v, xMin, xMax, left, right);
    if (px < left || px > right) return;
    ctxLocal.beginPath(); ctxLocal.moveTo(px, oy - 4); ctxLocal.lineTo(px, oy + 4); ctxLocal.stroke();
    if (Math.abs(v) > 1e-9) ctxLocal.fillText(fmtTick(v), px, oy + 6);
  });

  ctxLocal.textAlign    = 'right';
  ctxLocal.textBaseline = 'middle';
  yTicks.forEach(v => {
    const py = toPixY(v, yMin, yMax, bottom, top);
    if (py < top || py > bottom) return;
    ctxLocal.beginPath(); ctxLocal.moveTo(ox - 4, py); ctxLocal.lineTo(ox + 4, py); ctxLocal.stroke();
    if (Math.abs(v) > 1e-9) ctxLocal.fillText(fmtTick(v), ox - 7, py);
  });

  // ── Axis letters ─────────────────────────────────────────────────
  ctxLocal.fillStyle    = '#7ab0d8';
  ctxLocal.font         = 'italic 12px "Courier New", monospace';
  ctxLocal.textAlign    = 'left';
  ctxLocal.textBaseline = 'middle';
  ctxLocal.fillText(xLabel, right + 22, oy);
  ctxLocal.textAlign    = 'center';
  ctxLocal.textBaseline = 'bottom';
  ctxLocal.fillText('A', ox, top - 4);
}

// ═══════════════════════════════════════════════════════════════════════════
//  Signal rendering
// ═══════════════════════════════════════════════════════════════════════════
function drawSignalOnCanvas(signal, ctxLocal, canvasLocal) {
  clearCanvas(ctxLocal, canvasLocal);
  const bounds = plotBounds(canvasLocal);

  if (signal.domain === 'continuous') {
    const tMin = Math.min(...signal.t);
    const tMax = Math.max(...signal.t);
    const xMin = Math.min(...signal.x, 0);
    const xMax = Math.max(...signal.x, 0);
    const pad  = (xMax - xMin) * 0.10 || 0.6;

    drawAxesGrid(ctxLocal, bounds, tMin, tMax, xMin - pad, xMax + pad, 't');

    ctxLocal.shadowBlur  = 7;
    ctxLocal.shadowColor = COLOR_CONTINUOUS;
    ctxLocal.strokeStyle = COLOR_CONTINUOUS;
    ctxLocal.lineWidth   = 2;
    ctxLocal.beginPath();
    signal.t.forEach((t, i) => {
      const px = toPixX(t, tMin, tMax, bounds.left, bounds.right);
      const py = toPixY(signal.x[i], xMin - pad, xMax + pad, bounds.bottom, bounds.top);
      i === 0 ? ctxLocal.moveTo(px, py) : ctxLocal.lineTo(px, py);
    });
    ctxLocal.stroke();
    ctxLocal.shadowBlur = 0;

  } else {
    // Discrete
    const nMin  = Math.min(...signal.n);
    const nMax  = Math.max(...signal.n);
    const xMin  = Math.min(...signal.x, 0);
    const xMax  = Math.max(...signal.x, 0);
    const padY  = (xMax - xMin) * 0.12 || 0.6;
    const padN  = Math.max((nMax - nMin) * 0.05, 1);

    drawAxesGrid(ctxLocal, bounds, nMin - padN, nMax + padN, xMin - padY, xMax + padY, 'n');

    const baseline = toPixY(0, xMin - padY, xMax + padY, bounds.bottom, bounds.top);

    signal.n.forEach((n, i) => {
      const px = toPixX(n, nMin - padN, nMax + padN, bounds.left, bounds.right);
      const py = toPixY(signal.x[i], xMin - padY, xMax + padY, bounds.bottom, bounds.top);

      ctxLocal.shadowBlur  = 5;
      ctxLocal.shadowColor = COLOR_STEM;
      ctxLocal.strokeStyle = COLOR_STEM;
      ctxLocal.lineWidth   = 1.8;
      ctxLocal.beginPath();
      ctxLocal.moveTo(px, baseline);
      ctxLocal.lineTo(px, py);
      ctxLocal.stroke();

      ctxLocal.fillStyle = COLOR_DOT;
      ctxLocal.beginPath();
      ctxLocal.arc(px, py, 3, 0, Math.PI * 2);
      ctxLocal.fill();
      ctxLocal.shadowBlur = 0;
    });
  }
}

function drawMultiContinuousSignals(signals, ctxLocal, canvasLocal) {
  clearCanvas(ctxLocal, canvasLocal);
  const bounds = plotBounds(canvasLocal);

  const allT = signals.flatMap(s => s.t);
  const allX = signals.flatMap(s => s.x);
  const tMin = Math.min(...allT);
  const tMax = Math.max(...allT);
  const xMin = Math.min(...allX, 0);
  const xMax = Math.max(...allX, 0);
  const pad  = (xMax - xMin) * 0.10 || 0.6;

  drawAxesGrid(ctxLocal, bounds, tMin, tMax, xMin - pad, xMax + pad, 't');

  signals.forEach((signal, idx) => {
    const color = MULTI_COLORS[idx % MULTI_COLORS.length];
    ctxLocal.shadowBlur  = 6;
    ctxLocal.shadowColor = color;
    ctxLocal.strokeStyle = color;
    ctxLocal.lineWidth   = 1.8;
    ctxLocal.beginPath();
    signal.t.forEach((tVal, i) => {
      const px = toPixX(tVal, tMin, tMax, bounds.left, bounds.right);
      const py = toPixY(signal.x[i], xMin - pad, xMax + pad, bounds.bottom, bounds.top);
      i === 0 ? ctxLocal.moveTo(px, py) : ctxLocal.lineTo(px, py);
    });
    ctxLocal.stroke();
    ctxLocal.shadowBlur = 0;
  });

  // Legend
  signals.forEach((signal, idx) => {
    const color = MULTI_COLORS[idx % MULTI_COLORS.length];
    const ly    = bounds.top + 10 + idx * 18;
    ctxLocal.fillStyle     = color;
    ctxLocal.shadowBlur    = 4;
    ctxLocal.shadowColor   = color;
    ctxLocal.fillRect(bounds.left + 8, ly - 1, 18, 3);
    ctxLocal.shadowBlur    = 0;
    ctxLocal.fillStyle     = '#8ab8d8';
    ctxLocal.font          = '10.5px system-ui, sans-serif';
    ctxLocal.textAlign     = 'left';
    ctxLocal.textBaseline  = 'middle';
    ctxLocal.fillText(signal.title, bounds.left + 32, ly);
  });
}

// ═══════════════════════════════════════════════════════════════════════════
//  Populate dropdowns
// ═══════════════════════════════════════════════════════════════════════════
function populateSignalOptions(domain) {
  signalSelect.innerHTML = '';
  catalog[domain].forEach(signal => {
    const opt = document.createElement('option');
    opt.value = signal.key;
    opt.textContent = signal.title;
    signalSelect.appendChild(opt);
  });
}

function populateInterpolationSignals() {
  if (!interpSignalSelect) return;
  interpSignalSelect.innerHTML = '';
  catalog.discrete.forEach(signal => {
    const opt = document.createElement('option');
    opt.value = signal.key;
    opt.textContent = signal.title;
    interpSignalSelect.appendChild(opt);
  });
}

function populateContinuousOperationSignals() {
  if (!continuousOpSignalSelect) return;
  continuousOpSignalSelect.innerHTML = '';
  catalog.continuous.forEach(signal => {
    const opt = document.createElement('option');
    opt.value = signal.key;
    opt.textContent = signal.title;
    continuousOpSignalSelect.appendChild(opt);
  });
}

function populateTransformOptions(domain) {
  const scaleVals = domain === 'continuous' ? allowed.continuousScale : allowed.discreteScale;
  const shiftVals = domain === 'continuous' ? allowed.continuousShift : allowed.discreteShift;
  scaleMagSelect.innerHTML = '';
  shiftMagSelect.innerHTML = '';
  scaleVals.forEach(v => {
    const opt = document.createElement('option');
    opt.value = v; opt.textContent = v.toString();
    scaleMagSelect.appendChild(opt);
  });
  shiftVals.forEach(v => {
    const opt = document.createElement('option');
    opt.value = v; opt.textContent = v;
    shiftMagSelect.appendChild(opt);
  });
}

function updateInterpolationModeVisibility() {
  const discrete = domainSelect.value === 'discrete';
  interpModeSelect.parentElement.style.display = discrete ? 'flex' : 'none';
}

// ═══════════════════════════════════════════════════════════════════════════
//  API calls
// ═══════════════════════════════════════════════════════════════════════════
async function loadSignal(signalKey) {
  const response = await fetch(`/api/signals/${signalKey}`);
  const signal   = await response.json();
  titleEl.textContent       = signal.title;
  descriptionEl.textContent = signal.description;
  baseExpressionEl.textContent = signal.domain === 'continuous' ? 'x(t)' : 'x[n]';
  drawSignalOnCanvas(signal, ctx, canvas);
}

async function applyTransform() {
  const payload = {
    signal_key:  signalSelect.value,
    domain:      domainSelect.value,
    method:      methodSelect.value,
    scale_sign:  scaleSignSelect.value,
    scale_mag:   scaleMagSelect.value,
    shift_sign:  shiftSignSelect.value,
    shift_mag:   shiftMagSelect.value,
    interp_mode: interpModeSelect.value,
  };
  const response = await fetch('/api/transform', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  });
  const data = await response.json();
  if (!response.ok) { alert(data.error || 'Error al transformar la señal.'); return; }

  finalExpressionEl.textContent = data.final_expression;
  transformNoteEl.textContent   = data.note || '';
  drawSignalOnCanvas(data.final_signal, ctx, canvas);

  const s1 = data.steps[0];
  const s2 = data.steps[1];
  step1Title.textContent      = s1.title;
  step2Title.textContent      = s2.title;
  step1Expression.textContent = s1.expression;
  step2Expression.textContent = s2.expression;
  drawSignalOnCanvas(s1, step1Ctx, step1Canvas);
  drawSignalOnCanvas(s2, step2Ctx, step2Canvas);
}

async function applyInterpolation() {
  if (!interpSignalSelect || !interpSignalSelect.value) return;
  const payload = {
    signal_key: interpSignalSelect.value,
    factor:     interpFactorSelect.value,
    mode:       interpTypeSelect.value,
  };
  const response = await fetch('/api/interpolate', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  });
  const data = await response.json();
  if (!response.ok) { alert(data.error || 'Error al interpolar.'); return; }

  interpExpression.textContent = data.final_expression;
  interpNote.textContent       = data.note || '';

  const s1 = data.steps[0];
  const s2 = data.steps[1];
  interpStep1Title.textContent      = s1.title;
  interpStep2Title.textContent      = s2.title;
  interpStep1Expression.textContent = s1.expression;
  interpStep2Expression.textContent = s2.expression;
  drawSignalOnCanvas(s1, interpStep1Ctx, interpStep1Canvas);
  drawSignalOnCanvas(s2, interpStep2Ctx, interpStep2Canvas);
}

async function applyContinuousOperation() {
  if (!continuousOpSignalSelect || !continuousOpSignalSelect.value) return;
  const payload  = { signal_key: continuousOpSignalSelect.value };
  const response = await fetch('/api/continuous-operation', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  });
  const data = await response.json();
  if (!response.ok) { alert(data.error || 'Error en la operación continua.'); return; }

  continuousOpExpression.textContent = data.final_expression;
  continuousOpNote.textContent       = data.note || '';

  const s1 = data.steps[0];
  const s2 = data.steps[1];
  continuousOpStep1Title.textContent      = s1.title;
  continuousOpStep2Title.textContent      = s2.title;
  continuousOpStep1Expression.textContent = s1.expression;
  continuousOpStep2Expression.textContent = s2.expression;
  drawSignalOnCanvas(s1, continuousOpStep1Ctx, continuousOpStep1Canvas);
  drawSignalOnCanvas(s2, continuousOpStep2Ctx, continuousOpStep2Canvas);
  drawSignalOnCanvas(data.final_signal, continuousOpFinalCtx, continuousOpFinalCanvas);
}

async function processFileSignals() {
  if (!file1Input.files.length || !file2Input.files.length) {
    alert('Debes cargar los dos archivos .txt.');
    return;
  }
  const formData = new FormData();
  formData.append('file1', file1Input.files[0]);
  formData.append('file2', file2Input.files[0]);
  formData.append('mode',  fileInterpModeSelect.value);

  const response = await fetch('/api/file-sum', { method: 'POST', body: formData });
  const data     = await response.json();
  if (!response.ok) { alert(data.error || 'Error al procesar los archivos.'); return; }

  fileSumExpression.textContent = `f_c = ${data.fs_common} Hz,  y(t) = y₁(t) + y₂(t)`;
  fileSumNote.textContent       = data.note || '';
  drawMultiContinuousSignals([data.original_1,   data.original_2],   fileOriginalsCtx,   fileOriginalsCanvas);
  drawMultiContinuousSignals([data.oversampled_1, data.oversampled_2], fileOversampledCtx, fileOversampledCanvas);
  drawSignalOnCanvas(data.sum_signal, fileSumCtx, fileSumCanvas);
}

// ═══════════════════════════════════════════════════════════════════════════
//  Event listeners
// ═══════════════════════════════════════════════════════════════════════════
domainSelect.addEventListener('change', () => {
  populateSignalOptions(domainSelect.value);
  populateTransformOptions(domainSelect.value);
  updateInterpolationModeVisibility();
  loadSignal(signalSelect.value);
  finalExpressionEl.textContent = '— aplicar transformación para ver el resultado —';
  transformNoteEl.textContent   = '';
  clearCanvas(step1Ctx, step1Canvas);
  clearCanvas(step2Ctx, step2Canvas);
});

loadBtn.addEventListener('click',        () => loadSignal(signalSelect.value));
transformBtn.addEventListener('click',   () => applyTransform());
if (interpolateBtn)  interpolateBtn.addEventListener('click',  () => applyInterpolation());
if (continuousOpBtn) continuousOpBtn.addEventListener('click', () => applyContinuousOperation());
fileSumBtn.addEventListener('click',     () => processFileSignals());

// ═══════════════════════════════════════════════════════════════════════════
//  Init
// ═══════════════════════════════════════════════════════════════════════════
populateSignalOptions(domainSelect.value);
populateInterpolationSignals();
populateContinuousOperationSignals();
populateTransformOptions(domainSelect.value);
updateInterpolationModeVisibility();
loadSignal(signalSelect.value);

// Clear canvases with dark background
[
  [step1Ctx, step1Canvas],
  [step2Ctx, step2Canvas],
  [interpStep1Ctx, interpStep1Canvas],
  [interpStep2Ctx, interpStep2Canvas],
  [continuousOpStep1Ctx, continuousOpStep1Canvas],
  [continuousOpStep2Ctx, continuousOpStep2Canvas],
  [continuousOpFinalCtx, continuousOpFinalCanvas],
  [fileOriginalsCtx,   fileOriginalsCanvas],
  [fileOversampledCtx, fileOversampledCanvas],
  [fileSumCtx,         fileSumCanvas],
].forEach(([c, el]) => clearCanvas(c, el));

if (interpSignalSelect && interpSignalSelect.options.length > 0) applyInterpolation();
if (continuousOpSignalSelect && continuousOpSignalSelect.options.length > 0) applyContinuousOperation();
