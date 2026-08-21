(function ($) {
    "use strict";
    /*=================================
    JS Index Here
    ==================================*/
    /*
    01. On Load Function
    02. Preloader
    03. Mobile Menu Active
    04. Sticky fix
    05. Scroll To Top
    06. Counter Up
    07. Global Slider
    08. Magnific Popup
    09. Filter
    10. Product Image Slide
    11. Modal
  */
    /*=================================
    JS Index End
    ==================================*/
    /*

    /*---------- 01 On Load Function ----------*/
    $(window).on("load", function () {
        $(".preloader").fadeOut(1000);
        sessionStorage.setItem('dapVisited', '1');
    });

    /*---------- 02 Preloader ----------*/
    if ($(".preloader").length > 0) {
        $(".preloaderCls").each(function () {
            $(this).on("click", function (e) {
                e.preventDefault();
                $(".loader").css("display", "none");
                $('.loader').delay(1000).fadeOut('6000');
            });
        });
    }

    /*----------------- 03 Mobile Menu Humbagur -------------*/
    $.fn.asmobilemenu = function(options) {
        var opt = $.extend({
                menuToggleBtn: ".das-menu-toggle",
                bodyToggleClass: "das-body-visible",
                subMenuClass: "das-submenu",
                subMenuParent: "das-item-has-children",
                subMenuParentToggle: "das-active",
                meanExpandClass: "das-mean-expand",
                appendElement: '<span class="das-mean-expand"></span>',
                subMenuToggleClass: "das-open",
                toggleSpeed: 400,
            },
            options
        );
        return this.each(function() {
            var menu = $(this); // Select menu
            // Menu Show & Hide
            function menuToggle() {
                menu.toggleClass(opt.bodyToggleClass);
                // collapse submenu on menu hide or show
                var subMenu = "." + opt.subMenuClass;
                $(subMenu).each(function() {
                    if ($(this).hasClass(opt.subMenuToggleClass)) {
                        $(this).removeClass(opt.subMenuToggleClass);
                        $(this).css("display", "none");
                        $(this).parent().removeClass(opt.subMenuParentToggle);
                    }
                });
            }
            // Class Set Up for every submenu
            menu.find("li").each(function() {
                var submenu = $(this).find("ul");
                submenu.addClass(opt.subMenuClass);
                submenu.css("display", "none");
                submenu.parent().addClass(opt.subMenuParent);
                submenu.prev("a").append(opt.appendElement);
                submenu.next("a").append(opt.appendElement);
            });
            // Toggle Submenu
            function toggleDropDown($element) {
                if ($($element).next("ul").length > 0) {
                    $($element).parent().toggleClass(opt.subMenuParentToggle);
                    $($element).next("ul").slideToggle(opt.toggleSpeed);
                    $($element).next("ul").toggleClass(opt.subMenuToggleClass);
                } else if ($($element).prev("ul").length > 0) {
                    $($element).parent().toggleClass(opt.subMenuParentToggle);
                    $($element).prev("ul").slideToggle(opt.toggleSpeed);
                    $($element).prev("ul").toggleClass(opt.subMenuToggleClass);
                }
            }
            // Submenu toggle Button
            var expandToggler = "." + opt.meanExpandClass;
            $(expandToggler).each(function() {
                $(this).on("click", function(e) {
                    e.preventDefault();
                    toggleDropDown($(this).parent());
                });
            });
            // Menu Show & Hide On Toggle Btn click
            $(opt.menuToggleBtn).each(function() {
                $(this).on("click", function() {
                    menuToggle();
                });
            });
            // Hide Menu On out side click
            menu.on("click", function(e) {
                e.stopPropagation();
                menuToggle();
            });
            // Stop Hide full menu on menu click
            menu.find("div").on("click", function(e) {
                e.stopPropagation();
            });
        });
    };
    $(".das-menu-wrapper").asmobilemenu();

    if ($(".side-box-bar").length) {
        $(".side-box-bar").on("click", function(e) {
            e.preventDefault();
            $(".canvas-wrapper").toggleClass("active");
            $("body").toggleClass("locked");
        });
    }

    //----------------- 04 Sticky Menu -------------------------/////
    var num = 400;
    $(window).bind('scroll', function () {
        if ($(window).scrollTop() > num) {
            $('.stickey-wrapper').addClass('fixed');
        } else {
            $('.stickey-wrapper').removeClass('fixed');
        }
    });

    ///----------------------------- 05 Scroll To Top---------------------------------------/
    $(window).scroll(function () {
        if ($(this).scrollTop()) {
            $('.to-top').fadeIn(2000);
        } else {
            $('.to-top').fadeOut(1000);
        }
    });
    $(".to-top").click(function () {
        $("html, body").animate({ scrollTop: 500 }, 200);
    });


    // ------------------------------------------- 06 Counter JS ------------------------------//
    $('.counter').counterUp({
        delay: 10,
        time: 5000
    });

    // ------------------------- 07 Global Slider ------------------------- //
    $('.project-slider-wrap').slick({
        centerMode: true,
        centerPadding: '60px',
        slidesToShow: 2,
        margin: 20,
        dots: false,
        arrows: false,
        responsive: [
            {
                breakpoint: 1024,
                settings: {
                    arrows: false,
                    centerMode: true,
                    centerPadding: '40px',
                    slidesToShow: 1
                },
                breakpoint: 1140,
                settings: {
                    arrows: false,
                    centerMode: true,
                    centerPadding: '40px',
                    slidesToShow: 1
                }
            },
            {
                breakpoint: 776,
                settings: {
                    centerMode: false,
                    slidesToShow: 1
                }
            },

        ]
    });

    // Slick Slider 2 //////////////////////////////////
    $('.home-one-hero-wrapper').slick({
        slidesToShow: 1,
        dots: true,
        arrows: false,
        fade: true,
        autoplay: true,
        speed: 1500,
    });

    // Life and Work at DAP Slick Slider
    $('.dap-life-slider-track').slick({
      centerMode: true,
      centerPadding: '40px',
      slidesToShow: 3,
      dots: true,
      arrows: true,
      autoplay: true,
      autoplaySpeed: 2500,
      responsive: [
        {
          breakpoint: 992,
          settings: {
            slidesToShow: 2,
            centerPadding: '20px',
          }
        },
        {
          breakpoint: 600,
          settings: {
            slidesToShow: 1,
            centerPadding: '0px',
          }
        }
      ]
    });

    // ------------------------- 08 Magnific Popup ------------------------- //
    if ($(".image-link").length){
        $(document).ready(function() {
            $('.image-link').magnificPopup({
                type:'image',
                gallery:{
                    enabled:true,
                }
            });

        });
    }

    // ---------------------------- 09  Fillter ------------------------------------////
    $('.filter-active').imagesLoaded(function () {
        var $filter = '.filter-active',
            $filterItem = '.filter-item',
            $filterMenu = '.filter-menu-active';

        if ($($filter).length > 0) {
            var $grid = $($filter).isotope({
                itemSelector: $filterItem,
                filter: '.cat1',
                masonry: {
                    // use outer width of grid-sizer for columnWidth
                    columnWidth: 1
                }
            });

            // filter items on button click
            $($filterMenu).on('click', 'button', function () {
                var filterValue = $(this).attr('data-filter');
                $grid.isotope({
                    filter: filterValue
                });
            });

            // Menu Active Class
            $($filterMenu).on('click', 'button', function (event) {
                event.preventDefault();
                $(this).addClass('active');
                $(this).siblings('.active').removeClass('active');
            });
        };
    });

    // ------------------------- 10 Product Image Slide ------------------------- //
    document.addEventListener('DOMContentLoaded', () => {
        const imgBtns = Array.from(document.querySelectorAll('.product-small-img a'));
        const productImgContainer = document.querySelector('.product-img');
        let imgId = 1;

        imgBtns.forEach(imgItem => {
            imgItem.addEventListener('click', event => {
                event.preventDefault();
                imgId = parseInt(imgItem.dataset.id, 10);
                slideImage();
            });
        });

        function slideImage() {
            if (!productImgContainer) return;

            const imgs = productImgContainer.querySelectorAll('img');
            const displayWidth = imgs.length > 0 ? imgs[0].clientWidth : 0;

            productImgContainer.style.transform = `translate(${- (imgId - 1) * displayWidth}px)`;
        }

        // Debounce function to limit the rate of resize events
        function debounce(func, wait) {
            let timeout;
            return function(...args) {
                clearTimeout(timeout);
                timeout = setTimeout(() => func.apply(this, args), wait);
            };
        }

        window.addEventListener('resize', debounce(slideImage, 100));
    });

    //----------------- 11 Modal --------------------///
    var myModal = document.getElementById('myModal')
    var myInput = document.getElementById('myInput')



})(jQuery);

// Enhanced Client Slider with Interactive Effects
$(document).ready(function() {
    // Client Slider Enhancement
    if ($('#clientSlider').length > 0) {
        const slider = $('#clientSlider');
        const slides = slider.find('.client-slide');
        
        // Add random delay to each slide for staggered animation
        slides.each(function(index) {
            $(this).css('animation-delay', (index * 0.1) + 's');
        });
        
        // Add mouse tracking effect
        slider.on('mousemove', function(e) {
            const rect = this.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;
            
            // Move slides slightly based on mouse position
            slides.each(function(index) {
                const offset = (x / rect.width - 0.5) * 10;
                $(this).css('transform', `translateX(${offset}px)`);
            });
        });
        
        // Reset position on mouse leave
        slider.on('mouseleave', function() {
            slides.css('transform', 'translateX(0)');
        });
        
        // Add click effect
        slides.on('click', function() {
            $(this).addClass('clicked');
            setTimeout(() => {
                $(this).removeClass('clicked');
            }, 300);
        });
    }
});

// Add CSS for click effect
const clickEffectCSS = `
.client-slide.clicked {
    animation: clickPulse 0.3s ease;
}

@keyframes clickPulse {
    0% { transform: scale(1); }
    50% { transform: scale(1.1); }
    100% { transform: scale(1); }
}
`;

// Inject the CSS
$('<style>').prop('type', 'text/css').html(clickEffectCSS).appendTo('head');



// Open Positions Section Enhancements
document.addEventListener('DOMContentLoaded', function() {
    // Animate position cards on scroll
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate');
            }
        });
    }, observerOptions);

    // Observe all position cards
    const positionCards = document.querySelectorAll('.position-card');
    positionCards.forEach(card => {
        observer.observe(card);
    });

    // Add hover effects for better interactivity
    positionCards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-10px) scale(1.02)';
        });

        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0) scale(1)';
        });
    });

    // Smooth scroll for apply buttons
    const applyButtons = document.querySelectorAll('.apply-btn');
    applyButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            // Add a small delay to show the click effect
            this.style.transform = 'translateY(-2px) scale(0.98)';
            setTimeout(() => {
                this.style.transform = 'translateY(-2px) scale(1)';
            }, 150);
        });
    });

    // Add category filtering functionality (optional enhancement)
    const categoryButtons = document.querySelectorAll('[data-category-filter]');
    positionCards = document.querySelectorAll('.position-card');

    if (categoryButtons.length > 0) {
        categoryButtons.forEach(button => {
            button.addEventListener('click', function() {
                const category = this.getAttribute('data-category-filter');
                
                // Remove active class from all buttons
                categoryButtons.forEach(btn => btn.classList.remove('active'));
                // Add active class to clicked button
                this.classList.add('active');

                // Filter position cards
                positionCards.forEach(card => {
                    if (category === 'all' || card.getAttribute('data-category') === category) {
                        card.style.display = 'flex';
                        card.style.animation = 'slideInUp 0.6s ease-out';
                    } else {
                        card.style.display = 'none';
                    }
                });
            });
        });
    }

    // Add search functionality (optional enhancement)
    const searchInput = document.querySelector('#position-search');
    if (searchInput) {
        searchInput.addEventListener('input', function() {
            const searchTerm = this.value.toLowerCase();
            
            positionCards.forEach(card => {
                const title = card.querySelector('.position-title').textContent.toLowerCase();
                const description = card.querySelector('.position-description').textContent.toLowerCase();
                
                if (title.includes(searchTerm) || description.includes(searchTerm)) {
                    card.style.display = 'flex';
                    card.style.animation = 'slideInUp 0.6s ease-out';
                } else {
                    card.style.display = 'none';
                }
            });
        });
    }

    // Add loading animation for apply buttons
    const applyButtons = document.querySelectorAll('.apply-btn');
    applyButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            const originalText = this.innerHTML;
            this.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Opening Email...';
            this.style.pointerEvents = 'none';
            
            // Reset after 2 seconds
            setTimeout(() => {
                this.innerHTML = originalText;
                this.style.pointerEvents = 'auto';
            }, 2000);
        });
    });

    // Add parallax effect to section header
    const sectionHeader = document.querySelector('.section-header');
    if (sectionHeader) {
        window.addEventListener('scroll', function() {
            const scrolled = window.pageYOffset;
            const rate = scrolled * -0.5;
            sectionHeader.style.transform = `translateY(${rate}px)`;
        });
    }

    // Add counter animation for statistics (if any)
    const counters = document.querySelectorAll('.counter');
    const counterObserver = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const counter = entry.target;
                const target = parseInt(counter.getAttribute('data-target'));
                const duration = 2000; // 2 seconds
                const increment = target / (duration / 16); // 60fps
                let current = 0;

                const updateCounter = () => {
                    if (current < target) {
                        current += increment;
                        counter.textContent = Math.floor(current);
                        requestAnimationFrame(updateCounter);
                    } else {
                        counter.textContent = target;
                    }
                };

                updateCounter();
                counterObserver.unobserve(counter);
            }
        });
    }, { threshold: 0.5 });

    document.querySelectorAll('.counter').forEach(counter => {
        counterObserver.observe(counter);
    });
});

// Add smooth scrolling for anchor links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

// Add keyboard navigation for position cards
document.addEventListener('keydown', function(e) {
    if (e.key === 'Tab') {
        const focusedElement = document.activeElement;
        if (focusedElement.classList.contains('position-card')) {
            focusedElement.style.outline = '2px solid #377f4b';
            focusedElement.style.outlineOffset = '2px';
        }
    }
});

// Remove outline when clicking
document.addEventListener('click', function(e) {
    const focusedElement = document.activeElement;
    if (focusedElement && focusedElement.style.outline) {
        focusedElement.style.outline = 'none';
    }
});

// Simple dropdown click functionality
document.addEventListener("DOMContentLoaded", function() {
    document.querySelectorAll(".modern-navbar .dropdown-toggle").forEach(toggle => {
        toggle.addEventListener("click", function(e) {
            e.preventDefault();
            const parent = this.closest(".nav-item.dropdown");
            parent.classList.toggle("show");
        });
    });
});
