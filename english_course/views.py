from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse

from .forms import UserWordForm, EditUserWordForm, UserForm, CreateUserForm
from .models import UserWord, Word
from .utils import get_allowed_user_or_redirect


@login_required
def user_profile(request, user_id):
    target_user = get_allowed_user_or_redirect(request.user, user_id)
    if not target_user:
        return redirect('english_course:user', user_id=request.user.id)

    all_words = UserWord.objects.filter(user=target_user)
    words = all_words.order_by('-id')[:10]
    available_words = Word.objects.all()

    students = target_user.students.all()
    return render(request, 'english_course/user.html', {
        'user': target_user,
        'total_words': all_words.count(),
        'words': words,
        'form': UserWordForm(),
        'available_words': available_words,
        'user_form': UserForm(instance=target_user),
        'create_user_form': CreateUserForm(instance=target_user),
        'students': students,
        })


def add_word(request, user_id):
    target_user = get_allowed_user_or_redirect(request.user, user_id)

    if not target_user:
        return redirect('english_course:user', user_id=request.user.id)

    if request.method == 'POST':
        form = UserWordForm(request.POST)

        if form.is_valid():
            word_text = form.cleaned_data['word_text']
            word_translation = form.cleaned_data['translation']

            word_obj, created = Word.objects.get_or_create(word=word_text)
            user_word = UserWord.objects.filter(user=target_user, word=word_obj).first()

            if user_word:
                translate_exist = set(user_word.translation.split(', '))
                if word_translation not in translate_exist:
                    translate_exist.add(word_translation)
                    user_word.translation = ', '.join(sorted(translate_exist))
                    user_word.save()
            else:
                user_word = form.save(commit=False)
                user_word.user = target_user
                user_word.word = word_obj
                user_word.translation = word_translation
                user_word.save()

        return redirect('english_course:user', user_id=target_user.id)


def edit_word(request, word_id):
    user_word = get_object_or_404(UserWord, id=word_id)

    target_user = get_allowed_user_or_redirect(request.user, user_word.user.id)

    if not target_user:
        return redirect('english_course:user', user_id=request.user.id)

    if request.method == 'POST':
        form = EditUserWordForm(request.POST, instance=user_word)
        if form.is_valid():
            form.save()
        return redirect(reverse('english_course:user', kwargs={'user_id': target_user.id}))
    return redirect(reverse('english_course:user', kwargs={'user_id': target_user.id}))


def delete_userword(request, word_id):
    user_word = get_object_or_404(UserWord, id=word_id)
    target_user = get_allowed_user_or_redirect(request.user, user_word.user.id)
    if not target_user:
        return redirect('english_course:user', user_id=request.user.id)

    if request.method == 'POST':
        user_word.delete()
    return redirect('english_course:user', user_id=target_user.id)


@login_required()
def edit_profile(request, user_id):
    target_user = get_allowed_user_or_redirect(request.user, user_id)

    if not target_user:
        return redirect('english_course:user', user_id=request.user.id)

    if request.method == 'POST':
        form = UserForm(request.POST, instance=target_user)
        if form.is_valid():
            form.save()
            return redirect(reverse('english_course:user', kwargs={'user_id': target_user.id}))
    else:
        form = UserForm(instance=target_user)
    return render(request, 'english_course/user.html', {'user_form': form})


@login_required
def index(request):
    return redirect('english_course:user', user_id=request.user.id)


def create_user(request):
    if request.user.role not in ['admin', 'teacher']:
        return redirect('english_course:user', user_id=request.user.id)

    if request.method == 'POST':
        form = CreateUserForm(request.POST or None, current_user=request.user)
        if form.is_valid():
            new_user = form.save(commit=False)

            chosen_role = form.cleaned_data.get('role')
            if request.user.role == 'teacher':
                new_user.role = 'student'
                new_user.teacher = request.user
            else:
                new_user.role = chosen_role
            new_user.set_password(form.cleaned_data['password1'])
            new_user.save()
            return redirect('english_course:user', user_id=request.user.id)

    else:
        form = CreateUserForm(current_user=request.user)

    return render(request, 'english_course/modals/create_user.html', {'form': form})


def full_vocabulary(request, user_id):
    target_user = get_allowed_user_or_redirect(request.user, user_id)
    if not target_user:
        return redirect('english_course:user', user_id=request.user.id)

    all_words = UserWord.objects.filter(user=target_user).order_by('-id')
    paginator = Paginator(all_words, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'english_course/modals/vocabulary.html', {
        'page_obj': page_obj,
        'user': target_user,
    })
