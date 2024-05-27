from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response


class CustomPagination(LimitOffsetPagination):
    def get_paginated_response(self, data, message=None):
        try:
            if message is None:
                message = 'Successfully fetched requested data.'
            from accounts_engine.views import success_true_response
            return Response(success_true_response(message=message, data=data, count=self.count))
        except Exception as e:
            from accounts_engine.views import success_false_response
            return Response(success_false_response(message=str(e)))
