// Strict KaTeX parse of every expression given as a JSON array on stdin. Prints failures as JSON.
const katex = require('katex');
const exprs = JSON.parse(require('fs').readFileSync(0, 'utf8'));
const bad = [];
for (const tex of exprs) {
  try { katex.renderToString(tex, { displayMode: true, throwOnError: true, strict: 'error' }); }
  catch (e) { bad.push([tex, e.message]); }
}
console.log(JSON.stringify(bad));
