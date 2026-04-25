from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.core.exceptions import MultipleObjectsReturned

UserModel = get_user_model()

class EmailBackend(ModelBackend):
    '''
    Custom authentication backend that allows authenticating users 
    using their email address instead of a username.
    '''
    
    def authenticate(self, request, email=None, password=None, **kwargs):
        '''
        Authenticates a user based on email and password.
        '''
        # 1.2.3: Support for passing email directly or via USERNAME_FIELD kwargs
        if email is None:
            email = kwargs.get(UserModel.USERNAME_FIELD)

        try:
            # 1.2.4: Search for the user by the email field
            user = UserModel.objects.get(email=email)
        except (UserModel.DoesNotExist, MultipleObjectsReturned):
            # 1.2.5: Return None if user is not found
            return None

        # 1.2.4: Check password and ensure user is allowed to authenticate (is_active etc)
        if user.check_password(password) and self.user_can_authenticate(user):
            return user
        
        # 1.2.5: Return None if password validation fails
        return None