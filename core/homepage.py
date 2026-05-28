"""Helpers for landing-page featured content selection."""


def save_homepage_selection(request):
    """Update show_on_homepage + homepage_order from dashboard POST."""
    from .models import Video, ProfessionalSupportService

    for video in Video.objects.all():
        video.show_on_homepage = request.POST.get(f'video_home_{video.pk}') == 'on'
        try:
            video.homepage_order = int(request.POST.get(f'video_order_{video.pk}', 0) or 0)
        except ValueError:
            video.homepage_order = 0
        video.save(update_fields=['show_on_homepage', 'homepage_order'])

    for service in ProfessionalSupportService.objects.all():
        service.show_on_homepage = request.POST.get(f'service_home_{service.pk}') == 'on'
        try:
            service.homepage_order = int(request.POST.get(f'service_order_{service.pk}', 0) or 0)
        except ValueError:
            service.homepage_order = 0
        service.save(update_fields=['show_on_homepage', 'homepage_order'])
