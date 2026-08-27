from .models import Category

def menu_links(request):
    links= Category.objects.all()
    return dict(links=links)



# def menu_categories(request):
#     return {
#         'all_categories': Category.objects.all()
#     }