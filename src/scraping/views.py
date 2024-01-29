from django.shortcuts import render

#from .forms import FindForms
from .models import Vacancy


def home_view(request):
    qs = Vacancy.objects.all()
    return render(request, 'home.html', {'object_list': qs })
    #form = FindForms()
    #city = request.GET.get('city')
    #language = request.GET.get('language')
    #qs = []
    #if city or language:
     #   _filter = {}
      #  if city:
       #     _filter['city__slug'] = city
        #if language:
        #    _filter['language__slug'] = language

        #qs = Vacancy.objects.filter(**_filter)
    #return render(request, 'scraping/base.html', {'object_list': qs, 'form': form})
#from django.shortcuts import render

# Create your views here.
