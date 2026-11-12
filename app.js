// Scheduler links are configured in index.html; see documentation/microsoft-bookings.md.
// Measure the complete menu, including loaded fonts, rather than guessing a breakpoint.
const header = document.querySelector('.header');
const navRow = header.querySelector('.nav');
const menu = header.querySelector('nav');
const menuToggle = header.querySelector('.menu-toggle');
function closeMenu(restoreFocus = false) {
  header.classList.remove('is-menu-open');
  menuToggle.setAttribute('aria-expanded', 'false');
  menuToggle.setAttribute('aria-label', 'Open menu');
  if (restoreFocus) menuToggle.focus();
}
function fitNavigation() {
  menu.classList.add('is-measuring');
  const menuWidth = menu.getBoundingClientRect().width;
  menu.classList.remove('is-measuring');
  const rowStyle = getComputedStyle(navRow);
  const available = navRow.clientWidth - parseFloat(rowStyle.paddingLeft) - parseFloat(rowStyle.paddingRight);
  const needed = menuWidth + navRow.querySelector(':scope > a').getBoundingClientRect().width + navRow.querySelector(':scope > .button').getBoundingClientRect().width + parseFloat(rowStyle.columnGap) * 2;
  const collapsed = needed > available;
  header.classList.toggle('is-collapsed', collapsed);
  if (!collapsed) closeMenu();
}
menuToggle.addEventListener('click', () => {
  const open = header.classList.toggle('is-menu-open');
  menuToggle.setAttribute('aria-expanded', String(open));
  menuToggle.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
});
menu.addEventListener('click', event => { if (event.target.closest('a')) closeMenu(); });
document.addEventListener('keydown', event => { if (event.key === 'Escape' && header.classList.contains('is-menu-open')) closeMenu(true); });
document.addEventListener('click', event => { if (!header.contains(event.target)) closeMenu(); });
window.addEventListener('resize', fitNavigation);
document.fonts.ready.then(fitNavigation);
fitNavigation();

// Hero film: honor reduced motion and pause when the hero is out of view.
(() => {
 const video = document.querySelector('.hero-film');
 const control = document.querySelector('.hero-film-control');
 if (!video || !control) return;
 const preference = matchMedia('(prefers-reduced-motion: reduce)');
 let enabled = !preference.matches && !navigator.connection?.saveData;
 // Wait for the observer before playing: a restored scroll position may hide the hero.
 let visible = false;
 const sync = () => {
  if (enabled && visible && !document.hidden) video.play().catch(() => {
   // A pause during loading rejects play(). Keep the user preference so re-entry retries.
   update();
  });
  else video.pause();
 };
 const update = () => {
  control.dataset.playing = String(!video.paused);
  control.title = video.paused ? 'Play background video' : 'Pause background video';
  control.setAttribute('aria-label', video.paused ? 'Play background video' : 'Pause background video');
 };
 video.addEventListener('playing', () => { video.classList.add('has-frame'); update(); });
 video.addEventListener('error', () => { video.classList.remove('has-frame'); update(); });
 video.addEventListener('play', update);
 video.addEventListener('pause', update);
 control.addEventListener('click', () => { enabled = video.paused; sync(); });
 preference.addEventListener('change', () => { enabled = !preference.matches; sync(); });
 document.addEventListener('visibilitychange', sync);
 new IntersectionObserver(([entry]) => { visible = entry.isIntersecting; sync(); }).observe(video);
 update();
})();
