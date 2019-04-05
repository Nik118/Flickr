from rest_framework import serializers
from photos.models import Group, Image


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    """
    This serializer serializes the Group model.
    """
    user = serializers.ReadOnlyField(source='user.username')
    no_of_photos = serializers.SerializerMethodField()

    class Meta:
        model = Group
        fields = ('user', 'group_id', 'url', 'no_of_photos')

    def get_no_of_photos(self, obj):
        return Image.objects.filter(group__group_id=obj.group_id).count()


class ImageSerializer(serializers.HyperlinkedModelSerializer):
    """
    This serializer serializes the Image model.
    """
    group = serializers.HyperlinkedRelatedField(read_only=True,
                                                view_name='group-detail')

    class Meta:
        model = Image
        fields = ('title', 'description', 'group', 'image_id', 'image_url',
                  'is_public', 'is_family', 'is_friend', 'added_date', 'url')
