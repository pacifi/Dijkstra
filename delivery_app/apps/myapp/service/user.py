from django.core import serializers

from django.http import HttpResponse
from django.views import View

import simplejson as json

from backend_apps.backend_auth.models import User


class UserViewJson(View):
    def get(self, *args, **kwargs):
        print("User testing")
        pedidos = User.objects.filter()
        tmpJson = serializers.serialize("json", pedidos)
        tmpObj = json.loads(tmpJson)
        dump = json.dumps(tmpObj)
        return HttpResponse(dump, status=200, content_type="application/json")
