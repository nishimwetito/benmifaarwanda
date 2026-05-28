"""Redirect helpers after resource CRUD from dashboard or public lists."""

from django.urls import reverse

_SECTION_BY_LIST = {
    'video_list': 'videos',
    'pdf_list': 'pdfs',
    'slides_list': 'slides',
}


def redirect_after_resource_action(request, list_url_name):
    if request.GET.get('return') == 'dashboard' or request.POST.get('return') == 'dashboard':
        section = _SECTION_BY_LIST.get(list_url_name, 'videos')
        return f"{reverse('dashboard')}?tab=resources&section={section}"
    return reverse(list_url_name)
