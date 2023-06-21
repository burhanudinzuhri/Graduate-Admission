from django.db import models

# Create your models here.
class MyData(models.Model):
    id=models.AutoField(primary_key=True)
    TOFEL=models.IntegerField()
    GRE=models.IntegerField()
    UNI_rating=models.IntegerField()
    SOP=models.FloatField()
    LOR=models.FloatField()
    CGPA=models.FloatField()
    Research_Ex=models.BooleanField()
    Chance_of_Admit=models.FloatField(max_length=4, null=True)