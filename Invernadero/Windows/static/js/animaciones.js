// Animaciones con Intersection Observer para efectos al hacer scroll
document.addEventListener('DOMContentLoaded', function() {
    // Configuración del Intersection Observer
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    // Función para animar elementos al entrar en viewport
    function animateOnScroll(entries, observer) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const element = entry.target;

                // Agregar clases de animación basadas en data attributes
                const animationType = element.dataset.animation || 'animate-fade-in';
                const delay = element.dataset.delay || '0';

                // Aplicar animación con delay si existe
                if (delay > 0) {
                    setTimeout(() => {
                        element.classList.add(animationType);
                        element.classList.add('animate-duration-1000');
                        element.classList.remove('opacity-0');
                    }, delay);
                } else {
                    element.classList.add(animationType);
                    element.classList.add('animate-duration-1000');
                    element.classList.remove('opacity-0');
                }

                // Dejar de observar el elemento después de animarlo
                observer.unobserve(element);
            }
        });
    }

    // Crear el observer
    const observer = new IntersectionObserver(animateOnScroll, observerOptions);

    // Seleccionar elementos para animar
    const elementsToAnimate = document.querySelectorAll('.animate-on-scroll');
    elementsToAnimate.forEach(element => {
        // Inicialmente invisible
        element.classList.add('opacity-0');
        observer.observe(element);
    });

    // Animaciones específicas para cards con stagger
    const cards = document.querySelectorAll('.card, .equipment-card');
    cards.forEach((card, index) => {
        card.classList.add('animate-on-scroll');
        card.dataset.animation = 'animate-fade-in-up';
        card.dataset.delay = index * 200; // Delay escalonado
    });

    // Animaciones para secciones
    const sections = document.querySelectorAll('section, main');
    sections.forEach(section => {
        if (!section.classList.contains('hero')) { // Hero ya tiene animación
            section.classList.add('animate-on-scroll');
            section.dataset.animation = 'animate-fade-in';
        }
    });

    // Animaciones para footer
    const footer = document.querySelector('footer');
    if (footer) {
        footer.classList.add('animate-on-scroll');
        footer.dataset.animation = 'animate-fade-in-up';
    }

    // Animaciones para iconos (bounce on hover)
    const icons = document.querySelectorAll('.icono, .fas, .far, .fab');
    icons.forEach(icon => {
        icon.classList.add('transition-transform', 'duration-300', 'hover:animate-bounce');
    });


    // Animación para navbar al cargar página
    const navbar = document.querySelector('.navbar');
    if (navbar) {
        navbar.classList.add('animate-fade-in-down');
        navbar.classList.add('animate-duration-1000');
    }

    // Función para animaciones de carga inicial
    function initialAnimations() {
        // Animar logo
        const logo = document.querySelector('.logo');
        if (logo) {
            logo.classList.add('animate-fade-in');
            logo.classList.add('animate-duration-1500');
        }

        // Animar menú items con delay
        const menuItems = document.querySelectorAll('.menu a');
        menuItems.forEach((item, index) => {
            item.classList.add('animate-fade-in-down');
            item.style.animationDelay = `${index * 100}ms`;
            item.classList.add('animate-duration-800');
        });
    }

    // Ejecutar animaciones iniciales
    initialAnimations();

    // Función para parallax en backgrounds
    function parallaxEffect() {
        const parallaxElements = document.querySelectorAll('.parallax-bg');

        if (parallaxElements.length > 0) {
            window.addEventListener('scroll', () => {
                const scrolled = window.pageYOffset;
                const rate = scrolled * 0.5;

                parallaxElements.forEach(element => {
                    element.style.transform = `translateY(${rate}px)`;
                });
            });
        }

        // Parallax para imágenes hero
        const heroImage = document.querySelector('.hero img');
        if (heroImage) {
            window.addEventListener('scroll', () => {
                const scrolled = window.pageYOffset;
                const rate = scrolled * -0.3;
                heroImage.style.transform = `translateY(${rate}px)`;
            });
        }
    }

    // Activar parallax
    parallaxEffect();
});

// Función para animaciones de carga de página
window.addEventListener('load', function() {
    // Agregar clase para animación completa de carga
    document.body.classList.add('animate-fade-in');
    document.body.classList.add('animate-duration-500');
});