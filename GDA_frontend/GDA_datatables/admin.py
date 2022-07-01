from django.contrib import admin
from GDA_datatables.models import AnnotationRowModel


# Register your models here.

@admin.register(AnnotationRowModel)
class AnnotationRowModelAdmin(admin.ModelAdmin):
    list_display = ('symbol', 'entrezID', 'uniprotID', 'ensemblID', 'doid', 'source', 'diseaseName', 'doidSource')
