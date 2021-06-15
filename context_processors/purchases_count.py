from recipes.models import Purchase


def count(request):
    count = Purchase.objects.filter(user=request.user.id).count()
    return {'count': count}
