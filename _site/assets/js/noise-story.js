/**
 * NYC Noise Story Interactivity Scripts
 * Enhances the visualization experience with tooltips, highlights, and responsive elements
 */

document.addEventListener("DOMContentLoaded", function () {
  // Initialize smooth scrolling for anchor links
  document.querySelectorAll('a[href^="#"]').forEach((anchor) => {
    anchor.addEventListener("click", function (e) {
      e.preventDefault();
      const targetId = this.getAttribute("href");
      const targetElement = document.querySelector(targetId);

      if (targetElement) {
        window.scrollTo({
          top: targetElement.offsetTop - 60,
          behavior: "smooth",
        });

        document.querySelectorAll(".progress-nav a").forEach((navItem) => {
          navItem.classList.remove("active");
        });

        const activeNavItem = document.querySelector(
          `.progress-nav a[href="${targetId}"]`
        );
        if (activeNavItem) {
          activeNavItem.classList.add("active");
        }

        history.pushState(null, null, targetId);
      }
    });
  });

  // Enhanced Intersection Observer for fade-in animations with sequence
  const fadeElements = document.querySelectorAll(".fade-in");
  const slideGroups = {};
  fadeElements.forEach((element) => {
    const parentSlide = element.closest(".slide");
    if (parentSlide) {
      const slideId = parentSlide.id;
      if (!slideGroups[slideId]) {
        slideGroups[slideId] = [];
      }
      slideGroups[slideId].push(element);
    }
  });

  const fadeObserver = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          const element = entry.target;
          const parentSlideId = element.closest(".slide")?.id;

          if (parentSlideId && slideGroups[parentSlideId]) {
            const elementsInSlide = slideGroups[parentSlideId];
            const index = elementsInSlide.indexOf(element);

            if (index !== -1) {
              const delay = index * 100;
              setTimeout(() => {
                element.classList.add("visible");
              }, delay);
            } else {
              element.classList.add("visible");
            }
          } else {
            element.classList.add("visible");
          }

          fadeObserver.unobserve(element);
        }
      });
    },
    {
      threshold: 0.15,
      rootMargin: "0px 0px -10% 0px",
    }
  );

  fadeElements.forEach((element) => {
    fadeObserver.observe(element);
  });

  // Progress navigation observer
  const slides = document.querySelectorAll(".slide");
  const slideObserver = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          const id = entry.target.getAttribute("id");
          const navItem = document.querySelector(
            `.progress-nav a[href="#${id}"]`
          );

          if (navItem) {
            document.querySelectorAll(".progress-nav a").forEach((item) => {
              item.classList.remove("active");
            });
            navItem.classList.add("active");
            history.replaceState(null, null, `#${id}`);

            const timelinePoints = document.querySelectorAll(".timeline-point");
            timelinePoints.forEach((point) => {
              const pointTarget = point.getAttribute("data-target");
              point.classList.toggle("active", pointTarget === id);
            });
          }
        }
      });
    },
    {
      threshold: 0.6,
      rootMargin: "-10% 0px -40% 0px",
    }
  );

  slides.forEach((slide) => {
    slideObserver.observe(slide);
  });

  // Modal/Lightbox for visualizations
  const vizContainers = document.querySelectorAll(".viz-container");
  const modal = document.querySelector(".modal");
  const modalContent = document.querySelector(".modal-content");
  const closeModal = document.querySelector(".close-modal");

  if (vizContainers && modal && modalContent && closeModal) {
    vizContainers.forEach((container) => {
      const iframe = container.querySelector("iframe");
      const pngImage = container.querySelector('iframe[src*=".png"]');

      if (iframe && !pngImage) {
        const expandButton = document.createElement("button");
        expandButton.innerHTML = '<i class="fas fa-expand"></i>';
        expandButton.className = "viz-expand-button";
        expandButton.setAttribute("aria-label", "Expand visualization");
        expandButton.onclick = function () {
          openModal(iframe.cloneNode(true));
        };
        container.appendChild(expandButton);
      }

      const caption = container.querySelector(".viz-caption");
      if (caption) {
        caption.addEventListener("mouseover", function () {
          this.style.backgroundColor = "rgba(0, 57, 166, 0.9)";
        });
        caption.addEventListener("mouseout", function () {
          this.style.backgroundColor = "";
        });
      }
    });

    modal.addEventListener("click", function (e) {
      if (e.target === modal) {
        closeModalHandler();
      }
    });

    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && modal.classList.contains("show")) {
        closeModalHandler();
      }
    });

    function closeModalHandler() {
      modal.classList.remove("show");
      setTimeout(() => {
        document.body.style.overflow = "";
      }, 300);
    }
  }

  // Timeline navigation
  const timelinePoints = document.querySelectorAll(".timeline-point");
  timelinePoints.forEach((point) => {
    point.addEventListener("click", function () {
      const targetPhase = this.getAttribute("data-target");
      const targetElement = document.querySelector(`#${targetPhase}`);

      if (targetElement) {
        window.scrollTo({
          top: targetElement.offsetTop - 60,
          behavior: "smooth",
        });

        timelinePoints.forEach((p) => p.classList.remove("active"));
        this.classList.add("active");
      }
    });

    // Add hover effect
    point.addEventListener("mouseenter", function () {
      const label = this.querySelector(".timeline-label");
      if (label) {
        label.style.transform = "scale(1.1)";
        label.style.fontWeight = "bold";
      }
    });

    point.addEventListener("mouseleave", function () {
      const label = this.querySelector(".timeline-label");
      if (label) {
        label.style.transform = "";
        label.style.fontWeight = "";
      }
    });
  });

  // Initialize based on URL hash on page load
  if (location.hash) {
    const targetElement = document.querySelector(location.hash);
    if (targetElement) {
      setTimeout(() => {
        window.scrollTo({
          top: targetElement.offsetTop - 60,
          behavior: "auto",
        });

        // Activate the corresponding navigation
        const navItem = document.querySelector(
          `.progress-nav a[href="${location.hash}"]`
        );
        if (navItem) {
          navItem.classList.add("active");
        }

        // Activate timeline point if applicable
        const timelinePoints = document.querySelectorAll(".timeline-point");
        timelinePoints.forEach((point) => {
          const pointTarget = point.getAttribute("data-target");
          if (pointTarget === location.hash.substring(1)) {
            point.classList.add("active");
          }
        });
      }, 300);
    }
  }

  // Add scroll progress indicator
  const progressBar = document.createElement("div");
  progressBar.className = "scroll-progress-bar";
  document.body.appendChild(progressBar);

  window.addEventListener("scroll", () => {
    const windowHeight =
      document.documentElement.scrollHeight - window.innerHeight;
    const scrolled = (window.scrollY / windowHeight) * 100;
    progressBar.style.width = scrolled + "%";
  });

  // Create tooltip element that will be reused
  const tooltip = document.createElement("div");
  tooltip.className = "viz-tooltip";
  document.body.appendChild(tooltip);

  // Initialize interactive visualizations
  initializeVisualizationEnhancements();
  initializeModalLightbox();
  initializeBoroughHighlighting();
  initializeScrollEffects();
});

/**
 * Enhances the visualization containers with interactivity
 */
function initializeVisualizationEnhancements() {
  // Find all visualization containers
  const vizContainers = document.querySelectorAll(".viz-container");

  vizContainers.forEach((container) => {
    // Check if the container has an iframe and not a PNG image
    const iframe = container.querySelector("iframe");
    const pngImage = container.querySelector('iframe[src*=".png"]');

    // Only add expand functionality for iframes that are not PNG images
    if (iframe && !pngImage) {
      // Add expand functionality for visualizations
      const expandButton = document.createElement("button");
      expandButton.innerHTML = '<i class="fas fa-expand"></i>';
      expandButton.className = "viz-expand-button";
      expandButton.setAttribute("aria-label", "Expand visualization");
      expandButton.onclick = function () {
        openModal(iframe.cloneNode(true));
      };
      container.appendChild(expandButton);
    }

    // Add hover effect to visualization captions
    const caption = container.querySelector(".viz-caption");
    if (caption) {
      caption.addEventListener("mouseover", function () {
        this.style.backgroundColor = "rgba(0, 57, 166, 0.9)";
      });
      caption.addEventListener("mouseout", function () {
        this.style.backgroundColor = "";
      });
    }
  });

  // Add interactive legends if they exist
  initializeInteractiveLegends();
}

/**
 * Sets up the modal lightbox for expanded visualizations
 */
function initializeModalLightbox() {
  const modal = document.querySelector(".modal");
  const modalContent = document.querySelector(".modal-content");
  const closeButton = document.querySelector(".close-modal");

  if (!modal || !modalContent || !closeButton) return;

  closeButton.onclick = function () {
    modal.style.display = "none";
    modalContent.innerHTML = '<span class="close-modal">&times;</span>';
  };

  window.onclick = function (event) {
    if (event.target === modal) {
      modal.style.display = "none";
      modalContent.innerHTML = '<span class="close-modal">&times;</span>';
    }
  };
}

/**
 * Opens the modal with the provided content
 */
function openModal(content) {
  const modal = document.querySelector(".modal");
  const modalContent = document.querySelector(".modal-content");

  if (!modal || !modalContent) return;

  // Clear existing content except close button
  const closeButton = modalContent.querySelector(".close-modal");
  modalContent.innerHTML = "";
  modalContent.appendChild(closeButton);

  // Add the new content
  modalContent.appendChild(content);

  // Show modal
  modal.style.display = "flex";
}

/**
 * Makes borough tags and references interactive
 */
function initializeBoroughHighlighting() {
  // Borough classes to highlight
  const boroughs = [
    "manhattan",
    "brooklyn",
    "queens",
    "bronx",
    "staten-island",
  ];

  // Add hover effects to borough tags
  boroughs.forEach((borough) => {
    const tags = document.querySelectorAll(`.location-tag.${borough}`);

    tags.forEach((tag) => {
      tag.addEventListener("mouseover", function () {
        // Highlight all mentions of this borough in the text
        const mentions = document.querySelectorAll(`.${borough}-mention`);
        mentions.forEach((mention) => {
          mention.classList.add(`${borough}-highlight`);
        });
      });

      tag.addEventListener("mouseout", function () {
        // Remove highlighting
        const mentions = document.querySelectorAll(`.${borough}-mention`);
        mentions.forEach((mention) => {
          mention.classList.remove(`${borough}-highlight`);
        });
      });
    });
  });
}

/**
 * Sets up interactive legends for visualizations
 */
function initializeInteractiveLegends() {
  const legends = document.querySelectorAll(".viz-legend");

  legends.forEach((legend) => {
    const items = legend.querySelectorAll(".legend-item");
    const vizContainer = legend.closest(".viz-container");
    const iframe = vizContainer ? vizContainer.querySelector("iframe") : null;

    items.forEach((item) => {
      item.addEventListener("click", function () {
        // Toggle active/inactive class
        this.classList.toggle("inactive");

        // If we have access to the iframe content, toggle visibility
        if (iframe && iframe.contentDocument) {
          const category = this.getAttribute("data-category");
          const elements = iframe.contentDocument.querySelectorAll(
            `.${category}`
          );

          elements.forEach((el) => {
            el.style.opacity = this.classList.contains("inactive")
              ? "0.2"
              : "1";
          });
        }
      });
    });
  });
}

/**
 * Adds scroll-based reveal effects for content
 */
function initializeScrollEffects() {
  // Find all elements with fade-in class
  const fadeElements = document.querySelectorAll(".fade-in");

  // Add observer for scroll animations
  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add("visible");
          // Stop observing after it's visible
          observer.unobserve(entry.target);
        }
      });
    },
    {
      threshold: 0.1,
    }
  );

  // Observe each fade element
  fadeElements.forEach((element) => {
    observer.observe(element);
  });
}

/**
 * Helper function to show tooltip with data
 */
function showTooltip(event, content) {
  const tooltip = document.querySelector(".viz-tooltip");

  if (!tooltip) return;

  tooltip.innerHTML = content;
  tooltip.style.left = `${event.pageX + 15}px`;
  tooltip.style.top = `${event.pageY + 15}px`;
  tooltip.classList.add("active");
}

/**
 * Helper function to hide tooltip
 */
function hideTooltip() {
  const tooltip = document.querySelector(".viz-tooltip");

  if (!tooltip) return;

  tooltip.classList.remove("active");
}
