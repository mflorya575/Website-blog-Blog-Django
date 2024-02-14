import os
import django
from django.utils import timezone
from django.db import connection
from blog.models import Post

# Установка переменной окружения, чтобы Django знал, какую конфигурацию использовать
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myproject.settings")
django.setup()

def update_timezones():
    print("Updating timezones...")
    for post in Post.objects.all():
        print(f"Old publish: {post.publish}")
        post.publish = post.publish.replace(tzinfo=timezone.utc)
        post.save()
        print(f"New publish: {post.publish}")
    print("Timezones updated.")
    connection.close()

if __name__ == "__main__":
    update_timezones()
