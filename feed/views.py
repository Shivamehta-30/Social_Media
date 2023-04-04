from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Video, Comment


class VideoListView(ListView):
    model = Video
    template_name = 'video_list.html'
    context_object_name = 'videos'
    paginate_by = 10


class VideoDetailView(DetailView):
    model = Video
    template_name = 'video_detail.html'
    context_object_name = 'video'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        comments = Comment.objects.filter(
            video=self.object).order_by('-created_at')
        context['comments'] = comments
        return context


class VideoCreateView(CreateView):
    model = Video
    template_name = 'video_form.html'
    fields = ['title', 'video']
    success_url = reverse_lazy('video_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, 'Video uploaded successfully!')
        return super().form_valid(form)


class VideoUpdateView(UpdateView):
    model = Video
    template_name = 'video_form.html'
    fields = ['title', 'video']
    success_url = reverse_lazy('video_list')

    def form_valid(self, form):
        messages.success(self.request, 'Video updated successfully!')
        return super().form_valid(form)


class VideoDeleteView(DeleteView):
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


def like_post(request):
    post_id = request.POST.get('post_id')
    post = get_object_or_404(Video, id=post_id)
    post.likes += 1
    post.save()
    return JsonResponse({'success': True})
