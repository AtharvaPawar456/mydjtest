from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def nav_active(context, *url_names):
    """Returns a highlight class when the current view's url_name is one of url_names."""
    request = context.get('request')
    resolver_match = getattr(request, 'resolver_match', None)
    if not resolver_match or resolver_match.url_name not in url_names:
        return ''
    return 'text-brand-700 bg-slate-100 dark:bg-slate-800 dark:text-brand-400'
