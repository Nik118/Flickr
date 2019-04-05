import arrow
# from django.contrib.auth import authenticate
from django_filters.rest_framework import DjangoFilterBackend
from django_filters import Filter, FilterSet
import requests
from photos.models import Group, Image
from photos.serializers import GroupSerializer, ImageSerializer
from photos.permissions import IsOwnerOrReadOnly
from rest_framework.permissions import IsAuthenticated
from rest_framework import filters, status, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView

# Create your views here.


# class Login(APIView):
#     permission_classes = (AllowAny,)
#
#     def get(self, request, format=None):
#         username = request.query_params.get('username')
#         password = request.query_params.get('password')
#         user = authenticate(username=username, password=password)
#         if not user:
#             return Response({'error': 'Login failed'},
#                             status=status.HTTP_401_UNAUTHORIZED)
#         token, created = Token.objects.get_or_create(user=user)
#         return Response({'token': token.key}, status=status.HTTP_200_OK)


class DataSetFilter(FilterSet):
    image_id = Filter(lookup_expr='gt')

    class Meta:
        model = Image
        fields = ['image_id', 'group', 'is_public']


class Logout(APIView):
    """
    This view will delete the token associated with the user and forces
    the user to login again.
    """
    def get(self, request, format=None):
        # simply delete the token to force a login
        Token.objects.get(user=request.user).delete()
        return Response({'message': 'Logged out'}, status=status.HTTP_200_OK)


class CreateGroup(APIView):
    """
    This view is for extracting group related data and image related data
    from flickr APIs
    """
    def get(self, request, format=None):
        group_id = request.query_params.get('group_id')
        url = 'https://api.flickr.com/services/rest/?method=' \
              'flickr.groups.pools.getPhotos&api_key=' \
              '4fb0946eb8e41c0121381f40e772c414&group_id=' \
              '{0}&format=json&nojsoncallback=1'.format(group_id)

        r = requests.get(url)
        if r.status_code == 200:
            res = r.json()
        else:
            raise Exception('An error has occurred')

        res_list = []
        group, created = Group.objects.get_or_create(user=request.user,
                                                     group_id=group_id)

        for image in res['photos']['photo']:
            image_id = image['id']
            title = image['title']
            date = arrow.get(image['dateadded']).datetime
            is_public = True if image['ispublic'] == 1 else False
            is_friend = True if image['isfriend'] == 1 else False
            is_family = True if image['isfamily'] == 1 else False

            # Get URL of the image by image_id
            image_url = 'https://api.flickr.com/services/rest/?method=' \
                        'flickr.photos.getInfo&api_key=' \
                        '4fb0946eb8e41c0121381f40e772c414&' \
                        'photo_id={0}&format=' \
                        'json&nojsoncallback=1'.format(image_id)
            r = requests.get(image_url)
            if r.status_code == 200:
                result = r.json()
            else:
                raise Exception('An error has occurred')

            image_url = result['photo']['urls']['url'][0]['_content']
            description = result['photo']['description']['_content']

            image = Image(group=group, image_id=image_id, title=title,
                          added_date=date, is_public=is_public,
                          is_friend=is_friend, is_family=is_family,
                          image_url=image_url, description=description)
            res_list.append(image)

        Image.objects.bulk_create(res_list, batch_size=50)
        return Response(status=status.HTTP_200_OK)


class GroupViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides list, create, retrieve,
    update and destroy actions for Group model.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    filter_backends = (filters.SearchFilter, filters.OrderingFilter)
    search_fields = ('user__username',)
    ordering_fields = ('id',)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ImageViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides list, create, retrieve,
    update and destroy actions for Image model.
    """
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter,
                       filters.OrderingFilter)
    # filter_fields = ('group',)
    search_fields = ('title',)
    ordering_fields = ('id', 'image_id', 'added_date',)
    permission_classes = (IsOwnerOrReadOnly, IsAuthenticated,)
    filter_class = DataSetFilter
