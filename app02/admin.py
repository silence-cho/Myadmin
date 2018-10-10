# Register your models here.


from myAdmin.service.site import site
from app02 import models

site.register(models.Course)
site.register(models.Student)
