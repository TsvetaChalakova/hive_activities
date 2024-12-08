# from django.contrib.auth import get_user_model
# from django.db.models.signals import post_delete
# from django.dispatch import receiver
#
# UserModel = get_user_model()
#
#
# @receiver(post_delete, sender=UserModel)
# def delete_user_on_profile_delete(sender, instance, **kwargs):
#     if instance.user:
#         instance.user.delete()

# We are not deleting users when profiles are deleted, just deactivate them.
