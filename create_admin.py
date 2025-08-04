from django.contrib.auth import get_user_model

User = get_user_model()

if not User.objects.filter(username="admin").exists():
    User.objects.create_superuser("admin@example.com", "123")
    print("✅ Admin create")
else:
    print("ℹ️ Admin was created")