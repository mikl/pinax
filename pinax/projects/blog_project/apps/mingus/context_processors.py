from django.conf import settings

def site_info(request):
    """
    Adds site-specific meta information to the context.

    To employ, add the site_info method reference to your project
    settings TEMPLATE_CONTEXT_PROCESSORS.

    Example:
        TEMPLATE_CONTEXT_PROCESSORS = (
            ...
            "mingus.core.context_processors.site_info",
        )
    """
    return {
        'STATIC_URL': getattr(settings,'STATIC_URL', ''),
    }

