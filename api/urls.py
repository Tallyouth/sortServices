from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from api.views import ScoreProcess

urlpatterns = [
    url(r'^v1/score$', ScoreProcess.as_view()),  # 获取分数排行(get)
]
urlpatterns = format_suffix_patterns(urlpatterns)
