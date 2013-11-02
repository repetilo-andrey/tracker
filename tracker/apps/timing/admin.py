from django.contrib import admin

from .models import *


class TimePeriodAdminInline(admin.TabularInline):
    model = TimePeriod
    extra = max_num = 1
    readonly_fields = ('time_start', 'time_end', 'user')


class TicketAdmin(admin.ModelAdmin):
    inlines = [TimePeriodAdminInline, ]
    list_display = ('name', 'status',
                    'time_logged', 'date_closed')


class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'total_time', )


class DayStatisticAdmin(admin.ModelAdmin):
    list_display = ('user', 'day', 'day_time')


admin.site.register(DayStatistic, DayStatisticAdmin)
admin.site.register(Ticket, TicketAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(TimePeriod)


