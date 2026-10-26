const $ = id => document.getElementById(id);
let token, state, previewURL;
function notice(text, error = false) { $('notice').textContent = text; $('notice').className = error ? 'error' : ''; }
function render(editors = false) {
  if (editors) {
    for (const key of ['video', 'reason']) {
      $(key + '-model').value = state.config[key].model;
      $(key + '-prompt').value = state.config[key].prompt;
      $(key + '-settings').value = JSON.stringify(state.config[key].settings, null, 2);
    }
    $('video-schema').value = JSON.stringify(state.config.video.schema, null, 2);
  }
  $('filename').textContent = state.filename || 'No video uploaded.';
  for (const key of ['video', 'reason']) {
    const result = state.results[key] || {};
    $(key + '-status').textContent = result.status || 'Not run';
    $(key + '-output').textContent = Object.hasOwn(result, 'json') ? JSON.stringify(result.json, null, 2) : result.output || 'No output yet.';
    $(key + '-error').textContent = result.error || '';
  }
  const thinking = state.results.reason?.reasoning || '';
  $('thinking-panel').hidden = !thinking;
  $('thinking').textContent = thinking;
}
async function request(path, body, headers = {}) {
  const response = await fetch(path, {method: 'POST', headers: {'X-Avocado-Token': token, ...headers}, body: body instanceof File ? body : JSON.stringify(body)});
  const result = await response.json();
  if (!response.ok) throw new Error(result.error || 'Request failed');
  state = result;
  render();
}
async function save() {
  const config = {version: 2};
  for (const key of ['video', 'reason']) config[key] = {model: $(key + '-model').value, prompt: $(key + '-prompt').value, settings: JSON.parse($(key + '-settings').value)};
  config.video.schema = JSON.parse($('video-schema').value);
  await request('/api/config', {config});
}
async function busy(action) {
  const controls = [...document.querySelectorAll('button, input, textarea')];
  controls.forEach(el => el.disabled = true);
  try { await action(); } catch (error) { notice(error.message, true); }
  finally { controls.forEach(el => el.disabled = false); }
}
async function run(step) {
  await save();
  notice(step === 'reason' ? 'Reasoning over the video JSON…' : 'Analyzing the video locally. Model loading and inference can take a few minutes…');
  await request('/api/run', {step: step || '', mode: step ? 'step' : 'all'});
  const failed = Object.values(state.results).find(result => result.status === 'error');
  notice(failed ? failed.error : 'Output ready.', Boolean(failed));
}
$('file').addEventListener('change', () => busy(async () => {
  const file = $('file').files[0];
  if (!file) return;
  if (!$('consent').checked) { $('file').value = ''; throw new Error('Confirm permission before uploading.'); }
  if (file.size > 64 * 1024 * 1024) throw new Error('Choose a video up to 64 MiB.');
  await request('/api/upload', file, {'X-Upload-Consent': 'yes', 'X-Filename': encodeURIComponent(file.name)});
  if (previewURL) URL.revokeObjectURL(previewURL);
  previewURL = URL.createObjectURL(file);
  $('preview').src = previewURL;
  $('preview').hidden = false;
  notice('Video uploaded. Edit either prompt or the JSON schema, then run.');
}));
$('save').onclick = () => busy(async () => { await save(); notice('Edits saved. Changed inputs mark previous outputs stale.'); });
$('both').onclick = () => busy(() => run());
$('run-video').onclick = () => busy(() => run('video'));
$('run-reason').onclick = () => busy(() => run('reason'));
$('clear').onclick = () => busy(async () => {
  await request('/api/reset', {});
  render(true);
  if (previewURL) URL.revokeObjectURL(previewURL);
  previewURL = null;
  $('preview').removeAttribute('src'); $('preview').load(); $('preview').hidden = true;
  $('file').value = ''; $('consent').checked = false;
  notice('Session cleared.');
});
fetch('/api/state').then(response => response.json()).then(data => { token = data.token; state = data; render(true); }).catch(error => notice(error.message, true));
