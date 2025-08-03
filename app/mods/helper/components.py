from typed import typed, Str, Any
from app.models import Alpine

_X_DATA_RESPONSIVE = """{{
    isPhoneQuery: window.matchMedia('(max-width: 639px)'),
    isTabletQuery: window.matchMedia('(min-width: 640px) and (max-width: 1023px)'),
    isDesktopQuery: window.matchMedia('(min-width: 1024px)'),
    isPhone: false,
    isTablet: false,
    isDesktop: false,
    isMobile: false,
    isNotPhone: false,
    isNotTablet: false,
    isNotDesktop: false,
    isnotMobole: false,
    init() {{
        const updateScreenSizes = () => {{
            this.isPhone = this.isPhoneQuery.matches;
            this.isTablet = this.isTabletQuery.matches;
            this.isDesktop = this.isDesktopQuery.matches;
            this.isMobile = this.isPhone || this.isTablet;
            this.isNotPhone = this.isTablet || this.isDesktop;
            this.isNotTablet = this.isPhone || this.isDesktop;
            this.isNotDesktop = this.isPhone || this.isTablet;
            this.isNotMobile = this.isDesktop;
        };
        this.isPhoneQuery.addEventListener('change', updateScreenSizes);
        this.isTabletQuery.addEventListener('change', updateScreenSizes);
        this.isDesktopQuery.addEventListener('change', updateScreenSizes);
        updateScreenSizes();
    }}
}}"""

_RESPONSIVE  = Alpine(x_data=_X_DATA_RESPONSIVE)
_DESKTOP     = Alpine(x_if="isDesktop")
_PHONE       = Alpine(x_if="isPhone")
_TABLET      = Alpine(x_if="isTablet")
_MOBILE      = Alpine(x_if="isMobile")
_NOT_DESKTOP = Alpine(x_if="isNotDesktop")
_NOT_PHONE   = Alpine(x_if="isNotPhone")
_NOT_TABLET  = Alpine(x_if="isNotTablet")
_NOT_MOBILE  = Alpine(x_if="isNotMobile")
