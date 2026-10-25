let state, token, draft, dirty = false, busy = false, videoURL, selectedPerson;
const $ = id => document.getElementById(id);
const pretty = value => JSON.stringify(value, null, 2);
function el(tag, text, cls) { const e = document.createElement(tag); if (text !== undefined) e.textContent = text; if (cls) e.className = cls; return e; }
function notice(text, error = false) { $('notice').textContent = text; $('notice').className = error ? 'error' : ''; }
function changed() { dirty = true; $('recommendations').textContent = 'Unsaved changes. Save edits and rerun affected steps to see current suggestions.'; notice('Unsaved edits — run buttons save these edits before executing.'); }
async function api(path, data, headers = {}) {
  const response = await fetch(path, { method: 'POST', headers: { 'X-Avocado-Token': token, 'Content-Type': 'application/json', ...headers }, body: data instanceof File ? data : JSON.stringify(data) });
  const result = await response.json(); if (!response.ok) throw Error(result.error || response.statusText); return result;
}
async function task(action) {
  if (busy) return; busy = true;
  document.querySelectorAll('button,input,textarea,select').forEach(b => b.disabled = true);
  try { await action(); } catch (error) { notice(error.message, true); }
  finally { busy = false; document.querySelectorAll('button,input,textarea,select').forEach(b => b.disabled = false); }
}
function button(label, action, cls = 'secondary small') { const b = el('button', label, cls); b.type = 'button'; b.onclick = () => task(action); return b; }
function field(parent, title, value, onChange, rows = 2) {
  const label = el('label', title); const input = el('textarea'); input.rows = rows; input.value = typeof value === 'string' ? value : pretty(value); input.spellcheck = false;
  input.oninput = () => { onChange(input.value); $('config').value = pretty(draft); changed(); }; label.append(input); parent.append(label);
}
function editorSteps() {
  $('steps').replaceChildren();
  draft.steps.forEach((step, index) => {
    const card = el('div', undefined, 'step'), head = el('div', undefined, 'step-head');
    head.append(el('span', `${step.id} / ${step.kind}`, 'step-name'));
    const status = state.results[step.id]?.status || 'ready'; head.append(el('span', status, `badge ${status}`)); card.append(head);
    const controls = el('div', undefined, 'step-controls');
    controls.append(button('Run step', () => run(step.id, 'step')), button('Run from here', () => run(step.id, 'from')),
      button('↑', async () => { if (index) { [draft.steps[index - 1], draft.steps[index]] = [draft.steps[index], draft.steps[index - 1]]; editorSteps(); $('config').value = pretty(draft); changed(); } }),
      button('↓', async () => { if (index < draft.steps.length - 1) { [draft.steps[index + 1], draft.steps[index]] = [draft.steps[index], draft.steps[index + 1]]; editorSteps(); $('config').value = pretty(draft); changed(); } }),
      button('Remove', async () => { draft.steps.splice(index, 1); editorSteps(); $('config').value = pretty(draft); changed(); })); card.append(controls);
    const details = el('details'); details.append(el('summary', 'Prompt, model & step settings'));
    if (['observe', 'rank', 'model'].includes(step.kind)) {
      field(details, 'Model alias', step.model || '', v => step.model = v.trim());
      field(details, 'Prompt', step.prompt || '', v => step.prompt = v, 7);
      field(details, 'Additional inputs (JSON)', step.extra || {}, v => { try { step.extra = JSON.parse(v); } catch { /* invalid edits are caught before saving */ step.extra = v; } }, 3);
    }
    field(details, 'Settings (JSON)', step.settings, v => { try { step.settings = JSON.parse(v); } catch { step.settings = v; } }, 3);
    field(details, 'Input mappings (JSON)', step.inputs, v => { try { step.inputs = JSON.parse(v); } catch { step.inputs = v; } }, 3);
    card.append(details); $('steps').append(card);
  });
}
function currentOutput(kind) { for (const step of [...state.config.steps].reverse()) { if (step.kind === kind && state.results[step.id]?.status === 'current') return state.results[step.id].output; } return null; }
function renderFrames() {
  $('frames').replaceChildren(); const people = currentOutput('validate')?.people || currentOutput('observe')?.people || [];
  for (const frame of state.frames) {
    const card = el('div', undefined, 'frame'), canvas = el('canvas'); const img = new Image();
    img.onload = () => {
      canvas.width = img.width; canvas.height = img.height; const ctx = canvas.getContext('2d'); ctx.drawImage(img, 0, 0);
      for (const person of people) for (const loc of person.locations.filter(l => l.frame_id === frame.id)) {
        const [x, y, w, h] = loc.box, selected = person.id === selectedPerson;
        ctx.strokeStyle = selected ? '#ffce5c' : '#c4ff8c'; ctx.lineWidth = selected ? 7 : 3;
        ctx.strokeRect(x * img.width, y * img.height, w * img.width, h * img.height);
        ctx.font = 'bold 20px sans-serif'; const text = person.id + (person.identity_uncertain ? ' ?' : '');
        const top = Math.max(24, y * img.height); ctx.fillStyle = '#203a28'; ctx.fillRect(x * img.width, top - 24, ctx.measureText(text).width + 12, 26); ctx.fillStyle = '#fff'; ctx.fillText(text, x * img.width + 6, top - 5);
      }
    }; img.src = frame.image; card.append(canvas, el('span', `${frame.id} · ${frame.timestamp_s.toFixed(3)}s`)); $('frames').append(card);
  }
}
function recommendations() {
  const box = $('recommendations'); box.replaceChildren(); const output = currentOutput('rank');
  if (!output) { box.textContent = 'No current ranking. Run the pipeline or rerun stale steps.'; return; }
  if (output.status !== 'ok') box.append(el('p', 'Insufficient evidence to suggest someone.'));
  const observation = currentOutput('validate') || currentOutput('observe');
  if (Object.values(state.results).some(r => r.status === 'current' && r.human_assisted)) box.append(el('p', 'Human-assisted run: this result uses corrected inputs. It does not measure unassisted model accuracy.', 'muted'));
  output.candidates.forEach((candidate, i) => {
    const card = el('article', undefined, 'candidate'); card.append(el('h3', `${i + 1}. ${candidate.person_id} · ${candidate.preference_index}/100`));
    card.append(el('p', candidate.reason), el('p', `Connection / enjoyment: ${candidate.connection}`), el('p', `Effort / fatigue: ${candidate.effort}`), el('p', `Uncertainty: ${candidate.uncertainty}`));
    const person = observation?.people.find(p => p.id === candidate.person_id);
    candidate.evidence_ids.forEach(id => { const cue = person?.evidence.find(e => e.id === id); card.append(el('p', cue ? `${id} · ${cue.frame_id} · ${cue.visibility}: ${cue.cue} | Alternatives: ${cue.alternatives.join('; ')}` : id, 'muted')); });
    card.append(button('Locate in scene', async () => { selectedPerson = candidate.person_id; renderFrames(); $('frames').scrollIntoView({ behavior: 'smooth', block: 'center' }); })); box.append(card);
  });
  output.unknowns.forEach(text => box.append(el('p', `Unknown: ${text}`, 'muted')));
}
function inspect() {
  const id = $('inspect-step').value, result = state.results[id]; $('inspection').replaceChildren();
  if (!result) { $('inspection').append(el('p', 'This step has not run yet.')); $('correction').value = ''; return; }
  $('inspection').append(el('p', `${result.status} · ${result.source} · revision ${result.revision} · ${result.elapsed_s}s`));
  if (result.error) $('inspection').append(el('p', result.error, 'error'));
  const pre = el('pre', pretty(result)); $('inspection').append(pre);
  const history = el('details'); history.append(el('summary', `All attempts & original outputs (${state.history[id]?.length || 0})`), el('pre', pretty(state.history[id] || []))); $('inspection').append(history);
  $('correction').value = pretty(result.output || {});
}
function render(next) {
  state = next; draft = structuredClone(next.config); dirty = false;
  $('route').textContent = state.route ? `Configured route: ${state.route} · verify local GB10 execution` : 'Inference route not configured';
  $('preferences').value = state.context.personality_preferences || ''; $('goals').value = state.context.goals || ''; $('current-state').value = state.context.current_state || ''; $('energy').value = state.context.energy_budget || ''; $('rubric').value = state.rubric; $('config').value = pretty(draft);
  const selected = $('inspect-step').value; $('inspect-step').replaceChildren(); state.config.steps.forEach(s => { const opt = el('option', s.id); opt.value = s.id; $('inspect-step').append(opt); }); if (state.config.steps.some(s => s.id === selected)) $('inspect-step').value = selected;
  $('new-kind').replaceChildren(); state.kinds.forEach(k => { const opt = el('option', k); opt.value = k; $('new-kind').append(opt); });
  editorSteps(); renderFrames(); recommendations(); inspect();
  if (busy) document.querySelectorAll('button,input,textarea,select').forEach(b => b.disabled = true);
}
async function save() {
  const next = await api('/api/config', { config: draft, context: { personality_preferences: $('preferences').value, goals: $('goals').value, current_state: $('current-state').value, energy_budget: $('energy').value }, rubric: $('rubric').value }); render(next);
}
async function run(step, mode) {
  await save(); notice(`Running ${mode === 'all' ? 'pipeline' : step}… Local model requests can take several minutes.`);
  const next = await api('/api/run', { step, mode }); render(next); const errors = Object.values(state.results).filter(r => r.status === 'error');
  if (errors.length) notice(errors.map(e => e.error).join('\n'), true); else notice('Execution complete. Inspect evidence, uncertainty, and revision history below.');
}
$('save').onclick = () => task(async () => { await save(); notice('Saved. Affected downstream results are marked stale.'); });
$('apply-json').onclick = () => task(async () => { draft = JSON.parse($('config').value); await save(); notice('Pipeline JSON saved.'); });
$('config').oninput = () => { try { draft = JSON.parse($('config').value); } catch { /* handled on execution */ draft = null; } changed(); };
$('run-all').onclick = () => task(() => run('', 'all'));
$('add-step').onclick = () => task(async () => { const kind = $('new-kind').value, id = `${kind}_${Date.now()}`; draft.steps.push({ id, kind, inputs: { value: '$validate' }, settings: {}, ...(['model','observe','rank'].includes(kind) ? { model: 'reasoning', prompt: 'Return a JSON object.', extra: {} } : {}) }); editorSteps(); $('config').value = pretty(draft); changed(); });
$('upload').onclick = () => task(async () => {
  const file = $('video').files[0]; if (!file) throw Error('Choose a video first.'); if (!$('consent').checked) throw Error('Confirm permission to process the clip.'); if (file.size > 64 * 1024 * 1024) throw Error('Choose a clip up to 64 MiB.');
  await save(); const next = await api('/api/upload', file, { 'Content-Type': 'application/octet-stream', 'X-Upload-Consent': 'yes', 'X-Filename': encodeURIComponent(file.name) });
  if (videoURL) URL.revokeObjectURL(videoURL); videoURL = URL.createObjectURL(file); $('preview').src = videoURL; $('preview').hidden = false; render(next); notice('Clip uploaded. Run the sampling step to inspect frames, or Run all.');
});
$('reset').onclick = () => task(async () => { const next = await api('/api/reset', {}); if (videoURL) URL.revokeObjectURL(videoURL); $('preview').removeAttribute('src'); $('preview').load(); $('preview').hidden = true; $('video').value = ''; $('consent').checked = false; selectedPerson = null; render(next); notice('Session cleared. Video, frames, context, and run history removed from this process.'); });
$('correct').onclick = () => task(async () => { const step = $('inspect-step').value, output = JSON.parse($('correction').value); if (dirty) await save(); const next = await api('/api/correct', { step, output }); render(next); notice('Human correction saved as a separate revision. Rerun downstream steps.'); });
$('inspect-step').onchange = inspect;
['preferences','goals','current-state','energy','rubric'].forEach(id => $(id).oninput = changed);
fetch('/api/state').then(r => r.json()).then(next => { token = next.token; render(next); notice('Ready. Add context and upload an authorized clip. Local model aliases are configured in Pipeline JSON.'); }).catch(e => notice(e.message, true));
