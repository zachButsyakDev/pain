from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import NoteSection, Note
from .forms import NoteForm, NoteSectionForm


@login_required
def notes_list(request):
    """Main notes page: lists all notes belonging to the logged-in user."""
    search_query = request.GET.get('search', '')
    notes = Note.objects.filter(user=request.user).order_by('-updated_at')
    if search_query:
        notes = notes.filter(title__icontains=search_query) | Note.objects.filter(
            user=request.user, content__icontains=search_query
        )
    sections = NoteSection.objects.filter(user=request.user)
    context = {
        'notes': notes,
        'sections': sections,
        'search_query': search_query,
    }
    return render(request, 'notes.html', context)


@login_required
def create_note(request):
    """Create a new note for the logged-in user."""
    if request.method == 'POST':
        form = NoteForm(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.user = request.user
            note.save()
            return redirect('note_view', id=note.note_id)
    else:
        form = NoteForm()
        # Limit section choices to this user's sections
        form.fields['section'].queryset = NoteSection.objects.filter(user=request.user)

    context = {'form': form}
    return render(request, 'note_view.html', context)


@login_required
def note_view(request, id):
    """View a single note (read-only)."""
    note = get_object_or_404(Note, note_id=id, user=request.user)
    context = {'note': note}
    return render(request, 'note_detail.html', context)


@login_required
def edit_note(request, id):
    """Edit an existing note."""
    note = get_object_or_404(Note, note_id=id, user=request.user)
    if request.method == 'POST':
        form = NoteForm(request.POST, instance=note)
        if form.is_valid():
            form.save()
            return redirect('note_view', id=note.note_id)
    else:
        form = NoteForm(instance=note)
        form.fields['section'].queryset = NoteSection.objects.filter(user=request.user)

    context = {'form': form, 'note': note}
    return render(request, 'edit_note.html', context)


@login_required
def delete_note(request, id):
    """Delete a note belonging to the logged-in user."""
    note = get_object_or_404(Note, note_id=id, user=request.user)
    if request.method == 'POST':
        note.delete()
        return redirect('notes')
    context = {'note': note}
    return render(request, 'confirm_delete_note.html', context)


# ── NoteSection views ──────────────────────────────────────────────────────────

@login_required
def create_note_section(request):
    """Create a new section/folder for notes."""
    if request.method == 'POST':
        form = NoteSectionForm(request.POST)
        if form.is_valid():
            section = form.save(commit=False)
            section.user = request.user
            section.save()
            return redirect('notes')
    else:
        form = NoteSectionForm()
    context = {'form': form}
    return render(request, 'note_section_form.html', context)


@login_required
def update_note_section(request, id):
    """Rename a section."""
    section = get_object_or_404(NoteSection, section_id=id, user=request.user)
    if request.method == 'POST':
        form = NoteSectionForm(request.POST, instance=section)
        if form.is_valid():
            form.save()
            return redirect('notes')
    else:
        form = NoteSectionForm(instance=section)
    context = {'form': form, 'section': section}
    return render(request, 'note_section_form.html', context)


@login_required
def delete_note_section(request, id):
    """Delete a section (notes in it become unsectioned)."""
    section = get_object_or_404(NoteSection, section_id=id, user=request.user)
    if request.method == 'POST':
        section.delete()
        return redirect('notes')
    context = {'section': section}
    return render(request, 'confirm_delete_section.html', context)
