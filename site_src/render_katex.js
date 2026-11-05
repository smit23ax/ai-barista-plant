// Server-side KaTeX for the website: renders $$...$$ (display) and \(...\) (inline) in every .html file given,
// in place, with strict parsing (any bad expression stops the build). Writes katex.css (fonts inlined) once.
// Usage: NODE_PATH=docs/node_modules node site_src/render_katex.js site/katex.css site/a.html site/b.html ...
const fs = require('fs'), path = require('path'), katex = require('katex');
const [cssOut, ...files] = process.argv.slice(2);
const dec = s => s.replace(/&lt;/g, '<').replace(/&gt;/g, '>').replace(/&amp;/g, '&');
const opts = d => ({ displayMode: d, throwOnError: true, strict: 'error', output: 'html' });
let total = 0;
for (const f of files) {
  let html = fs.readFileSync(f, 'utf8'), n = 0;
  html = html.replace(/\$\$([\s\S]+?)\$\$/g, (_, tex) => { n++; return '<div class="eq">' + katex.renderToString(dec(tex), opts(true)) + '</div>'; });
  html = html.replace(/\\\(([\s\S]+?)\\\)/g, (_, tex) => { n++; return katex.renderToString(dec(tex), opts(false)); });
  fs.writeFileSync(f, html);
  total += n;
  console.log(path.basename(f), n, 'expressions');
}
const dist = path.dirname(require.resolve('katex/dist/katex.min.css'));
let css = fs.readFileSync(path.join(dist, 'katex.min.css'), 'utf8');
css = css.replace(/url\(fonts\/([^)]+?\.woff2)\)/g, (_, f) =>
  'url(data:font/woff2;base64,' + fs.readFileSync(path.join(dist, 'fonts', f)).toString('base64') + ')');
css = css.replace(/,url\(fonts\/[^)]+?\.(woff|ttf)\) format\("(woff|truetype)"\)/g, '');
fs.writeFileSync(cssOut, css);
console.log('total', total, 'expressions; katex.css', Math.round(css.length / 1024), 'KB');
