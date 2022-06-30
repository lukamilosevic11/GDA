from django.urls import path
from .views import IndexView, AnnotationRowsListJson, AnnotationView, parsing_triggered, update_data, \
    initialize_before_parsing

urlpatterns = [
    path('', IndexView.as_view(), name="index"),
    path("annotation_file/", AnnotationView.as_view(), name="annotation_file"),
    path("parsing/", parsing_triggered, name="parsing_triggered"),
    path("update_data/", update_data, name="update_data"),
    path("initialize_parsing/", initialize_before_parsing, name="initialize_before_parsing"),
    path("annotation_data/", AnnotationRowsListJson.as_view(), name="annotation_list_json"),
]
