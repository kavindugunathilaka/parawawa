/* ==========================================================================
   PARAWAWA (PARAWEMA) ECO BIO SEPTIC TANK SYSTEM - JS APPLICATION LOGIC
   Mobile-First Navigation, Fast Calculations, Accordion & Scroll Observers
   ========================================================================== */

document.addEventListener('DOMContentLoaded', () => {
  // --- 1. Mobile Navigation Drawer Toggle ---
  const mobileMenuBtn = document.getElementById('mobileMenuBtn');
  const mobileDrawer = document.getElementById('mobileDrawer');
  const mobileNavLinks = document.querySelectorAll('.mobile-nav-link');

  if (mobileMenuBtn && mobileDrawer) {
    mobileMenuBtn.addEventListener('click', () => {
      const isOpen = mobileDrawer.classList.contains('active');
      if (isOpen) {
        mobileDrawer.classList.remove('active');
        mobileMenuBtn.innerHTML = '<i class="fas fa-bars"></i>';
        document.body.style.overflow = '';
      } else {
        mobileDrawer.classList.add('active');
        mobileMenuBtn.innerHTML = '<i class="fas fa-times"></i>';
        document.body.style.overflow = 'hidden';
      }
    });

    mobileNavLinks.forEach(link => {
      link.addEventListener('click', () => {
        mobileDrawer.classList.remove('active');
        mobileMenuBtn.innerHTML = '<i class="fas fa-bars"></i>';
        document.body.style.overflow = '';
      });
    });
  }

  // --- 2. Theme Switcher (Dark / Light Mode) ---
  const themeToggleBtn = document.getElementById('themeToggle');
  const currentTheme = localStorage.getItem('parawawa_theme') || 'dark';

  if (currentTheme === 'light') {
    document.documentElement.setAttribute('data-theme', 'light');
    if (themeToggleBtn) themeToggleBtn.innerHTML = '<i class="fas fa-moon"></i>';
  } else {
    document.documentElement.setAttribute('data-theme', 'dark');
    if (themeToggleBtn) themeToggleBtn.innerHTML = '<i class="fas fa-sun"></i>';
  }

  if (themeToggleBtn) {
    themeToggleBtn.addEventListener('click', () => {
      const isDark = document.documentElement.getAttribute('data-theme') === 'dark';
      const newTheme = isDark ? 'light' : 'dark';
      
      document.documentElement.setAttribute('data-theme', newTheme);
      localStorage.setItem('parawawa_theme', newTheme);
      
      themeToggleBtn.innerHTML = newTheme === 'light' ? '<i class="fas fa-moon"></i>' : '<i class="fas fa-sun"></i>';
    });
  }

  // --- 3. Interactive Septic Tank Capacity & Cost-Savings Calculator ---
  const propertyTypeSelect = document.getElementById('propertyType');
  const occupantInput = document.getElementById('occupants');
  const calcBtn = document.getElementById('calculateBtn');

  const resultCapacity = document.getElementById('resultCapacity');
  const resultSavings = document.getElementById('resultSavings');
  const resultWastewater = document.getElementById('resultWastewater');

  function calculateTankSpecs() {
    if (!occupantInput || !propertyTypeSelect) return;
    const occupants = parseInt(occupantInput.value) || 5;
    const property = propertyTypeSelect.value;

    let multiplier = 1.0;
    if (property === 'commercial') multiplier = 1.4;
    if (property === 'hotel') multiplier = 1.8;
    if (property === 'apartment') multiplier = 1.5;

    const dailyVolume = Math.round(occupants * 150 * multiplier);
    
    let tankCapacityLiters = 1500;
    if (occupants > 6) tankCapacityLiters = 2500;
    if (occupants > 12) tankCapacityLiters = 5000;
    if (occupants > 25) tankCapacityLiters = 10000;
    if (occupants > 50) tankCapacityLiters = 25000;

    const annualGullyCost = 35000 * (occupants / 5) * multiplier;
    const total25YrSavings = Math.round(annualGullyCost * 25);

    if (resultCapacity) resultCapacity.textContent = `${tankCapacityLiters.toLocaleString()} Liters`;
    if (resultSavings) resultSavings.textContent = `LKR ${total25YrSavings.toLocaleString()}`;
    if (resultWastewater) resultWastewater.textContent = `${(dailyVolume * 365).toLocaleString()} L / yr`;
  }

  if (calcBtn) {
    calcBtn.addEventListener('click', calculateTankSpecs);
    occupantInput.addEventListener('input', calculateTankSpecs);
    propertyTypeSelect.addEventListener('change', calculateTankSpecs);
    calculateTankSpecs();
  }

  // --- 4. Tech Deep Dive Tab Switcher ---
  const techTabs = document.querySelectorAll('.tech-tab');
  const techStepTitle = document.getElementById('techStepTitle');
  const techStepDesc = document.getElementById('techStepDesc');

  const stepData = {
    1: {
      title: 'Stage 1: Primary Anaerobic Settling & Separation',
      desc: 'Raw wastewater enters the first chamber where heavy solids settle down naturally and oils/grease float to primary separation traps. Anaerobic microbes begin initial organic breakdown without energy input.'
    },
    2: {
      title: 'Stage 2: Oxygenated Aerobic Bio-Decomposition',
      desc: 'Wastewater passes through oxygenated channels. Specialized aerobic bacteria thrive in biological matrix beds, consuming up to 98% of harmful dissolved pathogens and organic pollutants.'
    },
    3: {
      title: 'Stage 3: Patented Multi-Layer Filter Media',
      desc: 'The unique Sri Lankan patented layer-base substrate bed filters micro-particles. Natural granite, biological sand, and porous rock layers digest remaining organic sludge, preventing any blockage.'
    },
    4: {
      title: 'Stage 4: Eco-Clean Purified Outflow (Irrigation Safe)',
      desc: 'Final discharge liquid reaches WHO/CEA environmental discharge standards. The odorless, pathogen-free water recharges groundwater aquifers or can be directly reused for gardening and landscape irrigation.'
    }
  };

  techTabs.forEach(tab => {
    tab.addEventListener('click', () => {
      techTabs.forEach(t => t.classList.remove('active'));
      tab.classList.add('active');

      const step = tab.getAttribute('data-step');
      if (stepData[step] && techStepTitle && techStepDesc) {
        techStepTitle.textContent = stepData[step].title;
        techStepDesc.textContent = stepData[step].desc;
      }
    });
  });

  // --- 5. Searchable & Expandable FAQ Accordion ---
  const faqItems = document.querySelectorAll('.accordion-item');
  const faqSearchInput = document.getElementById('faqSearch');

  faqItems.forEach(item => {
    const header = item.querySelector('.accordion-header');
    if (header) {
      header.addEventListener('click', () => {
        const isActive = item.classList.contains('active');
        
        faqItems.forEach(i => {
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
    }
  });

  if (faqSearchInput) {
    faqSearchInput.addEventListener('input', (e) => {
      const query = e.target.value.toLowerCase().trim();

      faqItems.forEach(item => {
        const text = item.textContent.toLowerCase();
        item.style.display = text.includes(query) ? 'block' : 'none';
      });
    });
  }

  // --- 6. Quote Request Modal & Form Handling ---
  const openModalBtns = document.querySelectorAll('.open-quote-modal');
  const modalOverlay = document.getElementById('quoteModal');
  const closeModalBtn = document.getElementById('closeModalBtn');
  const quoteForm = document.getElementById('quoteForm');

  openModalBtns.forEach(btn => {
    btn.addEventListener('click', (e) => {
      e.preventDefault();
      if (modalOverlay) modalOverlay.classList.add('active');
    });
  });

  if (closeModalBtn && modalOverlay) {
    closeModalBtn.addEventListener('click', () => {
      modalOverlay.classList.remove('active');
    });
  }

  if (modalOverlay) {
    modalOverlay.addEventListener('click', (e) => {
      if (e.target === modalOverlay) modalOverlay.classList.remove('active');
    });
  }

  if (quoteForm) {
    quoteForm.addEventListener('submit', (e) => {
      e.preventDefault();
      const submitBtn = quoteForm.querySelector('button[type="submit"]');
      const originalText = submitBtn.innerHTML;
      
      submitBtn.disabled = true;
      submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Submitting...';

      setTimeout(() => {
        submitBtn.innerHTML = '<i class="fas fa-check-circle"></i> Quote Request Submitted!';
        submitBtn.style.background = '#10b981';

        setTimeout(() => {
          if (modalOverlay) modalOverlay.classList.remove('active');
          quoteForm.reset();
          submitBtn.disabled = false;
          submitBtn.innerHTML = originalText;
          submitBtn.style.background = '';
          alert('Thank you! Your quote request for Parawawa Bio Septic System has been received. Our team will contact you shortly.');
        }, 1200);
      }, 1000);
    });
  }

  // --- 7. Fast Intersection Observer for Scroll Animations ---
  const observer = new IntersectionObserver((entries, obs) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('active');
        obs.unobserve(entry.target);
      }
    });
  }, { threshold: 0.1 });

  document.querySelectorAll('.reveal').forEach(el => observer.observe(el));
});
