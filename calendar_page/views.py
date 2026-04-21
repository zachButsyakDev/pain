from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.utils.dateparse import parse_datetime
from django.utils import timezone
from .models import CalendarEvent


@login_required
def calendar(request):
    return render(request, 'calendar_view.html', {})


@login_required
def events_json(request):
    events = CalendarEvent.objects.filter(user=request.user)
    data = []
    for e in events:
        data.append({
            'id':          e.event_id,
            'title':       e.title,
            'description': e.description,
            'start':       e.start.strftime('%Y-%m-%dT%H:%M'),
            'duration':    e.duration,
            'tags':        e.tag_list(),
        })
    return JsonResponse(data, safe=False)


@login_required
@require_POST
def event_create(request):
    title       = request.POST.get('title', '').strip()
    description = request.POST.get('description', '').strip()
    start_raw   = request.POST.get('start', '')
    duration    = request.POST.get('duration', 60)
    tags        = request.POST.get('tags', '').strip()

    if not title or not start_raw:
        return JsonResponse({'error': 'Title and start time are required.'}, status=400)

    start = parse_datetime(start_raw)
    if not start:
        return JsonResponse({'error': 'Invalid date/time format.'}, status=400)
    if timezone.is_naive(start):
        start = timezone.make_aware(start)

    if CalendarEvent.objects.filter(user=request.user, title=title, start=start).exists():
        return JsonResponse({'error': 'An identical event already exists.'}, status=400)

    event = CalendarEvent.objects.create(
        user=request.user,
        title=title,
        description=description,
        start=start,
        duration=int(duration),
        tags=tags,
    )
    return JsonResponse({'success': True, 'id': event.event_id})


@login_required
def event_detail(request, pk):
    event = get_object_or_404(CalendarEvent, event_id=pk, user=request.user)
    return JsonResponse({
        'id':          event.event_id,
        'title':       event.title,
        'description': event.description,
        'start':       event.start.strftime('%Y-%m-%dT%H:%M'),
        'duration':    event.duration,
        'tags':        event.tags,
    })


@login_required
@require_POST
def event_edit(request, pk):
    event = get_object_or_404(CalendarEvent, event_id=pk, user=request.user)

    title       = request.POST.get('title', '').strip()
    description = request.POST.get('description', '').strip()
    start_raw   = request.POST.get('start', '')
    duration    = request.POST.get('duration', 60)
    tags        = request.POST.get('tags', '').strip()

    if not title or not start_raw:
        return JsonResponse({'error': 'Title and start time are required.'}, status=400)

    start = parse_datetime(start_raw)
    if not start:
        return JsonResponse({'error': 'Invalid date/time format.'}, status=400)
    if timezone.is_naive(start):
        start = timezone.make_aware(start)

    event.title       = title
    event.description = description
    event.start       = start
    event.duration    = int(duration)
    event.tags        = tags
    event.save()
    return JsonResponse({'success': True})


@login_required
@require_POST
def event_delete(request, pk):
    event = get_object_or_404(CalendarEvent, event_id=pk, user=request.user)
    event.delete()
    return JsonResponse({'success': True})