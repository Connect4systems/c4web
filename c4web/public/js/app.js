document.addEventListener("DOMContentLoaded", () => {
  const body = document.body;
  const menuToggle = document.querySelector("[data-menu-toggle]");
  const navShell = document.querySelector("[data-nav-shell]");
  const header = document.querySelector(".site-header");
  const navDropdowns = document.querySelectorAll("[data-nav-dropdown]");
  const isMobileNav = () => window.matchMedia("(max-width: 860px)").matches;

  const closeDropdowns = () => {
    navDropdowns.forEach((dropdown) => {
      dropdown.classList.remove("open");
      const toggle = dropdown.querySelector(".c4-nav-toggle");
      if (toggle) {
        toggle.setAttribute("aria-expanded", "false");
      }
    });
  };

  const closeMenu = () => {
    if (!menuToggle || !navShell) return;
    navShell.classList.remove("open");
    menuToggle.setAttribute("aria-expanded", "false");
    closeDropdowns();
  };

  if (menuToggle && navShell) {
    menuToggle.addEventListener("click", () => {
      const isOpen = navShell.classList.toggle("open");
      menuToggle.setAttribute("aria-expanded", String(isOpen));
      body.classList.toggle("menu-open", isOpen);
    });

    navShell.querySelectorAll("a").forEach((link) => {
      link.addEventListener("click", () => {
        closeMenu();
        body.classList.remove("menu-open");
      });
    });

    document.addEventListener("click", (event) => {
      const target = event.target;
      if (!(target instanceof Node)) return;
      if (!navShell.classList.contains("open")) return;
      if (navShell.contains(target) || menuToggle.contains(target)) return;
      closeMenu();
      body.classList.remove("menu-open");
    });
  }

  navDropdowns.forEach((dropdown) => {
    const toggle = dropdown.querySelector(".c4-nav-toggle");
    if (!toggle) return;

    toggle.addEventListener("click", (event) => {
      if (!isMobileNav()) {
        closeDropdowns();
        return;
      }

      event.preventDefault();
      event.stopPropagation();

      const isExpanded = toggle.getAttribute("aria-expanded") === "true";

      navDropdowns.forEach((item) => {
        if (item === dropdown) return;
        item.classList.remove("open");
        const itemToggle = item.querySelector(".c4-nav-toggle");
        if (itemToggle) {
          itemToggle.setAttribute("aria-expanded", "false");
        }
      });

      dropdown.classList.toggle("open", !isExpanded);
      toggle.setAttribute("aria-expanded", String(!isExpanded));
    });
  });

  document.addEventListener("click", (event) => {
    const target = event.target;
    if (!(target instanceof Element)) return;
    if (target.closest("[data-nav-dropdown]")) return;
    closeDropdowns();
  });

  document.addEventListener("keydown", (event) => {
    if (event.key !== "Escape") return;
    closeDropdowns();
    closeMenu();
    body.classList.remove("menu-open");
  });

  window.addEventListener("resize", () => {
    if (!isMobileNav()) {
      closeDropdowns();
    }
  });

  const navLinks = document.querySelectorAll(".main-nav a");
  const currentPath = window.location.pathname.replace(/\/$/, "") || "/";

  navLinks.forEach((link) => {
    const href = link.getAttribute("href");
    if (!href || href.startsWith("#")) return;
    const normalizedHref = href.replace(/\/$/, "") || "/";

    if (normalizedHref === currentPath) {
      link.classList.add("active");
      return;
    }

    // Keep section pages highlighted for mapped aliases such as /home -> /
    if (normalizedHref === "/" && ["/home", "/index-ar", "/index-en"].includes(currentPath)) {
      link.classList.add("active");
    }
  });

  const navToggles = document.querySelectorAll(".c4-nav-toggle");
  navToggles.forEach((toggle) => {
    const dropdown = toggle.closest("[data-nav-dropdown]");
    if (!dropdown) return;
    if (dropdown.querySelector("a.active")) {
      toggle.classList.add("active");
    }
  });

  const progressBar = document.querySelector("[data-scroll-progress]");
  const onScroll = () => {
    if (header) {
      header.classList.toggle("compact", window.scrollY > 10);
    }

    if (!progressBar) return;

    const scrollTop = window.scrollY;
    const documentHeight = document.documentElement.scrollHeight - window.innerHeight;
    const progress = documentHeight > 0 ? Math.min((scrollTop / documentHeight) * 100, 100) : 0;
    progressBar.style.width = `${progress}%`;
  };

  window.addEventListener("scroll", onScroll, { passive: true });
  onScroll();

  const revealItems = document.querySelectorAll(".reveal");
  if ("IntersectionObserver" in window) {
    const revealObserver = new IntersectionObserver(
      (entries, observer) => {
        entries.forEach((entry) => {
          if (!entry.isIntersecting) return;
          entry.target.classList.add("revealed");
          observer.unobserve(entry.target);
        });
      },
      { threshold: 0.16 }
    );

    revealItems.forEach((item) => revealObserver.observe(item));
  } else {
    revealItems.forEach((item) => item.classList.add("revealed"));
  }

  const counters = document.querySelectorAll("[data-counter]");
  const animateCounter = (element) => {
    const target = Number(element.dataset.counter || 0);
    const duration = Number(element.dataset.duration || 1400);
    const prefix = element.dataset.prefix || "";
    const suffix = element.dataset.suffix || "";
    const start = performance.now();

    const render = (time) => {
      const progress = Math.min((time - start) / duration, 1);
      const value = Math.floor(progress * target);
      element.textContent = `${prefix}${value.toLocaleString("ar-EG")}${suffix}`;

      if (progress < 1) {
        requestAnimationFrame(render);
      } else {
        element.textContent = `${prefix}${target.toLocaleString("ar-EG")}${suffix}`;
      }
    };

    requestAnimationFrame(render);
  };

  if ("IntersectionObserver" in window) {
    const counterObserver = new IntersectionObserver(
      (entries, observer) => {
        entries.forEach((entry) => {
          if (!entry.isIntersecting) return;
          animateCounter(entry.target);
          observer.unobserve(entry.target);
        });
      },
      { threshold: 0.45 }
    );

    counters.forEach((counter) => counterObserver.observe(counter));
  } else {
    counters.forEach((counter) => animateCounter(counter));
  }

  const tabShells = document.querySelectorAll(".tab-shell");
  tabShells.forEach((shell) => {
    const buttons = shell.querySelectorAll(".tab-button");
    const panels = shell.querySelectorAll(".tab-panel");

    if (!buttons.length || !panels.length) return;

    const activateTab = (id) => {
      buttons.forEach((button) => {
        const isActive = button.dataset.tabTarget === id;
        button.classList.toggle("active", isActive);
        button.setAttribute("aria-selected", String(isActive));
      });

      panels.forEach((panel) => {
        const isActive = panel.dataset.tabPanel === id;
        panel.classList.toggle("active", isActive);
      });
    };

    buttons.forEach((button) => {
      button.addEventListener("click", () => {
        const target = button.dataset.tabTarget;
        if (!target) return;
        activateTab(target);
      });
    });
  });

  const filterGroups = document.querySelectorAll("[data-filter-group]");
  filterGroups.forEach((group) => {
    const chips = group.querySelectorAll(".chip[data-filter]");
    const targetSelector = group.getAttribute("data-filter-target") || "";
    const scope = targetSelector ? document.querySelector(targetSelector) : group;

    if (!scope || !chips.length) return;

    const items = scope.querySelectorAll("[data-category]");
    if (!items.length) return;

    chips.forEach((chip) => {
      chip.addEventListener("click", () => {
        const filter = chip.dataset.filter || "all";

        chips.forEach((item) => item.classList.remove("active"));
        chip.classList.add("active");

        items.forEach((card) => {
          const category = card.dataset.category || "";
          const categories = category.split(" ").filter(Boolean);
          const visible = filter === "all" || categories.includes(filter);
          card.hidden = !visible;
        });
      });
    });
  });

  const accordionTriggers = document.querySelectorAll(".accordion-trigger");
  accordionTriggers.forEach((trigger) => {
    trigger.addEventListener("click", () => {
      const panelId = trigger.getAttribute("data-accordion-target");
      const panel = panelId ? document.getElementById(panelId) : null;
      const isExpanded = trigger.getAttribute("aria-expanded") === "true";

      trigger.setAttribute("aria-expanded", String(!isExpanded));
      const icon = trigger.querySelector("span:last-child");
      if (icon) {
        icon.textContent = isExpanded ? "+" : "-";
      }

      if (!panel) return;
      panel.style.maxHeight = isExpanded ? "0" : `${panel.scrollHeight}px`;
    });
  });

  const floatItems = document.querySelectorAll("[data-float]");
  if (floatItems.length) {
    window.addEventListener("mousemove", (event) => {
      const xRatio = event.clientX / window.innerWidth - 0.5;
      const yRatio = event.clientY / window.innerHeight - 0.5;

      floatItems.forEach((item) => {
        const depth = Number(item.getAttribute("data-float")) || 8;
        const x = -(xRatio * depth);
        const y = -(yRatio * depth);
        item.style.transform = `translate3d(${x}px, ${y}px, 0)`;
      });
    });
  }

  const setupImageFallbacks = () => {
    const fallbackSrc = "/assets/c4web/images/image-fallback.svg";
    const contentImages = document.querySelectorAll("main img, .site-footer img");

    contentImages.forEach((img) => {
      if (!(img instanceof HTMLImageElement)) return;

      if (!img.getAttribute("loading")) {
        img.setAttribute("loading", "lazy");
      }
      img.decoding = "async";

      img.addEventListener("error", () => {
        if (img.dataset.fallbackApplied === "1") return;
        img.dataset.fallbackApplied = "1";
        img.classList.add("img-fallback");
        img.src = fallbackSrc;
      });
    });
  };

  setupImageFallbacks();

  const leadForms = document.querySelectorAll("[data-lead-form]");
  leadForms.forEach((form) => {
    form.addEventListener("submit", async (event) => {
      event.preventDefault();

      const submitButton = form.querySelector("button[type='submit']");
      const statusEl = form.querySelector("[data-form-status]");
      const setStatus = (message, type = "") => {
        if (!statusEl) return;
        statusEl.textContent = message;
        statusEl.classList.remove("success", "error");
        if (type) {
          statusEl.classList.add(type);
        }
      };

      if (submitButton) {
        submitButton.disabled = true;
      }
      setStatus("جاري إرسال الطلب...");

      const extractServerMessage = (payload) => {
        const raw = payload?._server_messages;
        if (!raw) return "";

        try {
          const messages = JSON.parse(raw);
          if (!Array.isArray(messages) || !messages.length) return "";

          const parsed = JSON.parse(messages[0] || "{}");
          const clean = String(parsed?.message || "")
            .replace(/<[^>]*>/g, " ")
            .replace(/\s+/g, " ")
            .trim();
          return clean;
        } catch (_error) {
          return "";
        }
      };

      try {
        const formData = new FormData(form);
        const body = new URLSearchParams();

        formData.forEach((value, key) => {
          const normalizedValue = String(value).trim();
          body.append(key, normalizedValue);
        });
        body.append("source_page", window.location.pathname || "/contact");

        const csrfToken = window.csrf_token || window.frappe?.csrf_token || "";
        const headers = {
          "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        };
        if (csrfToken) {
          headers["X-Frappe-CSRF-Token"] = csrfToken;
        }

        const response = await fetch("/api/method/c4web.api.create_website_lead", {
          method: "POST",
          headers,
          body: body.toString(),
          credentials: "same-origin",
        });

        const payload = await response.json().catch(() => ({}));
        if (!response.ok || payload.exc) {
          const detailedServerMessage = extractServerMessage(payload);
          const errorMessage =
            detailedServerMessage || payload?.message || "تعذر إرسال الطلب حاليا. حاول مرة أخرى.";
          throw new Error(errorMessage);
        }

        form.reset();
        setStatus("تم إنشاء Lead جديد بنجاح. سيتواصل فريقنا معك قريبا.", "success");
      } catch (error) {
        const message = error instanceof Error ? error.message : "تعذر إرسال الطلب حاليا. حاول مرة أخرى.";
        setStatus(message, "error");
      } finally {
        if (submitButton) {
          submitButton.disabled = false;
        }
      }
    });
  });

  const year = document.querySelector("[data-current-year]");
  if (year) {
    year.textContent = String(new Date().getFullYear());
  }

  if (!document.querySelector(".wa-float")) {
    const waLink = document.createElement("a");
    waLink.className = "wa-float";
    waLink.href = "https://wa.me/201006676145";
    waLink.target = "_blank";
    waLink.rel = "noopener noreferrer";
    waLink.setAttribute("aria-label", "تواصل عبر واتساب");
    waLink.innerHTML = '<img src="/files/WhatsApp.svg.webp" alt="واتساب" loading="lazy" />';
    body.appendChild(waLink);
  }
});
