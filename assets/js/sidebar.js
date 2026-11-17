/* Sidebar/theme behaviour adapted from diaoquesang.github.io (MIT).
   Personal additions: accessible drawer states and framework image viewer. */
(() => {
  const root = document.documentElement;
  const themeToggle = document.getElementById('theme-toggle');
  const themeText = themeToggle.querySelector('.theme-toggle-text');
  const renderTheme = () => {
    const dark = root.dataset.theme === 'dark';
    themeText.textContent = dark ? 'Light' : 'Dark';
    themeToggle.setAttribute('aria-label', dark ? 'Switch to light theme' : 'Switch to dark theme');
  };
  themeToggle.addEventListener('click', () => {
    const next = root.dataset.theme === 'dark' ? 'light' : 'dark';
    root.dataset.theme = next;
    try { localStorage.setItem('academic-theme', next); } catch (error) { /* Theme still works without storage. */ }
    renderTheme();
  });
  renderTheme();

  const links = Array.from(document.querySelectorAll('.nav-link'));
  const sections = links.map(link => document.getElementById(link.hash.slice(1))).filter(Boolean);
  const sidebar = document.getElementById('sidebar');
  const drawerToggle = document.getElementById('drawer-toggle');
  const mobile = window.matchMedia('(max-width: 1000px)');
  const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
  function setDrawer(open) {
    const expanded = mobile.matches && open;
    sidebar.classList.toggle('open', expanded);
    document.body.classList.toggle('drawer-open', expanded);
    sidebar.inert = mobile.matches && !expanded;
    drawerToggle.setAttribute('aria-expanded', String(expanded));
    drawerToggle.setAttribute('aria-label', expanded ? 'Close navigation' : 'Open navigation');
  }
  drawerToggle.addEventListener('click', () => setDrawer(!sidebar.classList.contains('open')));
  mobile.addEventListener('change', () => setDrawer(false));
  setDrawer(false);
  document.addEventListener('click', event => {
    if (sidebar.classList.contains('open') && !sidebar.contains(event.target) && !drawerToggle.contains(event.target)) setDrawer(false);
  });
  document.addEventListener('keydown', event => {
    if (event.key === 'Escape' && sidebar.classList.contains('open')) { setDrawer(false); drawerToggle.focus(); }
  });
  links.forEach(link => link.addEventListener('click', event => {
    const target = document.getElementById(link.hash.slice(1));
    if (!target) return;
    event.preventDefault();
    target.scrollIntoView({ behavior: reducedMotion.matches ? 'auto' : 'smooth' });
    if (mobile.matches) { setDrawer(false); drawerToggle.focus(); }
  }));
  function updateActive() {
    if (!sections.length) return;
    let active = sections[0], bestTop = -Infinity;
    sections.forEach(section => {
      const top = section.getBoundingClientRect().top;
      if (top <= 140 && top > bestTop) { active = section; bestTop = top; }
    });
    links.forEach(link => {
      const current = link.hash === '#' + active.id;
      link.classList.toggle('active', current);
      if (current) link.setAttribute('aria-current', 'location');
      else link.removeAttribute('aria-current');
    });
  }
  window.addEventListener('scroll', updateActive, { passive: true });
  window.addEventListener('resize', updateActive);
  updateActive();

  function refreshScrollHints() {
    document.querySelectorAll('.scroll-box').forEach(box => {
      const hint = box.nextElementSibling;
      if (hint?.classList.contains('scroll-hint')) hint.hidden = box.scrollHeight - box.clientHeight <= 1;
    });
  }
  refreshScrollHints();
  window.addEventListener('resize', refreshScrollHints);
  window.addEventListener('load', refreshScrollHints);
  themeToggle.addEventListener('click', refreshScrollHints);

  const dialog = document.getElementById('figure-dialog');
  if (!dialog || typeof dialog.showModal !== 'function') return;
  const image = document.getElementById('figure-full');
  const caption = document.getElementById('figure-caption');
  document.querySelectorAll('.figure-trigger').forEach(link => link.addEventListener('click', event => {
    event.preventDefault();
    image.src = link.href;
    image.alt = link.querySelector('img').alt;
    caption.textContent = link.dataset.figureCaption;
    dialog.showModal();
  }));
  dialog.querySelector('.dialog-close').addEventListener('click', () => dialog.close());
  dialog.addEventListener('click', event => {
    if (event.target !== dialog) return;
    const rect = dialog.getBoundingClientRect();
    if (event.clientX < rect.left || event.clientX > rect.right || event.clientY < rect.top || event.clientY > rect.bottom) dialog.close();
  });
})();
