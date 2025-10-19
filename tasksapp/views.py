from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from celery.result import AsyncResult
from django.conf import settings
from pathlib import Path

from .tasks import add, count_words


def home(request: HttpRequest) -> HttpResponse:
    return render(request, 'home.html')


def start_add(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        try:
            x = int(request.POST.get('x', '0'))
            y = int(request.POST.get('y', '0'))
        except ValueError:
            x, y = 0, 0
        task = add.delay(x, y)
        return redirect(reverse('task_status', kwargs={'task_id': task.id}))
    return render(request, 'add.html')


def start_count(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        text = request.POST.get('text', '')
        task = count_words.delay(text)
        return redirect(reverse('task_status', kwargs={'task_id': task.id}))
    return render(request, 'count.html')


def task_status(request: HttpRequest, task_id: str) -> HttpResponse:
    result = AsyncResult(task_id)
    context = {
        'task_id': task_id,
        'state': result.state,
        'ready': result.ready(),
        'successful': result.successful() if result.ready() else False,
        'result': result.result if result.ready() else None,
    }
    return render(request, 'task_status.html', context)


def decks(request: HttpRequest) -> HttpResponse:
    content_root: Path = Path(getattr(settings, 'SLIDES_CONTENT_DIR', Path('content')))
    decks_list: list[dict] = []
    if content_root.exists():
        for course_dir in sorted(content_root.iterdir()):
            if not course_dir.is_dir():
                continue
            for date_dir in sorted(course_dir.iterdir()):
                if not date_dir.is_dir():
                    continue
                for deck_dir in sorted(date_dir.iterdir()):
                    if not deck_dir.is_dir():
                        continue
                    slides = sorted(p for p in deck_dir.iterdir() if p.suffix == '.md')
                    decks_list.append({
                        'course': course_dir.name,
                        'date': date_dir.name,
                        'deck': deck_dir.name,
                        'slide_count': len(slides),
                        'path': str(deck_dir),
                    })
    context = {'decks': decks_list}
    return render(request, 'decks.html', context)

