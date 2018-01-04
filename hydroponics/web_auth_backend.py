from django.contrib.auth.backends import RemoteUserBackend
from django.http import HttpResponseRedirect
from django.contrib.auth import get_user_model


class HydroRemoteUserBackend(RemoteUserBackend):
    create_unknown_user = False

    def authenticate(self, remote_user):
        if not remote_user:
            return
        user = None
        username = self.clean_username(remote_user)

        UserModel = get_user_model()

        if self.create_unknown_user:
            user, created = UserModel._default_manager.get_or_create(**{
                UserModel.USERNAME_FIELD: username
            })
            if created:
                user = self.configure_user(user)
        else:
            try:
                user = UserModel._default_manager.get_by_natural_key(username)
            except UserModel.DoesNotExist:
                HttpResponseRedirect("/path/")
        return user
