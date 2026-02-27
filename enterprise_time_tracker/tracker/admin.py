from django.contrib import admin
from .models import Employee, TimeLog, BreakLog

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    search_fields = ('name',)

class BreakLogInline(admin.TabularInline):
    model = BreakLog
    extra = 0

@admin.register(TimeLog)
class TimeLogAdmin(admin.ModelAdmin):
    list_display = ('employee', 'date', 'clock_in', 'clock_out')
    list_filter = ('date', 'employee')
    inlines = [BreakLogInline]
