from rest_framework.serializers import ModelSerializer
from maps.models import Screenshot


class ScreenshotCreateSerializer(ModelSerializer):
    class Meta:
        model = Screenshot
        fields = [
            'screenshot'
        ]
