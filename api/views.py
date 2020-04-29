# coding: utf-8

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from collections import OrderedDict
from rest_framework.exceptions import NotFound
from api.serializers import ScoreSerializer
from api.models import ScoreTable


# 成功请求
class OkResponse(Response):
    def __init__(self, data=None, **kwargs):
        _data = {}
        if data:
            _data['data'] = data
        _data['code'] = 200
        _data['msg'] = 'success'
        super().__init__(_data, **kwargs)


# 失败请求
class FailResponse(Response):
    def __init__(self, data=None, code=40000, msg='fail', **kwargs):
        _data = {}
        if data:
            _data['data'] = data
        _data['code'] = code
        _data['msg'] = msg
        super().__init__(_data, **kwargs)


def _positive_int(integer_string, strict=False, cutoff=None):
    """
    Cast a string to a strictly positive integer.
    """
    ret = int(integer_string)
    if ret < 0 or (ret == 0 and strict):
        raise ValueError()
    if cutoff:
        return min(ret, cutoff)
    return ret


# 分页功能
class CustomPageNumberPagination(PageNumberPagination):
    def __init__(self,
                 page_size_query_param=100,
                 page_query_param=1,
                 page_size=100,
                 max_page_size=1000):
        self.page_size = page_size
        self.page_size_query_param = page_size_query_param
        self.page_query_param = page_query_param
        self.max_page_size = max_page_size

    def get_page_size(self, request):
        if self.page_size_query_param:
            try:
                return _positive_int(self.page_size_query_param,
                                     strict=True,
                                     cutoff=self.max_page_size)
            except (KeyError, ValueError):
                pass

        return self.page_size

    def paginate_queryset(self, queryset, request, view=None):
        """
        Paginate a queryset if required, either returning a
        page object, or `None` if pagination is not configured for this view.
        """
        page_size = self.get_page_size(request)
        if not page_size:
            return None

        paginator = self.django_paginator_class(queryset, page_size)
        page_number = self.page_query_param
        if page_number in self.last_page_strings:
            page_number = paginator.num_pages

        try:
            self.page = paginator.page(page_number)
        except Exception as exc:
            msg = self.invalid_page_message.format(page_number=page_number,
                                                   message=str(exc))
            raise NotFound(msg)

        if paginator.num_pages > 1 and self.template is not None:
            # The browsable API should display pagination controls.
            self.display_page_controls = True

        self.request = request
        return list(self.page)

    def get_paginated_response(self, data, request):
        return Response(
            OrderedDict([('count', self.page.paginator.count),
                         ('pageSize', self.get_page_size(request)),
                         ('page', self.page_query_param), ('results', data)]))


class ScoreProcess(APIView):
    def get(self, request):
        try:
            currentClient = request.GET.get('client')
            start = int(request.GET.get('start')) - 1 if request.GET.get(
                'start') else 0
            end = int(request.GET.get('end')) if request.GET.get('end') else 0
            if not currentClient:
                return FailResponse(msg='client为必传项')
            if start or end:
                if end == 0:
                    end = 100
                queryset = ScoreTable.objects.all().order_by(
                    '-score')[start:end]
            else:
                queryset = ScoreTable.objects.all().order_by('-score')
            querysetAll = ScoreTable.objects.all().order_by('-score')
            scoreList = [{
                '排名': i + start + 1,
                "客户端": j['client'],
                "分数": j['score']
            } for i, j in enumerate(ScoreSerializer(queryset, many=True).data)]
            for i, j in enumerate(
                    ScoreSerializer(querysetAll, many=True).data):
                if j['client'] == currentClient:
                    currentUser = {
                        "排名": i + 1,
                        "客户端": currentClient,
                        "分数": j['score']
                    }
                    scoreList.append(currentUser)
            return OkResponse(data=scoreList)
        except Exception as identifier:
            return FailResponse(msg=str(identifier))

    def post(self, request):
        try:
            client = request.data['client']
            score = request.data['score']
            if not isinstance(score, int):
                return FailResponse(msg='分数必须为int')
            ScoreTable.objects.update_or_create(client=client,
                                                defaults=request.data)
            return OkResponse()
        except Exception as identifier:
            return FailResponse(msg=str(identifier))
