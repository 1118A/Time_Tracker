from django.db import models
from django.utils import timezone
from datetime import timedelta

class Employee(models.Model):
    name = models.CharField(max_length=150, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class TimeLog(models.Model):
    employee = models.ForeignKey(Employee, related_name="time_logs", on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)
    clock_in = models.DateTimeField(null=True, blank=True)
    clock_out = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.employee.name} - {self.date}"

    @property
    def total_work_duration(self):
        if self.clock_in and self.clock_out:
            return self.clock_out - self.clock_in
        elif self.clock_in:
            return timezone.now() - self.clock_in
        return timedelta()

    @property
    def total_break_duration(self):
        total = timedelta()
        for b in self.breaks.all():
            if b.start_time and b.end_time:
                total += (b.end_time - b.start_time)
            elif b.start_time:
                total += (timezone.now() - b.start_time)
        return total

    @property
    def net_duration(self):
        return max(timedelta(), self.total_work_duration - self.total_break_duration)

class BreakLog(models.Model):
    time_log = models.ForeignKey(TimeLog, related_name="breaks", on_delete=models.CASCADE)
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Break for {self.time_log} at {self.start_time}"
