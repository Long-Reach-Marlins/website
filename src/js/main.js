// Small interactive helpers: nav toggle and dynamic year
(() => {
  const year = new Date().getFullYear();
  document.getElementById('year')?.textContent = year;
  document.getElementById('yearLegal')?.textContent = year;

  const navToggle = document.getElementById('navToggle');
  const mainNav = document.getElementById('mainNav');
  if (navToggle && mainNav) {
    navToggle.addEventListener('click', () => {
      const isOpen = mainNav.classList.toggle('open');
      navToggle.setAttribute('aria-expanded', String(isOpen));
    });
  }
})();
