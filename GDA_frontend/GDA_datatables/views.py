import time

from django.views.generic import TemplateView
from django.shortcuts import redirect, render
from django_datatables_view.base_datatable_view import BaseDatatableView
from GDA_datatables.models import AnnotationRowModel
from django.views.decorators.csrf import csrf_protect
from GDA_datatables.apps import FrontendTracker
from django.core.management import call_command
from django.http import JsonResponse


@csrf_protect
def initialize_before_parsing(request):
    if request.method == 'POST':
        print("INIT")
        frontendTracker = FrontendTracker()
        frontendTracker.progress = 0
        frontendTracker.parsing = True
        frontendTracker.parsingStarted = False

    return redirect("index")


@csrf_protect
def update_data(request):
    print("UPDATE")
    if request.method == 'POST':
        frontendTracker = FrontendTracker()
        resp_data = {
            'parsing': frontendTracker.parsing,
            'progress': frontendTracker.progress
        }

        return JsonResponse(resp_data, status=200)


@csrf_protect
def parsing_triggered(request):
    frontendTracker = FrontendTracker()

    if request.method == "POST" and not frontendTracker.parsingStarted:
        frontendTracker.parsingStarted = True
        print("PARSING")
        initializeSearchEngine = request.POST.get("initializeSearchEngine") == 'true'
        frontendTracker.parsing = True
        frontendTracker.progress = 0
        for i in range(101):
            frontendTracker.progress = i
            time.sleep(0.1)
        # call_command('migrate', 'GDA_datatables', '0001', '--fake')
        # call_command('migrate', 'GDA_datatables', '0002')
        frontendTracker.parsing = False
        frontendTracker.parsingStarted = False

    return redirect("index")


class IndexView(TemplateView):
    template_name = 'GDA_datatables/index.html'

    def get_context_data(self, **kwargs):
        print("INDEX")
        frontendTracker = FrontendTracker()
        context = super(IndexView, self).get_context_data(**kwargs)
        context["parsing"] = frontendTracker.parsing
        context["progress"] = frontendTracker.progress

        return context


class AnnotationView(TemplateView):
    template_name = 'GDA_datatables/annotation_file.html'

    def get_context_data(self, **kwargs):
        frontendTracker = FrontendTracker()
        context = super().get_context_data(**kwargs)
        context["parsing"] = frontendTracker.parsing
        context["progress"] = frontendTracker.progress

        return context


class AnnotationRowsListJson(BaseDatatableView):
    model = AnnotationRowModel

    def get_context_data(self, **kwargs):
        frontendTracker = FrontendTracker()
        context = super().get_context_data(**kwargs)
        context["parsing"] = frontendTracker.parsing
        context["progress"] = frontendTracker.progress

        return context
