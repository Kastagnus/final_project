from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

# კლასი რომელის გადაცემულია დჯანგოს ავტორიზაციის სეთინგებში
# მომხმარებს შეუძლია ავტორიზაცია როგორც ელ ფოსტით ასევე იუზერნეიმით
# class EmailOrUsernameModelBackend(ModelBackend):
#     def authenticate(self, request, username=None, password=None, **kwargs):
#         UserModel = get_user_model()
#         if username is None:
#             username=kwargs.get(UserModel.USERNAME_FIELD)
#         try:
#             user = UserModel._default_manager.get_by_natural_key(username)
#         except UserModel.DoesNotExist:
#             user=None
#
#         if user is None:
#             try:
#                 user=UserModel._default_manager.get(email=username)
#             except UserModel.DoesNotExist:
#                 user=None
#         if user is not None and user.check_password(password):
#             return user
#         return None

from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q


class EmailOrUsernameModelBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        UserModel = get_user_model()
        if username is None:
            username = kwargs.get(UserModel.USERNAME_FIELD)

        try:
            user = UserModel.objects.get(Q(username=username) | Q(email=username))
        except UserModel.DoesNotExist:
            return None

        if user is not None and user.check_password(password):
            return user
        return None

