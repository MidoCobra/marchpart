from django.http import HttpResponse
from main.models import Multiple_enteries


# def Base(request):
#     pass


# def Currency(request):
#     multiple_entries = Multiple_enteries.objects.get(label='mult_enteries')
#     context = None
#     if request.method == 'GET' or request.method == 'POST':
#         try:
#             currency_choice = request.session['currency_choice']
#         except:
#             currency_choice = None

#         context = {
#             'currency_choice': currency_choice,
#             'multiple_entries': multiple_entries,
#         }
#     return context
