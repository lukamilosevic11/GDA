from django.core.management import call_command
from django.http import JsonResponse
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_protect
from django.views.generic import TemplateView
from django_datatables_view.base_datatable_view import BaseDatatableView
from GDA_backend.Classes.event import Subject, Observer
from GDA_backend.Classes.parsing import Parsing
from GDA_backend.Common.init import Lock, time
from GDA_backend.Common.constants import ERROR_LOG_PATH
from .apps import FrontendTracker
from .models import AnnotationRowModel


@csrf_protect
def initialize_before_parsing(request):
    if request.method == 'POST':
        frontendTracker = FrontendTracker()
        frontendTracker.progress = 0
        frontendTracker.parsing = True
        frontendTracker.parsingStarted = False
        frontendTracker.spinner = False

    return redirect("index")


@csrf_protect
def update_data(request):
    if request.method == 'POST':
        frontendTracker = FrontendTracker()
        resp_data = {
            'parsing': frontendTracker.parsing,
            'progress': frontendTracker.progress,
            'spinner': frontendTracker.spinner,
            'showError': frontendTracker.showError
        }

        return JsonResponse(resp_data, status=200)

    return redirect("index")


@csrf_protect
def parsing_triggered(request):
    frontendTracker = FrontendTracker()

    if request.method == "POST" and not frontendTracker.parsingStarted:
        try:
            initializeSearchEngine = request.POST.get("initializeSearchEngine") == 'true'
            frontendTracker.parsingStarted = True
            frontendTracker.parsing = True
            frontendTracker.progress = 0
            frontendTracker.spinner = False
            progressSubject = Subject(Lock())
            observer = Observer(frontendTracker)
            progressSubject.attach(observer)
            Parsing.parse(progressSubject, initializeSearchEngine)
            frontendTracker.spinner = True
            call_command('migrate', 'GDA_datatables', '0001', '--fake')
            call_command('migrate', 'GDA_datatables', '0002')
            frontendTracker.parsing = False
            frontendTracker.parsingStarted = False
            frontendTracker.spinner = False
        except Exception as e:
            print(e)
            with open(ERROR_LOG_PATH, "w") as errorFile:
                errorFile.write(str(e))

            frontendTracker.showError = True
            time.sleep(1.5)
            frontendTracker.parsingStarted = False
            frontendTracker.parsing = False
            frontendTracker.progress = 0
            frontendTracker.spinner = False
            frontendTracker.showError = False

    return redirect("index")


class IndexView(TemplateView):
    template_name = 'GDA_datatables/index.html'

    def get_context_data(self, **kwargs):
        frontendTracker = FrontendTracker()
        context = super(IndexView, self).get_context_data(**kwargs)
        context["parsing"] = frontendTracker.parsing
        context["progress"] = frontendTracker.progress
        context["spinner"] = frontendTracker.spinner

        return context


class AnnotationView(TemplateView):
    template_name = 'GDA_datatables/annotation_file.html'

    def get_context_data(self, **kwargs):
        frontendTracker = FrontendTracker()
        context = super().get_context_data(**kwargs)
        context["parsing"] = frontendTracker.parsing
        context["progress"] = frontendTracker.progress
        context["spinner"] = frontendTracker.spinner

        return context


class AnnotationRowsListJson(BaseDatatableView):
    model = AnnotationRowModel

    def get_context_data(self, **kwargs):
        frontendTracker = FrontendTracker()
        context = super().get_context_data(**kwargs)
        context["parsing"] = frontendTracker.parsing
        context["progress"] = frontendTracker.progress
        context["spinner"] = frontendTracker.spinner

        return context
