from django.db import models


class BaseModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

# TODO
# class Promise(BaseModel):
#     """ We will do A. We will not do B """
#     body
#     source
#     promisor_name
#     party_names
#     parliament_period_name
#
#
# class Manuscript(BaseModel):
#     # ordered list of promises and interims
#     pass
#
#
# class Interim(BaseModel):
#     pass
#
#
# class Response(BaseModel):
#     # user response
#     pass
#
#
# class Session(BaseModel):
#     # Holds state of message session
#     pass
#
#
# class UserProfile(BaseModel):
#     pass
