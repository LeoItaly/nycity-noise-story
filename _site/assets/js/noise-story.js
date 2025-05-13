document.addEventListener("DOMContentLoaded", function () {
  // Initialize smooth scrolling for anchor links
  document.querySelectorAll('a[href^="#"]').forEach((anchor) => {
    anchor.addEventListener("click", function (e) {
      e.preventDefault();
      const targetId = this.getAttribute("href");
      const targetElement = document.querySelector(targetId);

      if (targetElement) {
        // Add smoother scrolling with easing
        window.scrollTo({
          top: targetElement.offsetTop - 60, // Add offset for header
          behavior: "smooth",
        });

        // Update active state in navigation
        document.querySelectorAll(".progress-nav a").forEach((navItem) => {
          navItem.classList.remove("active");
        });

        const activeNavItem = document.querySelector(
          `.progress-nav a[href="${targetId}"]`
        );
        if (activeNavItem) {
          activeNavItem.classList.add("active");
        }

        // Update URL hash without scrolling
        history.pushState(null, null, targetId);
      }
    });
  });

  // Enhanced Intersection Observer for fade-in animations with sequence
  const fadeElements = document.querySelectorAll(".fade-in");

  // Group fade elements by their parent slide
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

          // Only apply the staggered animation if we haven't seen this slide before
          if (parentSlideId && slideGroups[parentSlideId]) {
            const elementsInSlide = slideGroups[parentSlideId];
            const index = elementsInSlide.indexOf(element);

            // Apply staggered delay based on position in the parent slide
            if (index !== -1) {
              const delay = index * 100; // 100ms stagger
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
      rootMargin: "0px 0px -10% 0px", // Trigger a bit earlier
    }
  );

  fadeElements.forEach((element) => {
    fadeObserver.observe(element);
  });

  // Improved Intersection Observer for progress navigation
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

            // Update URL hash without scrolling
            history.replaceState(null, null, `#${id}`);

            // Also update timeline if applicable
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

  // Enhanced Modal/Lightbox for enlarging visualizations
  const vizContainers = document.querySelectorAll(".viz-container");
  const modal = document.querySelector(".modal");
  const modalContent = document.querySelector(".modal-content");
  const closeModal = document.querySelector(".close-modal");

  if (vizContainers && modal && modalContent && closeModal) {
    vizContainers.forEach((container) => {
      // Skip containers with iframes
      if (container.querySelector("iframe")) {
        return;
      }

      // Add a visible indicator that the visualization is clickable
      container.classList.add("clickable");

      const zoomIcon = document.createElement("div");
      zoomIcon.className = "zoom-icon";
      zoomIcon.innerHTML = '<i class="fas fa-search-plus"></i>';
      container.appendChild(zoomIcon);

      container.addEventListener("click", function () {
        const vizContent = this.innerHTML;
        modalContent.innerHTML =
          vizContent + '<span class="close-modal">&times;</span>';
        document.body.style.overflow = "hidden"; // Prevent scrolling
        modal.classList.add("show");

        document
          .querySelector(".close-modal")
          .addEventListener("click", function (e) {
            e.stopPropagation();
            closeModalHandler();
          });
      });
    });

    // Close modal when clicking outside the content
    modal.addEventListener("click", function (e) {
      if (e.target === modal) {
        closeModalHandler();
      }
    });

    // Close modal with Escape key
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && modal.classList.contains("show")) {
        closeModalHandler();
      }
    });

    function closeModalHandler() {
      modal.classList.remove("show");
      setTimeout(() => {
        document.body.style.overflow = ""; // Re-enable scrolling
      }, 300); // Wait for animation
    }
  }

  // Enhanced Timeline navigation
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
});
