from django.shortcuts import render, get_object_or_404

from ..models import YTvideos


def youtube_projects(request):
    videos = YTvideos.objects.all().order_by('-timestamp')
    for video in videos:
        if 'v=' in video.videolink:
            video.embed_id = video.videolink.split('v=')[-1].split('&')[0]
        else:
            video.embed_id = ''
    return render(request, 'YoutubeSection/youtube_projects.html', {'videos': videos})


def video_player(request, video_id):
    video = get_object_or_404(YTvideos, ytid=video_id)
    # Extract video ID from link like 'https://www.youtube.com/watch?v=VIDEO_ID'
    embed_id = video.videolink.split('v=')[-1]
    context = {
        'video': video,
        'embed_id': embed_id
    }
    return render(request, 'YoutubeSection/video_player.html', context)
