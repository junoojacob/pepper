from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):

    def create_user(self, username, email, password,phone ):
        username = self.normalze_email(username)
        user = self.model(username=username,email=email,phone=phone)
        user.set_password(password)
        user.save()
        return user


