from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import *
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import View
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.db.models import Q


class VideoListView(LoginRequiredMixin, ListView):
    model = Video
    template_name = 'video_list.html'
    context_object_name = 'videos'
    # paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        comments = Comment.objects.order_by('-created_at')
        context['comments'] = {}
        for comment in comments:
            video_id = comment.video.id
            if video_id not in context['comments']:
                context['comments'][video_id] = []
            context['comments'][video_id].append(comment)

        # get follower data
        user = self.request.user
        following_ids = Follower.objects.filter(follower=user).values_list('followed__id', flat=True)
        context['following_ids'] = following_ids
        context['inPlayList'] = True
        return context

class VideoDetailView(LoginRequiredMixin, DetailView):
    model = Video
    template_name = 'video_detail.html'
    context_object_name = 'video'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        comments = Comment.objects.filter(
            video=self.object).order_by('-created_at')
        context['comments'] = comments
        print(context)
        return context
 

class VideoCreateView(LoginRequiredMixin, CreateView):
    model = Video
    template_name = 'feed/video_form.html'
    fields = ['title', 'video', 'videoDescription']
    success_url = reverse_lazy('view')

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, 'Video uploaded successfully!')
        return super().form_valid(form)


class VideoUpdateView(LoginRequiredMixin, UpdateView):
    model = Video
    template_name = 'video_form.html'
    fields = ['title', 'video', 'videoDescription']
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
    if request.method == 'POST':
        video_id = request.POST.get('video_id')
        a = Video_Likes.objects.filter(VideoId=video_id, LikeByUserId=request.user.id)
        print(a)
        if a.exists():
            print("In like condition")
            return JsonResponse({'status': 'error'})

        my_like = Video_Likes()
        my_like.VideoId = video_id
        my_like.LikeByUserId = request.user.id

        post = Video.objects.get(id=video_id)
        print(post)
        post.likes += 1
        post.save()
        my_like.save()
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


@login_required
@require_POST
def like_dislike_video(request):
    user_id = request.user.id
    video_id = request.POST.get('video_id')
    is_liked = request.POST.get('is_liked')

    video = get_object_or_404(Video, id=video_id)
    try:
        like_dislike = Video_Likes_dislikes.objects.get(video_id=video_id, Like_Dislike_ByUserId=user_id)
        a = False
    except Video_Likes_dislikes.DoesNotExist:
        like_dislike = Video_Likes_dislikes(video_id_id=video_id, Like_Dislike_ByUserId=user_id)

    if is_liked == 'true':
        if not like_dislike.VideoIsLiked == True:
            video.likes += 1
        like_dislike.VideoIsLiked = True

    else:
        if not like_dislike.VideoIsLiked == False:
            video.likes -= 1
        like_dislike.VideoIsLiked = False

    like_dislike.save()
    video.save()

    data = {'likes': video.likes}
    return JsonResponse(data)


class PlaylistCreateView(LoginRequiredMixin, CreateView):
    model = Playlist
    template_name = 'feed/playlist_form.html'
    fields = ['title']
    success_url = reverse_lazy('view')

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, 'Playlist created successfully!')
        return super().form_valid(form)


class PlaylistListView(LoginRequiredMixin, ListView):
    model = Playlist
    template_name = 'feed/playlist_list.html'
    context_object_name = 'playlists'

    def get_queryset(self):
        return Playlist.objects.filter(user=self.request.user)


@login_required
def add_to_playlist(request, pk):
    video = get_object_or_404(Video, pk=pk)
    playlists = Playlist.objects.filter(user=request.user)

    if request.method == 'POST':
        playlist_ids = request.POST.getlist('playlists')
        playlists = Playlist.objects.filter(id__in=playlist_ids)

        for playlist in playlists:
            PlaylistVideo.objects.create(
                playlist=playlist,
                video=video,
                added_by=request.user
            )

        messages.success(request, 'Video added to playlist successfully!')
        return redirect('view')

    return render(request, 'feed/add_to_playlist.html', {'video': video, 'playlists': playlists})


@login_required
def follow(request, user_id):
    followed_user = User.objects.get(id=user_id)
    follower = request.user
    Follower.objects.create(follower=follower, followed=followed_user)
    return redirect('view')


@login_required
def unfollow(request, user_id):
    followed_user = User.objects.get(id=user_id)
    follower = request.user
    Follower.objects.filter(follower=follower, followed=followed_user).delete()
    return redirect('view')


class VideoPlaylistListView(ListView):
    model = Video
    template_name = 'video_list.html'
    context_object_name = 'videos'

    def get_queryset(self):
        # get the playlist object based on the playlist_id parameter in the URL
        playlist_id = self.kwargs['playlist_id']
        playlist = get_object_or_404(Playlist, id=playlist_id)
        
        # filter the videos that belong to the playlist
        videos = playlist.videos.all().values_list('video__id', flat=True)
        return Video.objects.filter(id__in=videos)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        playlist_id = self.kwargs['playlist_id']
        context['playlist'] = get_object_or_404(Playlist, id=playlist_id)

        comments = Comment.objects.order_by('-created_at')
        context['comments'] = {}
        for comment in comments:
            video_id = comment.video.id
            if video_id not in context['comments']:
                context['comments'][video_id] = []
            context['comments'][video_id].append(comment)

        user = self.request.user
        following_ids = Follower.objects.filter(follower=user).values_list('followed__id', flat=True)
        context['following_ids'] = following_ids
        context['inPlayList'] = False

        return context



class VideoByFollowedUsers(ListView):
    model = Video
    template_name = 'feed\FollowersVideoList.html'
    context_object_name = 'videos'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        comments = Comment.objects.order_by('-created_at')
        context['comments'] = {}
        for comment in comments:
            video_id = comment.video.id
            if video_id not in context['comments']:
                context['comments'][video_id] = []
            context['comments'][video_id].append(comment)

        # get follower data
        user = self.request.user
        following_ids = Follower.objects.filter(follower=user).values_list('followed__id', flat=True)
        context['following_ids'] = following_ids
        context['inPlayList'] = True
        return context

@login_required
def aaa(request):
    return redirect('view')
