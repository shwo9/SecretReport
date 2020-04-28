from django.contrib import admin

from helpline.models import Report, Author, Organization, ReportFile, Log

admin.site.register(Organization)
admin.site.register(Author)
admin.site.register(Report)
admin.site.register(ReportFile)
admin.site.register(Log)
