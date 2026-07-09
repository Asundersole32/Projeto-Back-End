from django.contrib.auth.models import BaseUserManager

class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, first_name, last_name, password=None, **extra_fields):
        if not email:
            raise ValueError("User must have an email address!")
        if not username: 
            raise ValueError("User must have a username!")
        
        user = self.model(
            email=self.normalize_email(email),
            username=username,
            first_name=first_name,
            last_name=last_name,
        )
        user.set_password(password)
        
        # Define campos extras dinamicamente (ex: is_admin, is_staff, is_superuser, is_active, etc.)
        for field, value in extra_fields.items():
            setattr(user, field, value)
        
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, username, first_name, last_name, password=None, **extra_fields):
        # Garante que o superusuário tenha privilégios
        extra_fields.setdefault('is_admin', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        # is_active geralmente é True por padrão, mas pode ser definido
        extra_fields.setdefault('is_active', True)
        
        return self.create_user(email, username, first_name, last_name, password, **extra_fields)