# 임시로 만듦 삭제예정

# from django.db import models
# from django.contrib.auth import get_user_model

# User = get_user_model()


# class Lab(models.Model):
#     user = models.ForeignKey(
#         User,
#         on_delete=models.CASCADE,
#         related_name='labs')
#     title = models.CharField(max_length=255)
#     result = models.TextField()
#     created_at = models.DateTimeField(auto_now_add=True)


# class FreeMarket(models.Model):
#     user = models.ForeignKey(
#         User,
#         on_delete=models.CASCADE,
#         related_name='freemarket')
#     item_name = models.CharField(max_length=255)
#     quantity = models.CharField(max_length=50)
#     created_at = models.DateTimeField(auto_now_add=True)
