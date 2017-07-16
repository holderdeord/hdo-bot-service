import json

from rest_framework.renderers import JSONRenderer

from api.serializers.manuscript import BaseManuscriptSerializer


def render_and_load_manuscript(manuscript):
    return json.loads(JSONRenderer().render(BaseManuscriptSerializer(manuscript).data).decode())
