from django.shortcuts import render

# Create your views here.
def category(request):
    context = {}
    return render(request, 'category/category.html', context)