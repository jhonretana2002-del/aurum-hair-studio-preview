const menuButton = document.querySelector('.menu-toggle');
const navigation = document.querySelector('.main-nav');
menuButton.addEventListener('click', () => {
  const open = menuButton.getAttribute('aria-expanded') !== 'true';
  menuButton.setAttribute('aria-expanded', String(open));
  menuButton.setAttribute('aria-label', open ? 'Cerrar menú' : 'Abrir menú');
  navigation.classList.toggle('is-open', open);
});
navigation.addEventListener('click', (event) => {
  if (event.target.closest('a')) {
    navigation.classList.remove('is-open');
    menuButton.setAttribute('aria-expanded', 'false');
    menuButton.setAttribute('aria-label', 'Abrir menú');
  }
});

const searchButton = document.querySelector('.search-trigger');
const searchPanel = document.querySelector('#search-panel');
const searchInput = document.querySelector('#category-search');
const searchStatus = document.querySelector('#search-status');
const categories = [...document.querySelectorAll('.discover-card')];
searchButton.addEventListener('click', () => {
  const open = searchPanel.hidden;
  searchPanel.hidden = !open;
  searchButton.setAttribute('aria-expanded', String(open));
  if (open) searchInput.focus();
  else { searchInput.value = ''; categories.forEach(card => card.hidden = false); searchStatus.textContent = ''; }
});
searchInput.addEventListener('input', () => {
  const query = searchInput.value.trim().toLocaleLowerCase('es');
  let count = 0;
  categories.forEach(card => { const match = card.textContent.toLocaleLowerCase('es').includes(query); card.hidden = !match; if (match) count++; });
  searchStatus.textContent = query ? `${count} ${count === 1 ? 'categoría encontrada' : 'categorías encontradas'}` : '';
});
document.addEventListener('keydown', event => {
  if (event.key === 'Escape' && !searchPanel.hidden) {
    searchPanel.hidden = true; searchButton.setAttribute('aria-expanded', 'false'); searchButton.focus();
    searchInput.value = ''; categories.forEach(card => card.hidden = false); searchStatus.textContent = '';
  }
});

const dialog = document.querySelector('#info-dialog');
document.querySelectorAll('.info-trigger').forEach(button => button.addEventListener('click', () => {
  document.querySelector('#dialog-message').textContent = button.dataset.message;
  dialog.showModal();
}));
document.querySelector('#year').textContent = new Date().getFullYear();

if (new URLSearchParams(location.search).get('preview') === 'videos') {
  const preview = document.querySelector('#video-preview');
  preview.hidden = false;
  preview.querySelectorAll('img[data-src]').forEach(image => { image.src = image.dataset.src; });
  document.title = 'Aurum Hair Studio — Propuesta de videos verticales';
  if (location.hash === '#video-preview') {
    window.addEventListener('load', () => {
      setTimeout(() => preview.scrollIntoView({ behavior: 'instant', block: 'start' }), 100);
    }, { once: true });
  }
}
