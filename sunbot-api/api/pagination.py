from rest_framework import pagination
from rest_framework.response import Response


class CustomPageNumberPagination(pagination.PageNumberPagination):

    def get_paginated_response(self, data, total=None, total_1=None, total_2=None):
        return Response({
            "next": self.get_next_link(),
            "previous": self.get_previous_link(),
            "current": self.page.number,
            "last": self.page.paginator.num_pages,
            "count": self.page.paginator.count,
            "total": total,
            "total_1": total_1,
            "total_2": total_2,
            "results": data,
        })