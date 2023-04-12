from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Video, Comment
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


class VideoListView(LoginRequiredMixin, ListView):
    model = Video
    template_name = 'video_list.html'
    context_object_name = 'videos'
    paginate_by = 10


class VideoDetailView(LoginRequiredMixin, DetailView):
    model = Video
    template_name = 'video_detail.html'
    context_object_name = 'video'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        comments = Comment.objects.filter(
            video=self.object).order_by('-created_at')
        context['comments'] = comments
        return context


class VideoCreateView(LoginRequiredMixin, CreateView):
    model = Video
    template_name = 'feed/video_form.html'
    fields = ['title', 'video']
    success_url = reverse_lazy('view')

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, 'Video uploaded successfully!')
        return super().form_valid(form)


class VideoUpdateView(LoginRequiredMixin, UpdateView):
    model = Video
    template_name = 'video_form.html'
    fields = ['title', 'video']
    success_url = reverse_lazy('VideoListView')

    def form_valid(self, form):
        messages.success(self.request, 'Video updated successfully!')
        return super().form_valid(form)


class VideoDeleteView(LoginRequiredMixin, DeleteView):
    model = Video
    template_name = 'video_confirm_delete.html'
    success_url = reverse_lazy('video_list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Video deleted successfully!')
        return super().delete(request, *args, **kwargs)


@login_required
def add_comment_to_video(request, pk):
    video = get_object_or_404(Video, pk=pk)
    if request.method == 'POST':
        comment_text = request.POST.get('comment_text')
        comment = Comment.objects.create(
            video=video, user=request.user, comment=comment_text)
        comment.save()
        messages.success(request, 'Comment added successfully!')
        return redirect('video_detail', pk=pk)
    else:
        return redirect('video_detail', pk=pk)


def Dashboard(request):
    print("Dashboard view called")
    videos = Video.objects.all()
    return render(request, 'Dashboard.html', {'videos': videos})


def like_video(request):
    print("In like_post")
    if request.method == 'POST':
        print("In If")
        video_id = request.POST.get('video_id')
        post = Video.objects.get(id=video_id)
        print(post)
        post.likes += 1
        post.save()
        return JsonResponse({'status': 'success'})
    else:
        return JsonResponse({'status': 'error'})

@login_required
def add_comment(request, pk):
    if request.method == 'POST':
        comment = Comment()
        comment.user = request.user
        comment.video_id = request.POST.get('video-id')
        comment.comment = request.POST.get('comment')
        comment.save()
        return redirect('/')
    else:
        return redirect('home')
