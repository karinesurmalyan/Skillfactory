from random import randint
from django.core.mail import send_mail
from django.shortcuts import render
from .models import *
from django.contrib.auth.models import User, Group
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView,
)
from .filters import *
from .forms import *
from datetime import datetime
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import HttpResponseRedirect, HttpRequest, HttpResponseBadRequest, request
from django.urls import reverse_lazy, resolve, reverse
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.conf import settings


class AnnouncementsList(ListView):
    model = Announcement
    ordering = '-date'
    template_name = 'announcements.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['-date'] = datetime.utcnow()
        return context


class AnnouncementDetail(DetailView):
    model = Announcement
    template_name = 'announcement.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_ad = context.get('post_detail')
        return context


class AnnouncementCreate(LoginRequiredMixin, CreateView):
    form_class = PostForm
    model = Announcement
    template_name = 'post_edit.html'
    context_object_name = 'post_create'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.author = self.request.user
        post.save()
        return super().form_valid(form)


class AnnouncementUpdate(LoginRequiredMixin, UpdateView):
    form_class = PostForm
    model = Announcement
    template_name = 'post_edit.html'
    context_object_name = 'post_edit'

    def form_valid(self, form):
        post = form.save(commit=False)
        if post.author == self.request.user:
            return super().form_valid(form)
        else:
            return HttpResponseBadRequest(
                f'Чтобы редактировать пост, необходимо быть его автором')


class AnnouncementDelete(LoginRequiredMixin, DeleteView):
    model = Announcement
    template_name = 'post_delete.html'
    context_object_name = 'post_delete'
    success_url = reverse_lazy('posts')
    permission_required = 'board.delete_post'

    def form_valid(self, form):
        post = form.save(commit=False)
        if post.author == self.request.user:
            return super().form_valid(form)
        else:
            return HttpResponseBadRequest(
                f'Чтобы удалить пост, необходимо быть его автором')


class CommentList(ListView, LoginRequiredMixin):
    model = Comment
    template_name = 'comments.html'
    context_object_name = 'comments'
    ordering = '-date'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context

    def get_queryset(self, **kwargs):
        queryset = super().get_queryset()
        self.filterset = CommentFilter(self.request.GET, queryset)
        return self.filterset.qs


class CommentDetail(LoginRequiredMixin, DeleteView):
    model = Comment
    ordering = '-date'
    context_object_name = 'comment'
    template_name = 'comment.html'
    success_url = reverse_lazy('posts')


class CommentCreate(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'comment_edit.html'
    context_object_name = 'comment_edit'
    success_url = reverse_lazy('posts')

    def get_queryset(self, **kwargs):
        queryset = super().get_queryset(**kwargs)
        return queryset

    def form_valid(self, form):
        comment = form.save(commit=False)
        comment.comment_post = Announcement.objects.get(id=self.kwargs.get("pk"))
        comment.comment_author = self.request.user
        comment.save()
        send_mail(
            subject=f'{comment.comment_post.author}, на Ваше объявление {comment.comment_post.title} оставил отклик {comment.comment_author}.',
            message=f'{comment.text},'
                    f'Чтобы принять или отклонить перейдите на страницу с откликами на Ваши объявления - {self.request.build_absolute_uri(reverse("comments"))}',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[comment.comment_post.author.email])
        return redirect(f'/posts/{self.kwargs.get("pk")}')

    def get_success_url(self):
        return reverse('comment_detail', kwargs={'pk': self.object.pk})


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'allauth/layouts/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_premium'] = not self.request.user.groups.filter(name='premium').exists()
        return context


class ConfirmUser(UpdateView):
    model = User
    context_object_name = 'confirm_user'

    def post(self, request, *args, **kwargs):
        if 'code' in request.POST:
            user = User.objects.filter(code=request.POST['code'])
            if user.exists():
                user.update(is_active=True)
                user.update(code=None)
            else:
                return render(self.request, 'users/invalid_code.html')
        return redirect('account_login')


@login_required
def comment_accept(request, **kwargs):
    if request.user.is_authenticated:
        comment = Comment.objects.get(id=kwargs.get("pk"))
        comment.is_accepted = True
        comment.save()
        send_mail(subject=f'Отклин на объявление {comment.comment_post.title}',
                  message=f'{comment.comment_author},'
                          f'Ваш отклик на объявление {comment.comment_post.title} принят!',
                  from_email=settings.DEFAULT_FROM_EMAIL,
                  recipient_list=[comment.comment_author.email])
        return HttpResponseRedirect('/posts/comments')
    else:
        return HttpResponseRedirect('/accounts/login')


@login_required
def comment_decline(request, **kwargs):
    if request.user.is_authenticated:
        comment = Comment.objects.get(id=kwargs.get("pk"))
        comment.delete()
        return HttpResponseRedirect('/posts/comments')
    else:
        return HttpResponseRedirect('/accounts/login')


@login_required
def upgrade_me(request):
    user = request.user
    authors_group = Group.objects.get(name='premium')
    if not request.user.groups.filter(name='premium').exists():
        authors_group.user_set.add(user)
    return redirect('/')

