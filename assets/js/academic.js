(() => {
  const navigation = document.querySelectorAll('.nav-links a[data-section]');
  const updateNavigation = () => {
    const section = window.location.hash === '#publications' ? 'publications' : 'home';
    navigation.forEach(link => {
      if (link.dataset.section === section) link.setAttribute('aria-current', 'location');
      else link.removeAttribute('aria-current');
    });
  };
  updateNavigation();
  window.addEventListener('hashchange', updateNavigation);

  const dialog = document.getElementById('figure-dialog');
  if (!dialog || typeof dialog.showModal !== 'function') return;
  const image = document.getElementById('figure-full');
  const caption = document.getElementById('figure-caption');
  document.querySelectorAll('.figure-trigger').forEach(link => {
    link.addEventListener('click', event => {
      event.preventDefault();
      image.src = link.href;
      image.alt = link.querySelector('img').alt;
      caption.textContent = link.dataset.figureCaption;
      dialog.showModal();
    });
  });
  dialog.querySelector('.dialog-close').addEventListener('click', () => dialog.close());
  dialog.addEventListener('click', event => {
    if (event.target !== dialog) return;
    const rect = dialog.getBoundingClientRect();
    if (event.clientX < rect.left || event.clientX > rect.right || event.clientY < rect.top || event.clientY > rect.bottom) dialog.close();
  });
})();
