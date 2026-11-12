from pathlib import Path
import re,json
p=Path(__file__).resolve().parents[1]
p.joinpath('webflow').mkdir(exist_ok=True)
html=p.joinpath('index.html').read_text()
body=re.search(r'<body>([\s\S]*)</body>',html).group(1)
body=re.sub(r'<script\b[^>]*>[\s\S]*?</script>', '', body)
css='\n'.join(p.joinpath(f).read_text() for f in ['styles.css','typography.css','buttons.css','theme.css'])
css=re.sub(r'@font-face\s*\{[^}]*\}', '',css)
css=css.replace('Poppins','MeNowMusclePoppins')
css=css.replace(':root', '.muscle-page')
css=re.sub(r'(?<![\w.-])body(?=\s|[.{:#>])','.muscle-page',css)
css=re.sub(r'(?<![\w.-])html(?=\s*\{)','.muscle-page',css)
css='''/* Styles intentionally live ONLY inside the shadow root. Do not paste into Webflow head. */
:host { all: initial !important; display: block !important; width: 100% !important; min-width: 0 !important; direction: ltr !important; unicode-bidi: isolate !important; }
:host::before, :host::after { content: none !important; }
.muscle-page { all: initial; display: block; direction: ltr; unicode-bidi: isolate; text-align: left; }
'''+css
js=p.joinpath('app.js').read_text().replace('document.querySelector','root.querySelector').replace('document.activeElement','root.activeElement').replace('document.addEventListener','root.addEventListener')
js=js.replace("root.addEventListener('visibilitychange'", "document.addEventListener('visibilitychange'")
p.joinpath('webflow/muscle-health.css').write_text(css)
loader='''/* Generated Webflow integration: keep original standalone files unchanged. */
(() => {
  'use strict';
  const script = document.currentScript;
  const host = script.previousElementSibling;
  if (!host || !host.matches('[data-menow-muscle-health]') || host.shadowRoot) return;
  const base = new URL('../', script.src);
  const asset = path => new URL(path, base).href;
  // A unique family prevents host-site Poppins definitions from changing this page.
  const fontReady = Promise.all([['Regular',400],['Medium',500],['SemiBold',600]].map(async ([name,weight]) => {
    const face = new FontFace('MeNowMusclePoppins', `url("${asset(`assets/fonts/Poppins-${name}.ttf`)}")`, {weight:String(weight), display:'swap'});
    document.fonts.add(face);
    try { await face.load(); } catch (error) { console.warn('Muscle Health font unavailable', error); }
  }));
  const root = host.attachShadow({mode:'open'});
  const style = document.createElement('style');
  style.textContent = CSS_TEXT.replace(/url\\((['"]?)(assets\\/[^)'"\\s]+)\\1\\)/g, (_,quote,path) => `url("${asset(path)}")`);
  const page = document.createElement('div');
  page.className = 'muscle-page';
  page.lang = 'en';
  page.innerHTML = BODY_HTML;
  for (const element of page.querySelectorAll('[src], [poster], [data-src]')) {
    for (const attribute of ['src','poster','data-src']) {
      const value = element.getAttribute(attribute);
      if (value && value.startsWith('assets/')) element.setAttribute(attribute, asset(value));
    }
  }
  root.append(style, page);
APP_JS
  fontReady.then(() => { fitNavigation(); window.dispatchEvent(new Event('resize')); });
  document.addEventListener('click', event => {
    if (!event.composedPath().includes(host)) closeMenu();
  });
  // Native fragment lookup does not find IDs inside a shadow tree.
  function goToFragment(hash, focus = false) {
    let id;
    try { id = decodeURIComponent(hash.slice(1)); } catch { return; }
    const target = id ? root.getElementById(id) : page;
    if (!target) return;
    const offset = header.getBoundingClientRect().height + 12;
    const top = target.getBoundingClientRect().top + window.scrollY - offset;
    window.scrollTo({top: Math.max(0, top), behavior: window.matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth'});
    if (focus) {
      const hadTabindex = target.hasAttribute('tabindex');
      if (!hadTabindex) target.setAttribute('tabindex','-1');
      target.focus({preventScroll:true});
      if (!hadTabindex) target.addEventListener('blur', () => target.removeAttribute('tabindex'), {once:true});
    }
  }
  root.addEventListener('click', event => {
    const link = event.target.closest('a[href^="#"]');
    if (!link || event.button !== 0 || event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) return;
    const hash = link.getAttribute('href');
    event.preventDefault();
    history.pushState(null, '', hash === '#' ? location.pathname + location.search : hash);
    goToFragment(hash, true);
  });
  window.addEventListener('hashchange', () => goToFragment(location.hash));
  if (location.hash) fontReady.then(() => goToFragment(location.hash));
})();
'''.replace('CSS_TEXT',json.dumps(css)).replace('BODY_HTML',json.dumps(body)).replace('APP_JS',js)
p.joinpath('webflow/muscle-health.js').write_text(loader)
p.joinpath('webflow/embed.html').write_text('''<!-- Replace this example URL with the HTTPS location where you publish this folder. -->
<div data-menow-muscle-health></div>
<script src="https://YOUR-ASSET-HOST/glp1-agonist/webflow/muscle-health.js"></script>
''')
p.joinpath('webflow/preview.html').write_text('''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Webflow isolated preview</title><style>body{margin:0}</style><div data-menow-muscle-health></div><script src="muscle-health.js"></script></html>''')
