import json

from rest_framework.renderers import JSONRenderer


def render_and_load_serializer_data(serializer):
    return json.loads(JSONRenderer().render(serializer.data).decode())
