from django.contrib.auth.decorators import login_required
from django.shortcuts import render

def home(request):
    return render(request, 'deliveryLavalle_site/index.html')