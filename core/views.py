from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Sum

from note_page.models import Note
from .models import StudySession


def welcome(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            existing_sessions = StudySession.objects.filter(
                user=user,
                is_active=True
            )

            for session in existing_sessions:
                session.end_time = timezone.now()
                session.duration_seconds = int(
                    (session.end_time - session.start_time).total_seconds()
                )
                session.is_active = False
                session.save()

            StudySession.objects.create(
                user=user,
                is_active=True
            )

            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, "welcome.html")


@login_required
def home(request):
    notes = Note.objects.filter(user=request.user).order_by('-updated_at')
    events = []

    today = timezone.localdate()

    saved_today_seconds = StudySession.objects.filter(
        user=request.user,
        start_time__date=today,
        is_active=False
    ).aggregate(total=Sum('duration_seconds'))['total'] or 0

    total_study_seconds = StudySession.objects.filter(
        user=request.user,
        is_active=False
    ).aggregate(total=Sum('duration_seconds'))['total'] or 0

    active_session = StudySession.objects.filter(
        user=request.user,
        is_active=True
    ).order_by('-start_time').first()

    current_session_seconds = 0
    if active_session:
        current_session_seconds = int(
            (timezone.now() - active_session.start_time).total_seconds()
        )

    today_study_seconds = saved_today_seconds + current_session_seconds

    return render(request, "home.html", {
        "notes": notes,
        "events": events,
        "total_study_seconds": total_study_seconds,
        "today_study_seconds": today_study_seconds,
        "saved_today_seconds": saved_today_seconds,
        "current_session_seconds": current_session_seconds,
    })


@login_required
def custom_logout(request):
    if request.method == "POST":
        active_session = StudySession.objects.filter(
            user=request.user,
            is_active=True
        ).order_by('-start_time').first()

        session_message = None

        if active_session:
            active_session.end_time = timezone.now()
            active_session.duration_seconds = int(
                (active_session.end_time - active_session.start_time).total_seconds()
            )
            active_session.is_active = False
            active_session.save()

            total_seconds = active_session.duration_seconds
            session_hours = total_seconds // 3600
            session_minutes = (total_seconds % 3600) // 60
            session_seconds = total_seconds % 60

            today = timezone.localdate()
            today_total_seconds = StudySession.objects.filter(
                user=request.user,
                start_time__date=today,
                is_active=False
            ).aggregate(total=Sum('duration_seconds'))['total'] or 0

            today_hours = today_total_seconds // 3600
            today_minutes = (today_total_seconds % 3600) // 60
            today_seconds = today_total_seconds % 60

            session_message = (
                f"You studied for {session_hours}h {session_minutes}m {session_seconds}s this session. "
                f"Your total study time today is {today_hours}h {today_minutes}m {today_seconds}s."
            )

        logout(request)

        if session_message:
            messages.success(request, session_message)

        return redirect('welcome')

    return redirect('home')


@csrf_exempt
@login_required
@require_POST
def close_study_session(request):
    active_session = StudySession.objects.filter(
        user=request.user,
        is_active=True
    ).order_by('-start_time').first()

    if active_session:
        active_session.end_time = timezone.now()
        active_session.duration_seconds = int(
            (active_session.end_time - active_session.start_time).total_seconds()
        )
        active_session.is_active = False
        active_session.save()

    return JsonResponse({'success': True})

@login_required
def account(request):
    today = timezone.localdate()

    saved_today_seconds = StudySession.objects.filter(
        user=request.user,
        start_time__date=today,
        is_active=False
    ).aggregate(total=Sum('duration_seconds'))['total'] or 0

    total_study_seconds = StudySession.objects.filter(
        user=request.user,
        is_active=False
    ).aggregate(total=Sum('duration_seconds'))['total'] or 0

    active_session = StudySession.objects.filter(
        user=request.user,
        is_active=True
    ).order_by('-start_time').first()

    current_session_seconds = 0
    if active_session:
        current_session_seconds = int(
            (timezone.now() - active_session.start_time).total_seconds()
        )

    today_study_seconds = saved_today_seconds + current_session_seconds

    return render(request, "account.html", {
        "total_study_seconds": total_study_seconds,
        "today_study_seconds": today_study_seconds,
        "saved_today_seconds": saved_today_seconds,
        "current_session_seconds": current_session_seconds,
    })