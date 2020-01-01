# coding: utf-8

from django.views.generic import View
from django.shortcuts import redirect, reverse

from app.libs.base_render import render_to_response
from app.utils.permission import dashboard_auth
from app.model.model_video import VideoType, FromType, IdentityType, NationalityType, Video, VideoSub, VideoStar
from app.utils.common import check_video_attribute


class ExternalVideo(View):
    template_name = 'dashboard/video/external_video.html'

    @dashboard_auth
    def get(self, request):
        data = {'error': request.GET.get('error')}
        video_list = Video.objects.filter(status=True)
        data['video'] = video_list
        return render_to_response(request, self.template_name, data=data)

    def post(self, request):
        name = request.POST.get('name')
        image = request.POST.get('image')
        info = request.POST.get('info')
        video_type = request.POST.get('video_type')
        from_to = request.POST.get('from_to')
        nationality = request.POST.get('nationality')

        print(name, image, info, video_type, from_to, nationality)
        if not all([name, image, info, video_type, from_to, nationality]):
            return redirect('{0}?error={1}'.format(reverse('external_link'), '缺少必要字段'))

        obj_type_list = {VideoType: video_type, FromType: from_to, NationalityType: nationality}
        for v_class, v_vaule in obj_type_list.items():
            result = check_video_attribute(v_class, v_vaule)
            if result:
                return redirect(
                    "{0}?error={1}".format(reverse('external_link'), result['value'] + "-" + result['message']))

        Video.objects.create(
            name=name,
            image=image,
            info=info,
            video_type=video_type,
            from_to=from_to,
            nationality=nationality
        )
        return redirect(reverse('external_link'))


class VideoSubView(View):
    template_name = 'dashboard/video/video_sub.html'

    @dashboard_auth
    def get(self, request, video_id):
        data = {}
        video = Video.objects.get(pk=video_id)
        data['error'] = request.GET.get('error')
        data['video'] = video
        return render_to_response(request, self.template_name, data)

    def post(self, request, video_id):
        url = request.POST.get('url')

        video = Video.objects.get(pk=video_id)
        VideoSub.objects.create(video=video, url=url, number=video.video_sub.count() + 1)
        return redirect(reverse('video_sub', kwargs={'video_id': video_id}))


class VideoStarView(View):

    def post(self, request):
        name = request.POST.get('name')
        identity = request.POST.get('identity')
        video_id = request.POST.get('video_id')

        if not all([name, identity, video_id]):
            return redirect("{0}?error={1}".format(reverse('video_sub', kwargs={'video_id': video_id}), "缺少必要的字段"))

        result = check_video_attribute(IdentityType, identity)

        if result:
            return redirect(
                "{0}?error={1}".format(reverse('video_sub', kwargs={'video_id': video_id}),
                                       "{0}-{1}".format(result['value'], result['message']))
            )

        video = Video.objects.get(pk=video_id)

        VideoStar.objects.create(
            video=video,
            name=name,
            identity=identity
        )
        return redirect(reverse('video_sub', kwargs={'video_id': video_id}))
