/*-------------------------------------------------------------------------------------------*
 *                                    LAYOUT JAVASCRIPT                                      *
 *-------------------------------------------------------------------------------------------*/

/** Core script to handle the entire theme and core functions.
 * It handles responsive layout on screen size resize or mobile device rotate. **/
var Layout = function () {

    var resBreakpointMd = App.getResponsiveBreakpoint('md');

    // Set proper height for sidebar and content. The content and sidebar height must be synced always.
    var handleSidebarAndContentHeight = function () {

        var content = $('.page-content');
        var sidebar = $('.page-sidebar');
        var header = $('.page-header');
        var footer = $('.page-footer');
        var body = $('body');
        var height;

        var headerHeight = header.outerHeight();
        var footerHeight = footer.outerHeight();

        if (App.getViewPort().width < resBreakpointMd) {
            height = App.getViewPort().height - headerHeight - footerHeight;
        } else {
            height = sidebar.height() + 20;
        }

        if ((height + headerHeight + footerHeight) <= App.getViewPort().height) {
            height = App.getViewPort().height - headerHeight - footerHeight;
        }
        content.attr('style', 'min-height:' + height + 'px');
    };

    // Handle sidebar menu
    var handleSidebarMenu = function () {

        var pageSidebarMenu = $('.page-sidebar-menu');
        var body = $('body');
        var sidebarSearch = $('.sidebar-search');

        // Handle sidebar link click
        pageSidebarMenu.on('click', 'li > a.nav-toggle, li > a > span.nav-toggle', function (e) {
            var that = $(this).closest('.nav-item').children('.nav-link');

            if (App.getViewPort().width >= resBreakpointMd && !pageSidebarMenu.attr("data-initialized") && $('body').hasClass('page-sidebar-closed') &&  that.parent('li').parent('.page-sidebar-menu').size() === 1) {
                return;
            }

            var hasSubMenu = that.next().hasClass('sub-menu');

            if (App.getViewPort().width >= resBreakpointMd && that.parents('.page-sidebar-menu-hover-submenu').size() === 1) { // Exit of hover sidebar menu
                return;
            }

            if (hasSubMenu === false) {
                if (App.getViewPort().width < resBreakpointMd && $('.page-sidebar').hasClass("in")) { // Close the menu on mobile view while loading a page
                    $('.page-header .responsive-toggler').click();
                }
                return;
            }

            if (that.next().hasClass('sub-menu always-open')) {
                return;
            }

            var parent =that.parent().parent();
            var the = that;
            var menu = pageSidebarMenu;
            var sub = that.next();

            var autoScroll = menu.data("auto-scroll");
            var slideSpeed = parseInt(menu.data("slide-speed"));
            var keepExpand = menu.data("keep-expanded");

            if (!keepExpand) {
                parent.children('li.open').children('a').children('.arrow').removeClass('open');
                parent.children('li.open').children('.sub-menu:not(.always-open)').slideUp(slideSpeed);
                parent.children('li.open').removeClass('open');
            }

            var slideOffeset = -200;

            if (sub.is(":visible")) {
                $('.arrow', the).removeClass("open");
                the.parent().removeClass("open");
                sub.slideUp(slideSpeed, function () {
                    if (autoScroll === true && body.hasClass('page-sidebar-closed') === false) {
                        if (body.hasClass('page-sidebar-fixed')) {
                            menu.slimScroll({
                                'scrollTo': (the.position()).top
                            });
                        } else {
                            App.scrollTo(the, slideOffeset);
                        }
                    }
                    handleSidebarAndContentHeight();
                });
            } else if (hasSubMenu) {
                $('.arrow', the).addClass("open");
                the.parent().addClass("open");
                sub.slideDown(slideSpeed, function () {
                    if (autoScroll === true && body.hasClass('page-sidebar-closed') === false) {
                        if (body.hasClass('page-sidebar-fixed')) {
                            menu.slimScroll({
                                'scrollTo': (the.position()).top
                            });
                        } else {
                            App.scrollTo(the, slideOffeset);
                        }
                    }
                    handleSidebarAndContentHeight();
                });
            }

            e.preventDefault();
        });

        // Handle scrolling to top on responsive menu toggler click when header is fixed for mobile view
        $(document).on('click', '.page-header-fixed-mobile .page-header .responsive-toggler', function(){
            App.scrollTop();
        });      
     
        // Handle sidebar hover effect
        handleFixedSidebarHoverEffect();

        // SEARCH FORM IN SIDEBAR */
        // Handle the search bar close
        $('.page-sidebar').on('click', '.sidebar-search .remove', function (e) {
            e.preventDefault();
            sidebarSearch.removeClass("open");
            $('.i-delete-quickSearch').removeClass('i-delete-quickSearch-closed');
        });

        // Handle the search query submit on enter press
        $('.page-sidebar .sidebar-search').on('keypress', 'input.form-control', function (e) {

            if (e.which == 13) {
                sidebarSearch.submit();
                return false;
            }
        });

        // Handle the search submit (for sidebar search and responsive mode of the header search)
        $('.sidebar-search .submit').on('click', function (e) {

            e.preventDefault();
            if (body.hasClass("page-sidebar-closed")) {
                if (sidebarSearch.hasClass('open') === false) {
                    if ($('.page-sidebar-fixed').size() === 1) {
                        $('.page-sidebar .sidebar-toggler').click(); //trigger sidebar toggle button
                    }
                    sidebarSearch.addClass("open");
                    $('.i-delete-quickSearch').addClass('i-delete-quickSearch-closed');
                } else {
                    sidebarSearch.submit();
                }
            } else {
                sidebarSearch.submit();
            }
        });

        // Handle close on body click
        if (sidebarSearch.size() !== 0) {
            $('.sidebar-search .input-group').on('click', function(e){
                e.stopPropagation();
            });

            body.on('click', function() {
                if (sidebarSearch.hasClass('open')) {
                    sidebarSearch.removeClass("open");
                    $('.i-delete-quickSearch').removeClass('i-delete-quickSearch-closed');
                }
            });
        }
    };

    // Helper function to calculate sidebar height for fixed sidebar layout.
    var _calculateFixedSidebarViewportHeight = function () {
        var sidebarHeight = App.getViewPort().height - $('.page-header').outerHeight(true);
        return sidebarHeight;
    };

    // Handle fixed sidebar
    var handleFixedSidebar = function () {
        var menu = $('.page-sidebar-menu');

        App.destroySlimScroll(menu);

        if ($('.page-sidebar-fixed').size() === 0) {
            handleSidebarAndContentHeight();
            return;
        }

        if (App.getViewPort().width >= resBreakpointMd) {
            menu.attr("data-height", _calculateFixedSidebarViewportHeight());
            App.initSlimScroll(menu);
            handleSidebarAndContentHeight();
        }
    };

    // Handle sidebar toggler to close/hide the sidebar.
    var handleFixedSidebarHoverEffect = function () {
        var body = $('body');
        if (body.hasClass('page-sidebar-fixed')) {
            $('.page-sidebar').on('mouseenter', function () {
                if (body.hasClass('page-sidebar-closed')) {
                    $(this).find('.page-sidebar-menu').removeClass('page-sidebar-menu-closed');
                }
            }).on('mouseleave', function () {
                if (body.hasClass('page-sidebar-closed')) {
                    $(this).find('.page-sidebar-menu').addClass('page-sidebar-menu-closed');
                }
            });
        }
    };

    // Handle sidebar toggler
    var handleSidebarToggler = function () {

        var body = $('body');

        if ($.cookie && $.cookie('sidebar_closed') === '1' && App.getViewPort().width >= resBreakpointMd) {
            body.addClass('page-sidebar-closed');
            $('.page-sidebar-menu').addClass('page-sidebar-menu-closed');
        }

        // Handle sidebar show/hide
        body.on('click', '.sidebar-toggler', function () {
            var sidebar = $('.page-sidebar');
            var sidebarMenu = $('.page-sidebar-menu');
            $(".sidebar-search", sidebar).removeClass("open");

            if (body.hasClass("page-sidebar-closed")) {
                body.removeClass("page-sidebar-closed");
                sidebarMenu.removeClass("page-sidebar-menu-closed");
                if ($.cookie) {
                    $.cookie('sidebar_closed', '0');
                }
            } else {
                body.addClass("page-sidebar-closed");
                sidebarMenu.addClass("page-sidebar-menu-closed");
                if (body.hasClass("page-sidebar-fixed")) {
                    sidebarMenu.trigger("mouseleave");
                }
                if ($.cookie) {
                    $.cookie('sidebar_closed', '1');
                }
            }

            $(window).trigger('resize');
        });
    };

    // Handle Bootstrap Tabs
    var handleTabs = function () {
        // Fix content height on tab click
        $('body').on('shown.bs.tab', 'a[data-toggle="tab"]', function () {
            handleSidebarAndContentHeight();
        });
    };

    // Handle 100% height elements (block, portlet, etc)
    var handle100HeightContent = function () {

        $('.full-height-content').each(function(){
            var target = $(this);
            var height;

            height = App.getViewPort().height -
                $('.page-header').outerHeight(true) -
                $('.page-footer').outerHeight(true) -
                $('.page-title').outerHeight(true) -
                $('.page-bar').outerHeight(true);

            if (target.hasClass('portlet')) {
                var portletBody = target.find('.portlet-body');

                App.destroySlimScroll(portletBody.find('.full-height-content-body')); // Destroy slim scroll

                height = height -
                    target.find('.portlet-title').outerHeight(true) -
                    parseInt(target.find('.portlet-body').css('padding-top')) -
                    parseInt(target.find('.portlet-body').css('padding-bottom')) - 5;

                if (App.getViewPort().width >= resBreakpointMd && target.hasClass("full-height-content-scrollable")) {
                    height = height - 35;
                    portletBody.find('.full-height-content-body').css('height', height);
                    App.initSlimScroll(portletBody.find('.full-height-content-body'));
                } else {
                    portletBody.css('min-height', height);
                }
            } else {
               App.destroySlimScroll(target.find('.full-height-content-body')); // Destroy slim scroll

                if (App.getViewPort().width >= resBreakpointMd && target.hasClass("full-height-content-scrollable")) {
                    height = height - 35;
                    target.find('.full-height-content-body').css('height', height);
                    App.initSlimScroll(target.find('.full-height-content-body'));
                } else {
                    target.css('min-height', height);
                }
            }
        });
    };

    // Main init methods to initialize the layout
    return {

        initSidebar: function() {
            // Layout handlers
            handleFixedSidebar(); // It handles fixed sidebar menu
            handleSidebarMenu(); // It handles main menu
            handleSidebarToggler(); // It handles sidebar hide/show

            App.addResizeHandler(handleFixedSidebar); // Reinitialize fixed sidebar on window resize
        },

        initContent: function() {
            handle100HeightContent(); // It handles 100% height elements (block, portlet, etc.)
            handleTabs(); // It handles bootstrap tabs

            App.addResizeHandler(handleSidebarAndContentHeight); // Recalculate sidebar & content height on window resize
            App.addResizeHandler(handle100HeightContent); // Reinitialize content height on window resize
        },

        init: function () {            
            this.initSidebar();
            this.initContent();
        },

        // Public function to fix the sidebar and content height accordingly
        fixContentHeight: function () {
            handleSidebarAndContentHeight();
        },

        initFixedSidebarHoverEffect: function() {
            handleFixedSidebarHoverEffect();
        },

        initFixedSidebar: function() {
            handleFixedSidebar();
        }
    };

}(); // /.Layout function()

jQuery(document).ready(function() {
    Layout.init(); // Init core components
});
