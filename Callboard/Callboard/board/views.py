from random import randint
from django.core.mail import send_mail
from django.shortcuts import render
from .models import *
from django.contrib.auth.models import User
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
    context_object_name = 'post_detail'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_ad = context.get('post_detail')
        return context


class AnnouncementCreate(PermissionRequiredMixin, CreateView):
    form_class = PostForm
    model = Announcement
    template_name = 'post_edit.html'
    context_object_name = 'post_create'
    permission_required = ('board.add_post',)

    def form_valid(self, form):
        post = form.save(commit=False)
        post.author = self.request.user
        return super().form_valid(form)


class AnnouncementUpdate(PermissionRequiredMixin, UpdateView):
    form_class = PostForm
    model = Announcement
    template_name = 'post_edit.html'
    context_object_name = 'post_edit'
    permission_required = 'board.change_post'

    def form_valid(self, form):
        post = form.save(commit=False)
        if post.author == self.request.user:
            return super().form_valid(form)
        else:
            return HttpResponseBadRequest(
                f'{self.request.user.username}, чтобы редактировать пост, необходимо быть его автором')


class AnnouncementDelete(PermissionRequiredMixin, DeleteView):
    model = Announcement
    template_name = 'post_delete.html'
    context_object_name = 'post_delete'
    success_url = reverse_lazy('posts')
    permission_required = 'board.delete_post'


class CommentList(ListView, PermissionRequiredMixin):
    model = Comment
    template_name = 'comments.html'
    context_object_name = 'comments'
    ordering = '-date'
    permission_required = 'board.add_post'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context

    def get_queryset(self, **kwargs):
        queryset = super().get_queryset()
        self.filterset = CommentFilter(self.request.GET, queryset)
        return self.filterset.qs


class CommentDetail(PermissionRequiredMixin, DeleteView):
    model = Comment
    ordering = '-date'
    context_object_name = 'comment'
    template_name = 'comment.html'
    success_url = reverse_lazy('posts')
    permission_required = 'board.add_post'


class CommentCreate(PermissionRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'comment_edit.html'
    context_object_name = 'comment_edit'
    success_url = reverse_lazy('posts')
    permission_required = 'board.add_comment'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def form_valid(self, form):
        comment = form.save(commit=False)
        comment.comment_post = Announcement.objects.get(id=self.kwargs.get("pk"))
        comment.comment_author =self.request.user
        comment.save()
        return redirect(f'/posts/{self.kwargs.get("pk")}')


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
        comment.active = True
        comment.save()
        return HttpResponseRedirect('/posts/comments')
    # else:
    #     return HttpResponseRedirect('/accounts/login')


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

