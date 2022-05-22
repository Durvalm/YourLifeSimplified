from .models import ToDoList

def menu_links(request):
    if request.user.is_authenticated:
        try:
            links = ToDoList.objects.filter(user=request.user, is_completed=False, is_late=False).latest('-end_date')
        except:
            links = None
    else:
        try:
            links = ToDoList.objects.get(user=None, id=id, is_completed=False, is_late=False, session_key=request.session.session_key).latest('-end_date')
        except:
            links = None

    return dict(links=links)