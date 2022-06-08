from goals.models import Goal

def menu_goals(request):
    if request.user.is_authenticated:
        try:
            goals = Goal.objects.filter(user=request.user).latest('-end_date')
        except:
            goals = None
    else:
        try:
            goals = Goals.objects.get(user=None, id=id, session_key=request.session.session_key).latest('-end_date')
        except:
            goals = None

    return dict(goals=goals)