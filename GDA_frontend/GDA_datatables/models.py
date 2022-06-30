from django.db import models


# Create your models here.
class AnnotationRowModel(models.Model):
    symbol = models.CharField('symbol', max_length=30, default='None')
    entrezID = models.CharField('entrezID', max_length=50, default='None')
    uniprotID = models.CharField('uniprotID', max_length=50, default='None')
    ensemblID = models.CharField('ensemblID', max_length=50, default='None')
    doid = models.CharField('doid', max_length=30, default='None')
    source = models.CharField('source', max_length=30, default='None')
    diseaseName = models.TextField('diseaseName', default='None')
    jaccardIndex = models.CharField('jaccardIndex', max_length=10, default='None')

    class Meta:
        unique_together = ['symbol', 'entrezID', 'uniprotID', 'ensemblID', 'doid', 'source', 'diseaseName',
                           'jaccardIndex']

    def __str__(self):
        return str(self.symbol) + '\t' + \
               str(self.entrezID) + '\t' + \
               str(self.uniprotID) + '\t' + \
               str(self.ensemblID) + '\t' + \
               str(self.doid) + '\t' + \
               str(self.source) + '\t' + \
               str(self.diseaseName) + '\t' + \
               str(self.jaccardIndex) + '%' if self.jaccardIndex == "None" else str(self.jaccardIndex)
