// Server-side KaTeX render: $$...$$ (display) and \(...\) (inline), strict parse, CSS + fonts inlined.
const fs = require('fs'), path = require('path'), katex = require('katex');
const [src, out] = process.argv.slice(2);
let html = fs.readFileSync(src, 'utf8');
let count = 0;
const dec = s => s.replace(/&lt;/g, '<').replace(/&gt;/g, '>').replace(/&amp;/g, '&');
const opts = d => ({ displayMode: d, throwOnError: true, strict: 'error', output: 'html' });
html = html.replace(/\$\$([\s\S]+?)\$\$/g, (_, tex) => { count++; return '<div class="eq">' + katex.renderToString(dec(tex), opts(true)) + '</div>'; });
html = html.replace(/\\\(([\s\S]+?)\\\)/g, (_, tex) => { count++; return katex.renderToString(dec(tex), opts(false)); });
const dist = path.dirname(require.resolve('katex/dist/katex.min.css'));
let css = fs.readFileSync(path.join(dist, 'katex.min.css'), 'utf8');
css = css.replace(/url\(fonts\/([^)]+?\.woff2)\)/g, (_, f) =>
  'url(data:font/woff2;base64,' + fs.readFileSync(path.join(dist, 'fonts', f)).toString('base64') + ')');
css = css.replace(/,url\(fonts\/[^)]+?\.(woff|ttf)\) format\("(woff|truetype)"\)/g, '');
const page = `<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>${path.basename(out, '.html').replace('_', ' ')}</title>
<style>${css}
:root{--bg:#0d1117;--fg:#c9d1d9;--mut:#8b95a1;--acc:#7ee787;--line:#30363d;--card:#161b22}
body{background:var(--bg);color:var(--fg);font:16px/1.65 system-ui,-apple-system,Segoe UI,Roboto,sans-serif;margin:0}
main{max-width:860px;margin:0 auto;padding:32px 16px 80px}
h1{font:600 30px/1.2 ui-monospace,Menlo,monospace;letter-spacing:1px}
h2{font:600 21px/1.3 ui-monospace,Menlo,monospace;margin-top:48px;border-top:1px solid var(--line);padding-top:24px}
h3{font:600 17px ui-monospace,Menlo,monospace;color:var(--acc)}
a{color:#58a6ff} code{font:14px ui-monospace,Menlo,monospace;background:var(--card);padding:1px 5px;border-radius:4px}
.lead{color:var(--mut)} .eq{overflow-x:auto;overflow-y:hidden;padding:4px 0}
.phys{background:var(--card);border-left:3px solid var(--acc);padding:10px 14px;border-radius:4px}
.toc{display:grid;grid-template-columns:repeat(auto-fill,minmax(250px,1fr));gap:4px 16px;background:var(--card);padding:14px;border-radius:6px}
table{border-collapse:collapse;width:100%;font-size:14px} th,td{border-bottom:1px solid var(--line);padding:6px 8px;text-align:left;vertical-align:top}
@media print{body{background:#fff;color:#000}.phys,.toc,code{background:#f3f3f3}}
</style></head><body><main>${html}</main></body></html>`;
fs.writeFileSync(out, page);
console.log('rendered', count, 'expressions,', Math.round(page.length / 1024), 'KB');
