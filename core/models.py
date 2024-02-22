from django.db import models
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.utils.timezone import now

# Create your models here.
class ManeloUser(User):
    
    
    # Existing fields
    def user_directory_path(instance, filename):
        # file will be uploaded to MEDIA_ROOT/users/images/<id>/<filename>
        return 'users/images/{0}/{1}'.format(instance.pk, filename)
    
    profile_picture = models.ImageField(upload_to=user_directory_path, default="default_user_icon.jpg", blank=True)
    
    # Additional fields for profile picture processing can be added here or handled in the view or serializer layer

    # New fields as per enhanced requirements
    bio = models.TextField(blank=True, null=True)
    birthdate = models.DateField(blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    gender = models.CharField(max_length=50, blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    social_media_links = models.JSONField(blank=True, null=True)  # Stores social media links as a JSON object
    language_preference = models.CharField(max_length=10, blank=True, null=True)  # ISO language code
    time_zone = models.CharField(max_length=50, blank=True, null=True)
    account_creation_date = models.DateTimeField(auto_now_add=True)
    #last_login = models.DateTimeField(default=now)
    verification_status = models.BooleanField(default=False)
    user_status = models.CharField(max_length=10, blank=True, null=True)  # e.g., online, offline, away
    interests = models.ManyToManyField('Interest', blank=True)  # Assuming an Interest model exists
    accessibility_settings = models.JSONField(blank=True, null=True)  # Stores accessibility preferences as a JSON object

    # Enhanced privacy settings
    #privacy_settings = models.CharField(max_length=10, choices=ManeloUser.PRIVACY_CHOICES, default='public', blank=True)
    friends = models.ManyToManyField('self', blank=True, symmetrical=True)

    # Method for full name (assuming parent User model has first_name and last_name fields)
    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    # Method for profile picture processing (pseudo code)
    def get_profile_picture_versions(self):
        # Return different versions of the profile picture (thumbnails, high-resolution, etc.)
        pass

    # Quick access method for the user's unique ID
    def get_unique_id(self):
        return self.pk

    def __str__(self):
        return self.full_name()  # Utilizes the full_name method for display

# Example Interest model
class Interest(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


def post_image_upload_to(instance, filename):
    return f'users/images/{instance.author.pk}/{filename}'
class Post(models.Model):
    
    author = models.ForeignKey(ManeloUser, on_delete=models.CASCADE, related_name='posts')
    content = models.TextField()
    image = models.ImageField(upload_to=post_image_upload_to, blank=True, null=True)  # Use named function
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.content[:50]

    class Meta:
        ordering = ['-created_at']
    
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(ManeloUser, on_delete=models.CASCADE, related_name='user_comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.content[:50]
    
    
class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes', null=True, blank=True)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='likes', null=True, blank=True)
    user = models.ForeignKey(ManeloUser, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'post', 'comment')  # Ensure a user can like a post/comment only once.
        
        
        
class Group(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    members = models.ManyToManyField(ManeloUser, through='GroupMember')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class GroupMember(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    user = models.ForeignKey(ManeloUser, on_delete=models.CASCADE)
    joined_at = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user.full_name()} - {self.group.name}'
    
    
    
class Message(models.Model):
    sender = models.ForeignKey(ManeloUser, related_name='sent_messages', on_delete=models.CASCADE)
    recipient = models.ForeignKey(ManeloUser, related_name='received_messages', on_delete=models.CASCADE)
    content = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)
    read_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f'From {self.sender.full_name()} to {self.recipient.full_name()}'


class Notification(models.Model):
    NOTIFICATION_TYPES = (('like', 'Like'), ('comment', 'Comment'), ('message', 'Message'))
    recipient = models.ForeignKey(ManeloUser, on_delete=models.CASCADE, related_name='notifications')
    sender = models.ForeignKey(ManeloUser, on_delete=models.CASCADE, null=True, blank=True, related_name='+')
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
    text = models.TextField()  # Additional info that can be shown in the notification
    read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Notification for {self.recipient.full_name()}'
