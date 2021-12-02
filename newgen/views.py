from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import ListView, DetailView
from .models import Post, Category, Tag, MainPage, Questions
from django.db.models import F
from .forms import NewsForm, UserRegisterForm, UserLoginForm
from django.contrib import messages
from django.contrib.auth import login, logout


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Вы успешно зарегистрировались')
            return redirect('home')
        else:
            messages.error(request, 'Ошибка регистрации')
    else:
        form = UserRegisterForm()
    return render(request, 'newgen/register.html', {"form": form})


def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = UserLoginForm()
    return render(request, 'newgen/login.html', {"form": form})


def user_logout(request):
    logout(request)
    return redirect('login')

def admin(request):
    return redirect('admin')


class Home(ListView):
    model = MainPage
    template_name = 'newgen/index.html'
    context_object_name = 'pages'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Пространство образования и эксперимента'
        return context


class PostsByCategory(ListView):
    template_name = 'newgen/category.html'
    context_object_name = 'posts'
    paginate_by = 2
    allow_empty = False

    def get_queryset(self):
        return Post.objects.filter(category__slug=self.kwargs['slug'])

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = Category.objects.get(slug=self.kwargs['slug'])
        context['content'] = Category.objects.get(slug=self.kwargs['slug'])
        return context


class PostsByTag(ListView):
    template_name = 'newgen/tags.html'
    context_object_name = 'posts'
    paginate_by = 2
    allow_empty = False

    def get_queryset(self):
        return Post.objects.filter(tags__slug=self.kwargs['slug'])

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Статьи по тегу: ' + str(Tag.objects.get(slug=self.kwargs['slug']))
        return context



class List(ListView):
    model = Category
    template_name = 'newgen/category.html'
    context_object_name = 'category'

    def get_queryset(self):
        return Category.objects.filter(category__slug=self.kwargs['slug'])

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = Category.objects.get(slug=self.kwargs['slug'])
        return context


def get_post(request, slug):
    return render(request, 'newgen/category.html')


class GetPost(DetailView):
    model = Post
    template_name = 'newgen/single.html'
    context_object_name = 'post'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        self.object.views = F('views') + 1
        self.object.save()
        self.object.refresh_from_db()
        return context


def add_news(request):
    if request.method == 'POST':
        form = NewsForm(request.POST)
        if form.is_valid():
            # print(form.cleaned_data)
            Questions.objects.create(**form.cleaned_data)
            return redirect('answer')
            # posts = form.save()
            # return redirect(posts)
    else:
        form = NewsForm()
    return render(request, 'newgen/add_news.html', {'form': form})


def get_answer(request):
    return render(request, 'newgen/answer.html')
