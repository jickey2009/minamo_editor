from django.shortcuts import render, redirect
from .forms import BookForm, ChapterForm, SectionForm, ConfigurationForm, SignupForm, LoginForm
from .models import Book, Chapter, Section, Configuration
from django.views.generic import ListView, CreateView
from django.contrib.auth.views import LoginView as BaseLoginView, LogoutView as BaseLogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.contrib.auth import login, authenticate
import urllib.parse

# Create your views here.
class SignupView(CreateView):
    form_class = SignupForm
    template_name = 'minamo/signup.html'
    success_url = reverse_lazy('minamo:index')

    def form_valid(self, form):
        response = super().form_valid(form)
        user_id = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        authenticated_user = authenticate(username=user_id, password=password)
        if authenticated_user is not None:
            login(self.request, authenticated_user)
        return response
    
class LoginView(BaseLoginView):
    form_class = LoginForm
    template_name = 'minamo/login.html'

class LogoutView(BaseLogoutView):
    success_url = reverse_lazy('minamo:index')

class BookListView(LoginRequiredMixin, ListView):
    model = Book
    template_name = 'minamo/index.html'
    context_object_name = 'books'
    ordering = ['-created_date']
    paginate_by = 10
    def get_queryset(self, **kwargs):
        queryset = super().get_queryset(**kwargs)
        return queryset.filter(author=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['books_json'] = [{'id': book.id} for book in context['books']]
        return context

@login_required
def new_book(request):
    new_book = Book(author=request.user)
    new_book.title = "無題の本"
    new_book.description = ""
    new_book.save()
    return redirect('minamo:index')
    
@login_required
def book_detail(request, book_id):
    book = request.user.book_set.get(id=book_id)
    chapters = book.chapter_set.order_by('order')
    context = {'book': book, 'chapters': chapters}
    context['chapters_json'] = [{'id': chapter.id} for chapter in chapters]
    return render(request, 'minamo/book_detail.html', context)

@login_required
def edit_book(request, book_id):
    book = request.user.book_set.get(id=book_id)
    form = BookForm(request.POST or None, instance=book)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('minamo:index')
    context = {'form': form, 'book': book}
    return render(request, 'minamo/edit_book.html', context)

@login_required
def delete_book(request, book_id):
    book = request.user.book_set.get(id=book_id)
    book.delete()
    return redirect('minamo:index')

@login_required
def rename_book(request, book_id):
    book = request.user.book_set.get(id=book_id)
    if request.method == 'POST':
        new_title = request.POST.get('title', '').strip()
        if new_title:
            book.title = new_title
            book.save()
        return redirect('minamo:index')

@login_required
def new_chapter(request, book_id):
    form = ChapterForm(request.POST or None)
    book = request.user.book_set.get(id=book_id)
    new_chapter = Chapter(book=book, order=book.next_chapter_order)
    new_chapter.title = "Chapter " + str(book.next_chapter_order)
    book.next_chapter_order += 1
    book.save()
    new_chapter.save()
    return redirect('minamo:book_detail', book_id=book.id)

@login_required
def chapter_detail(request, book_id, chapter_id):
    book = request.user.book_set.get(id=book_id)
    chapter = book.chapter_set.get(id=chapter_id)
    sections = chapter.section_set.order_by('order')
    context = {'book': book, 'chapter': chapter, 'sections': sections}
    context['sections_json'] = [{'id': section.id} for section in sections]
    return render(request, 'minamo/chapter_detail.html', context)

@login_required
def rename_chapter(request, book_id, chapter_id):
    book = request.user.book_set.get(id=book_id)
    chapter = book.chapter_set.get(id=chapter_id)
    if request.method == 'POST':
        new_title = request.POST.get('title', '').strip()
        if new_title:
            chapter.title = new_title
            chapter.save()
        return redirect('minamo:book_detail', book_id=book.id)
    
@login_required
def swap_chapter(request, book_id, chapter_id, direction):
    book = request.user.book_set.get(id=book_id)
    chapter = book.chapter_set.get(id=chapter_id)
    direction -= 2  # Convert 1 (up) / 3 (down) to -1 / +1
    target_chapter = chapter
    target_order = chapter.order + direction
    while (target_order >= 1 and target_order < book.next_chapter_order):
        try:
            target_chapter = book.chapter_set.get(order=target_order)
            break
        except Chapter.DoesNotExist:
            pass
        target_order += direction
    chapter.order, target_chapter.order = target_chapter.order, chapter.order
    chapter.save()
    target_chapter.save()

    return redirect('minamo:book_detail', book_id=book.id)

@login_required
def delete_chapter(request, book_id, chapter_id):
    book = request.user.book_set.get(id=book_id)
    chapter = book.chapter_set.get(id=chapter_id)
    chapter.delete()
    return redirect('minamo:book_detail', book_id=book.id)

@login_required
def new_section(request, book_id, chapter_id):
    book = request.user.book_set.get(id=book_id)
    chapter = book.chapter_set.get(id=chapter_id)
    new_section = Section(chapter=chapter, order=chapter.next_section_order)
    new_section.title = "Section " + str(chapter.next_section_order)
    new_section.content_head = ""
    new_section.length = 0
    new_section.save()
    chapter.next_section_order += 1
    chapter.save()
    return redirect('minamo:chapter_detail', book_id=book.id, chapter_id=chapter.id)


@login_required
def section_detail(request, book_id, chapter_id, section_id):
    book = request.user.book_set.get(id=book_id)
    chapter = book.chapter_set.get(id=chapter_id)
    section = chapter.section_set.get(id=section_id)
    context = {'book': book, 'chapter': chapter, 'section': section}
    return render(request, 'minamo/section_detail.html', context)

@login_required
def edit_section(request, book_id, chapter_id, section_id, return_url =None):
    book = request.user.book_set.get(id=book_id)
    chapter = book.chapter_set.get(id=chapter_id)
    section = chapter.section_set.get(id=section_id)
    length = section.length
    if request.method == 'POST' :
        section.content = request.POST.get('content', '')
        section.length = len(section.content)
        if section.content:
            section.content_head = section.content.splitlines()[0][:15]
        section.save()
        length_diff = section.length - length
        chapter.length += length_diff
        chapter.save()
        book.length += length_diff
        book.save()
        if return_url == 'chapter':
            return redirect('minamo:chapter_detail', book_id=book.id, chapter_id=chapter.id)
        else:
            return redirect('minamo:edit_section', book_id=book.id, chapter_id=chapter.id, section_id=section.id)
    context = {'book': book, 'chapter': chapter, 'section': section}
    context['configuration_json'] = None
    try:
        context['configuration_json'] = {
            'dark_mode': request.user.configuration.dark_mode,
            'text_size': request.user.configuration.text_size,
            'textarea_height': request.user.configuration.textarea_height,
            'textarea_width': request.user.configuration.textarea_width,
        }
    except Configuration.DoesNotExist:
        pass

    return render(request, 'minamo/edit_section.html', context)

@login_required
def rename_section(request, book_id, chapter_id, section_id,):
    book = request.user.book_set.get(id=book_id)
    chapter = book.chapter_set.get(id=chapter_id)
    section = chapter.section_set.get(id=section_id)
    if request.method == 'POST':
        new_title = request.POST.get('title', '').strip()
        if new_title:
            section.title = new_title
            section.save()
    return redirect('minamo:chapter_detail', book_id=book.id, chapter_id=chapter.id)
    
@login_required
def swap_section(request, book_id, chapter_id, section_id, direction):
    book = request.user.book_set.get(id=book_id)
    chapter = book.chapter_set.get(id=chapter_id)
    section = chapter.section_set.get(id=section_id)
    direction -= 2  # Convert 1 (up) / 3 (down) to -1 / +1
    target_section = section
    target_order = section.order + direction
    while (target_order >= 1 and target_order < chapter.next_section_order):
        try:
            target_section = chapter.section_set.get(order=target_order)
            break
        except Section.DoesNotExist:
            pass
        target_order += direction
    section.order, target_section.order = target_section.order, section.order
    section.save()
    target_section.save()
    return redirect('minamo:chapter_detail', book_id=book.id, chapter_id=chapter.id)

@login_required
def delete_section(request, book_id, chapter_id, section_id):
    book = request.user.book_set.get(id=book_id)
    chapter = book.chapter_set.get(id=chapter_id)
    section = chapter.section_set.get(id=section_id)
    section.delete()
    return redirect('minamo:chapter_detail', book_id=book.id, chapter_id=chapter.id)

@login_required
def export_book(request, book_id):
    content = ''
    book = request.user.book_set.get(id=book_id)
    chapters = book.chapter_set.order_by('order')
    for chapter in chapters:
        content += f"# {chapter.title}\n\n"
        sections = chapter.section_set.order_by('order')
        for section in sections:
            content += f"## {section.title}\n\n"
            content += f"{section.content}\n\n"
    filename = urllib.parse.quote(f"{book.title}.txt")
    response = HttpResponse(content, content_type='text/plain; charset=utf-8')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    return response

@login_required
def settings(request):
    user = request.user
    try:
        configuration = user.configuration
    except Configuration.DoesNotExist:
        configuration = Configuration(user=user)
        configuration.save()
    form = ConfigurationForm(request.POST or None, instance=configuration)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('minamo:index')
    context = {'form': form}
    return render(request, 'minamo/settings.html', context)