from django.shortcuts import render

from django.views.generic import TemplateView, ListView
from frontpage.models import DoneSummary


class DoneSummaryView(ListView):
    template_name = "done_summary.html"
    model = DoneSummary      # shorthand for setting queryset = models.Car.objects.all()
    # context_object_name = "objects"    #default is object_list as well as model's_verbose_name_list and/or model's_verbose_name_plural_list, if defined in the model's inner Meta class
    paginate_by = 50  #and that's it !!

    # @method_decorator(csrf_exempt)
    # def dispatch(self, request, *args, **kwargs):
    #   return super(DoneSummaryView, self).dispatch(request, *args, **kwargs)

    # def get_context_data(self, *args, **kwargs):
    #   context = super(DoneSummaryView, self).get_context_data(*args, **kwargs)
    #   context['objects'] = DoneSummary.objects.filter()
    #   return context

    # def get(self, request, *args, **kwargs):
    #     return self.render_to_response(self.get_context_data())
    #     
    def get_queryset(self):
        queryset = DoneSummary.objects.all()
        code = self.request.GET.get("code")
        if code:
            try:
                queryset = queryset.filter(code=code)
            except:
            	pass
                # Display error message
        return queryset   

#url(r'list/$', AnimalList.as_view(), name = 'animal_list'),

# class AnimalList(ListView):
#     model = Animal

#     def get_queryset(self):
#         queryset = Animal.objects.all()
#         hpk = self.request.GET.get("hpk"):
#         if hpk:
#             try:
#                 queryset = queryset.filter(herd=hpk)
#             except:
#                 # Display error message
#         return queryset