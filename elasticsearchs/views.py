from elasticsearch_dsl import Q
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .documents import MediaContentDocument
from .serializers import MediaContentSerializer
from accounts_engine.utils import success_false_response, success_true_response
from rest_framework_simplejwt.authentication import JWTAuthentication
import logging

logger = logging.getLogger(__name__)
logger_info = logging.getLogger('info')
logger_error = logging.getLogger('error')


class MediaContentSearchView(APIView):
    authentication_classes = [JWTAuthentication]

    def get(self, request, *args, **kwargs):
        try:
            user = request.user
            if not user.is_authenticated:
                return Response({"error": "Authentication required."}, status=status.HTTP_401_UNAUTHORIZED)

            query_params = request.query_params

            title = query_params.get('title', None)
            description = query_params.get('description', None)
            awards = query_params.get('awards', None)
            genre = query_params.get('genre', None)
            directors = query_params.getlist('directors', [])
            actors = query_params.getlist('actors', [])
            # print('------------------------------------------------')
            # print('directors: ')
            # print(directors)

            start_date = query_params.get('release_year_start', None)
            end_date = query_params.get('release_year_end', None)

            es_query = Q()

            if awards:
                es_query &= Q('nested', path='awards', query=Q('match', awards__name={"query": awards, "fuzziness": "AUTO"}))

            if genre:
                es_query &= Q('nested', path='genre', query=Q('match', genre__name={"query": genre, "fuzziness": "AUTO"}))

            if directors:
                for director in directors:
                    es_query &= Q('nested', path='director', query=Q('match', director__name={"query": director, "fuzziness": "AUTO"}))

            if actors:
                for actor in actors:
                    es_query &= Q('nested', path='actors', query=Q('match', actors__name={"query": actor, "fuzziness": "AUTO"}))

            if title:
                es_query &= Q('match', title={"query": title, "fuzziness": "AUTO"})

            if description:
                es_query &= Q('match', description={"query": description, "fuzziness": "AUTO"})

            if start_date:
                if end_date:
                    es_query &= Q('range', release_year={"gte": start_date, "lte": end_date})
                else:
                    es_query &= Q('range', release_year={"gte": start_date}) # getter then equal to.

            search_results = MediaContentDocument.search().query(es_query).to_queryset()
            search_results = search_results.order_by('-created_date')
            serializer = MediaContentSerializer(search_results, many=True)

            message = "Successfully fetched content based on search parameters"
            logger_info.info(message)

            return Response(success_true_response(data=serializer.data, message=message), status=status.HTTP_200_OK)

        except Exception as e:
            message = str(e)
            logger_error.error(message)
            return Response(
                success_false_response(message='An unexpected error occurred. Please try again later.'),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
