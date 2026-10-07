/* ==========================================================================
   PARAWAWA (PARAWEMA) ECO BIO SEPTIC TANK - MOBILE RESPONSIVE JS
   Handles Mobile Drawer, Accordion, Calculator, Modal & 10 SEO Article Reader
   ========================================================================== */

document.addEventListener('DOMContentLoaded', () => {

  // --- 0. Compact Navbar on Scroll ---
  const navbarEl = document.querySelector('.navbar');
  if (navbarEl) {
    const updateNavbarScrolled = () => {
      navbarEl.classList.toggle('scrolled', window.scrollY > 20);
    };
    updateNavbarScrolled();
    window.addEventListener('scroll', updateNavbarScrolled, { passive: true });
  }

  // --- 1. Mobile Menu Drawer Toggle ---
  const mobileMenuBtn = document.getElementById('mobileMenuBtn');
  const mobileDrawer = document.getElementById('mobileDrawer');

  if (mobileMenuBtn && mobileDrawer) {
    mobileMenuBtn.addEventListener('click', (e) => {
      e.stopPropagation();
      mobileDrawer.classList.toggle('active');
      const icon = mobileMenuBtn.querySelector('i');
      if (icon) {
        if (mobileDrawer.classList.contains('active')) {
          icon.className = 'fas fa-times';
          document.body.style.overflow = 'hidden';
        } else {
          icon.className = 'fas fa-bars';
          document.body.style.overflow = '';
        }
      }
    });

    const drawerLinks = mobileDrawer.querySelectorAll('a');
    drawerLinks.forEach(link => {
      link.addEventListener('click', () => {
        mobileDrawer.classList.remove('active');
        document.body.style.overflow = '';
        const icon = mobileMenuBtn.querySelector('i');
        if (icon) icon.className = 'fas fa-bars';
      });
    });

    document.addEventListener('click', (e) => {
      if (mobileDrawer.classList.contains('active') && !mobileDrawer.contains(e.target) && !mobileMenuBtn.contains(e.target)) {
        mobileDrawer.classList.remove('active');
        document.body.style.overflow = '';
        const icon = mobileMenuBtn.querySelector('i');
        if (icon) icon.className = 'fas fa-bars';
      }
    });
  }

  // --- 2. 10 Full SEO/AEO/GEO Articles Text Database & Dynamic Grid Handler ---
  // Article metadata is generated into articles-meta.js by tools/build_articles.py;
  // each article lives on its own page at /articles/<slug>/.
  const articlesData = window.ARTICLES_META || {};

  // --- Dynamic Toggle for Homepage Articles Grid (#toggleAllArticlesBtn) ---
  const articlesGrid = document.getElementById('articlesGrid');
  const toggleAllArticlesBtn = document.getElementById('toggleAllArticlesBtn');
  let showingAllArticles = false;

  const renderArticlesGrid = () => {
    if (!articlesGrid) return;

    // Determine article keys to display (either 1-3 or 1-10)
    const keysToShow = showingAllArticles ? Object.keys(articlesData) : ["1", "2", "3"];

    articlesGrid.innerHTML = keysToShow.filter(key => articlesData[key]).map(key => {
      const art = articlesData[key];
      const imgClass = /\.png$/i.test(art.img) ? ' contain' : '';

      return `
        <article class="article-card reveal active" data-article="${key}">
          <div class="article-card-img${imgClass}">
            <img src="/${art.img.replace(/\.(jpg|jpeg|png)$/i, '.webp')}" alt="${art.imgAlt}" width="400" height="200" loading="lazy" decoding="async">
            <span class="article-badge badge-blue">${art.badge}</span>
          </div>
          <div class="article-card-body">
            <div class="article-meta"><i class="far fa-clock"></i> ${art.readTime}</div>
            <h3 class="article-title"><a class="card-link" href="/articles/${art.slug}/">${art.title}</a></h3>
            <p class="article-summary">${art.summary}</p>
            <span class="btn btn-secondary btn-block btn-sm" aria-hidden="true"><i class="fas fa-book-reader"></i> Read Full Article</span>
          </div>
        </article>
      `;
    }).join('');
  };

  if (toggleAllArticlesBtn) {
    toggleAllArticlesBtn.addEventListener('click', () => {
      showingAllArticles = !showingAllArticles;
      renderArticlesGrid();
      if (showingAllArticles) {
        toggleAllArticlesBtn.innerHTML = '<i class="fas fa-compress-alt"></i> Show Only 3 Featured Articles';
      } else {
        toggleAllArticlesBtn.innerHTML = '<i class="fas fa-th-large"></i> Explore All 20 Knowledge Articles';
        const blogSection = document.getElementById('blog');
        if (blogSection) blogSection.scrollIntoView({ behavior: 'smooth' });
      }
    });
  }

  // --- 3. Quote Modal Handlers ---
  const quoteModal = document.getElementById('quoteModal');
  const closeModalBtn = document.getElementById('closeModalBtn');
  const modalTriggers = document.querySelectorAll('.open-quote-modal');

  modalTriggers.forEach(btn => {
    btn.addEventListener('click', (e) => {
      e.preventDefault();
      if (quoteModal) {
        quoteModal.classList.add('active');
        document.body.style.overflow = 'hidden';
      }
    });
  });

  if (closeModalBtn && quoteModal) {
    closeModalBtn.addEventListener('click', () => {
      quoteModal.classList.remove('active');
      document.body.style.overflow = '';
    });

    quoteModal.addEventListener('click', (e) => {
      if (e.target === quoteModal) {
        quoteModal.classList.remove('active');
        document.body.style.overflow = '';
      }
    });
  }

  // Form Submissions
  const quoteForm = document.getElementById('quoteForm');
  const modalQuoteForm = document.getElementById('modalQuoteForm');

  const handleFormSubmit = (e) => {
    e.preventDefault();
    alert('Thank you! Your quote request has been received. Our engineering team at Parawewa led by Mr. Dharmakeerthi Mannage will contact you within 2 hours. / ස්තූතියි! ඔබගේ පණිවිඩය ලැබුණි. පරවැව ඉංජිනේරු කණ්ඩායම පැය 2ක් ඇතුළත ඔබ හා සම්බන්ධ වනු ඇත.');
    if (quoteModal) quoteModal.classList.remove('active');
    document.body.style.overflow = '';
    e.target.reset();
  };

  if (quoteForm) quoteForm.addEventListener('submit', handleFormSubmit);
  if (modalQuoteForm) modalQuoteForm.addEventListener('submit', handleFormSubmit);

  // --- 4. Tank Capacity Calculator & 10-Yr Savings ---
  const calculateBtn = document.getElementById('calculateBtn');
  const propertyTypeInput = document.getElementById('propertyType');
  const occupantsInput = document.getElementById('occupants');

  const resultCapacity = document.getElementById('resultCapacity');
  const resultSavings = document.getElementById('resultSavings');
  const resultWastewater = document.getElementById('resultWastewater');

  const updateCalculator = () => {
    if (!occupantsInput || !resultCapacity) return;

    const occupants = Math.max(1, parseInt(occupantsInput.value) || 5);
    const propType = propertyTypeInput ? propertyTypeInput.value : 'residential';

    let litersPerPerson = 150;
    if (propType === 'commercial') litersPerPerson = 80;
    if (propType === 'apartment') litersPerPerson = 180;
    if (propType === 'hotel') litersPerPerson = 250;

    const totalDailyLiter = occupants * litersPerPerson;
    const recommendedCapacity = Math.max(1000, Math.ceil((totalDailyLiter * 2) / 500) * 500);

    const annualGullySavings = 15000;
    const annualPowerSavings = propType === 'residential' ? 22500 : 50000;
    const total10YrSavings = (annualGullySavings + annualPowerSavings) * 10;
    const annualRecycledWater = occupants * 150 * 365;

    resultCapacity.textContent = `${recommendedCapacity.toLocaleString()} Liters`;
    if (resultSavings) resultSavings.textContent = `LKR ${total10YrSavings.toLocaleString()}`;
    if (resultWastewater) resultWastewater.textContent = `${annualRecycledWater.toLocaleString()} L / yr`;
  };

  if (calculateBtn) calculateBtn.addEventListener('click', updateCalculator);
  if (occupantsInput) occupantsInput.addEventListener('input', updateCalculator);
  if (propertyTypeInput) propertyTypeInput.addEventListener('change', updateCalculator);

  // --- 5. Searchable FAQ Accordion ---
  const accordionHeaders = document.querySelectorAll('.accordion-header');
  accordionHeaders.forEach(header => {
    header.addEventListener('click', () => {
      const item = header.parentElement;
      const isActive = item.classList.contains('active');

      document.querySelectorAll('.accordion-item').forEach(i => {
        i.classList.remove('active');
        const body = i.querySelector('.accordion-body');
        if (body) body.style.maxHeight = null;
      });

      if (!isActive) {
        item.classList.add('active');
        const body = item.querySelector('.accordion-body');
        if (body) body.style.maxHeight = body.scrollHeight + 'px';
      }
    });
  });

  const faqSearchInput = document.getElementById('faqSearch');
  if (faqSearchInput) {
    faqSearchInput.addEventListener('input', (e) => {
      const query = e.target.value.toLowerCase().trim();
      const items = document.querySelectorAll('.accordion-item');

      items.forEach(item => {
        const text = item.textContent.toLowerCase();
        if (text.includes(query)) {
          item.style.display = 'block';
        } else {
          item.style.display = 'none';
        }
      });
    });
  }

  // --- 6. Intersection Observer Scroll Reveal ---
  const revealElements = document.querySelectorAll('.reveal');
  if ('IntersectionObserver' in window && revealElements.length > 0) {
    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('active');
        }
      });
    }, { threshold: 0.1 });

    revealElements.forEach(el => observer.observe(el));
  } else {
    revealElements.forEach(el => el.classList.add('active'));
  }

  // --- 7. Industries Tab List (Who does Parawewa suit?) ---
  const indTabs = Array.from(document.querySelectorAll('.ind-item'));
  const indPanels = Array.from(document.querySelectorAll('.ind-panel'));

  const selectIndustry = (index, moveFocus) => {
    indTabs.forEach((tab, i) => {
      const on = i === index;
      tab.classList.toggle('active', on);
      tab.setAttribute('aria-selected', on ? 'true' : 'false');
      tab.tabIndex = on ? 0 : -1;
    });
    indPanels.forEach((panel, i) => {
      const on = i === index;
      panel.classList.toggle('active', on);
      panel.hidden = !on;
    });
    if (moveFocus) indTabs[index].focus();
  };

  indTabs.forEach((tab, i) => {
    tab.addEventListener('click', () => selectIndustry(i, false));
    tab.addEventListener('keydown', (e) => {
      let next = null;
      if (e.key === 'ArrowDown' || e.key === 'ArrowRight') next = (i + 1) % indTabs.length;
      if (e.key === 'ArrowUp' || e.key === 'ArrowLeft') next = (i - 1 + indTabs.length) % indTabs.length;
      if (e.key === 'Home') next = 0;
      if (e.key === 'End') next = indTabs.length - 1;
      if (next !== null) {
        e.preventDefault();
        selectIndustry(next, true);
      }
    });
  });

  // --- 8. Keep modal ARIA state in sync (hidden modals are not read as page content) ---
  document.querySelectorAll('.modal-overlay').forEach(modal => {
    const sync = () => modal.setAttribute('aria-hidden', modal.classList.contains('active') ? 'false' : 'true');
    sync();
    new MutationObserver(sync).observe(modal, { attributes: true, attributeFilter: ['class'] });
  });

});
