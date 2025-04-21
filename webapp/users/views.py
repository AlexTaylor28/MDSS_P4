from django.shortcuts import render
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404

from .models import User

@login_required
def toggle_follow(request):
    if request.method == "POST":
        target_id = request.POST.get("user_id")
        target_user = get_object_or_404(User, id=target_id)
        user = request.user

        if target_user in user.following.all():
            user.unfollow_user(target_user)
            followed = False
        else:
            user.follow_user(target_user)
            followed = True

        return JsonResponse({"followed": followed})
    return JsonResponse({"error": "Invalid request"}, status=400)

def users_list_view(request):
    users = User.objects.all()

    now = timezone.now()
    for user in users:
        user.is_recent = user.last_login and (now - user.last_login) <= timedelta(days=1)

    return render(request, "users_list.html", {"users": users})

def user_detail_view(request, user_id):
    user = User.objects.get(id=user_id)
    context = {"user": user}
    return render(request, "user_detail.html", context)

