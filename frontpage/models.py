from django.db import models

# Create your models here.


class DoneSummary(models.Model):
	code = models.CharField(null=True, blank=True, max_length=50)
	ip = models.CharField(null=True, blank=True, max_length=50)
	timestamp = models.DateTimeField(auto_now_add=True)
	Price = models.CharField(null=True, blank=True, max_length=50)
	B_Lot = models.CharField(null=True, blank=True, max_length=50)
	S_Lot = models.CharField(null=True, blank=True, max_length=50)
	T_Lot = models.CharField(null=True, blank=True, max_length=50)
	B_Frq = models.CharField(null=True, blank=True, max_length=50)
	S_Frq = models.CharField(null=True, blank=True, max_length=50)
	T_Frq = models.CharField(null=True, blank=True, max_length=50)

	class Meta:
	    ordering = ['-timestamp']


		