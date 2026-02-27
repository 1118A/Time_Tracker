import csv
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.http import HttpResponse, HttpResponseBadRequest
from django.contrib import messages
from .models import Employee, TimeLog, BreakLog
from datetime import timedelta

def dashboard(request):
    today = timezone.localdate()
    employee_name = request.GET.get('employee_name', '').strip()
    
    context = {
        'employee_name': employee_name,
        'today_log': None,
        'recent_logs': [],
        'today_total': timedelta(),
    }
    
    if employee_name:
        employee, created = Employee.objects.get_or_create(name=employee_name)
        
        # Get today's log
        today_log, log_created = TimeLog.objects.get_or_create(
            employee=employee,
            date=today
        )
        context['today_log'] = today_log
        
        # Get recent logs
        context['recent_logs'] = TimeLog.objects.filter(employee=employee).order_by('-date')[:30]
        
        # Calculate today's total
        context['today_total'] = today_log.net_duration
        
        # Calculate UI states
        context['can_clock_in'] = "" if not today_log.clock_in else "disabled"
        context['can_clock_out'] = "" if bool(today_log.clock_in and not today_log.clock_out) else "disabled"
        has_active_break = today_log.breaks.filter(end_time__isnull=True).exists()
        context['can_start_break'] = "" if bool(today_log.clock_in and not today_log.clock_out and not has_active_break) else "disabled"
        context['can_end_break'] = "" if bool(has_active_break) else "disabled"
        
    return render(request, 'tracker/dashboard.html', context)

def action(request):
    if request.method != 'POST':
        return HttpResponseBadRequest("Invalid request method.")
        
    action_type = request.POST.get('action')
    employee_name = request.POST.get('employee_name', '').strip()
    
    if not employee_name:
        messages.error(request, "Employee name is required.")
        return redirect('tracker:dashboard')
        
    employee, _ = Employee.objects.get_or_create(name=employee_name)
    today = timezone.localdate()
    log, _ = TimeLog.objects.get_or_create(employee=employee, date=today)
    
    now = timezone.now()
    
    try:
        if action_type == 'clock_in':
            if log.clock_in:
                messages.warning(request, "Already clocked in.")
            else:
                log.clock_in = now
                log.save()
                messages.success(request, "Successfully clocked in.")
                
        elif action_type == 'clock_out':
            if not log.clock_in:
                messages.error(request, "Cannot clock out. You haven't clocked in.")
            elif log.clock_out:
                messages.warning(request, "Already clocked out.")
            else:
                # Close any active breaks
                active_break = log.breaks.filter(end_time__isnull=True).first()
                if active_break:
                    active_break.end_time = now
                    active_break.save()
                    
                log.clock_out = now
                log.save()
                messages.success(request, "Successfully clocked out.")
                
        elif action_type == 'break_start':
            if not log.clock_in:
                messages.error(request, "Cannot start break. You haven't clocked in.")
            elif log.clock_out:
                messages.error(request, "Cannot start break. You are already clocked out.")
            elif log.breaks.filter(end_time__isnull=True).exists():
                messages.warning(request, "A break is already in progress.")
            else:
                BreakLog.objects.create(time_log=log, start_time=now)
                messages.success(request, "Break started.")
                
        elif action_type == 'break_end':
            active_break = log.breaks.filter(end_time__isnull=True).first()
            if not active_break:
                messages.error(request, "No active break to end.")
            else:
                active_break.end_time = now
                active_break.save()
                messages.success(request, "Break ended.")
        else:
            messages.error(request, "Unknown action.")
            
    except Exception as e:
        messages.error(request, f"An error occurred: {str(e)}")
        
    return redirect(f"/?employee_name={employee_name}")

def export_csv(request):
    employee_name = request.GET.get('employee_name', '').strip()
    
    response = HttpResponse(
        content_type='text/csv',
        headers={'Content-Disposition': 'attachment; filename="time_logs.csv"'},
    )

    writer = csv.writer(response)
    writer.writerow(['Date', 'Employee', 'Clock In', 'Clock Out', 'Total Work Duration', 'Total Break Duration', 'Net Duration'])
    
    logs = TimeLog.objects.all().order_by('-date', 'employee__name')
    if employee_name:
        logs = logs.filter(employee__name=employee_name)

    for log in logs:
        writer.writerow([
            log.date,
            log.employee.name,
            log.clock_in.strftime('%Y-%m-%d %H:%M:%S') if log.clock_in else 'N/A',
            log.clock_out.strftime('%Y-%m-%d %H:%M:%S') if log.clock_out else 'N/A',
            str(log.total_work_duration).split('.')[0],
            str(log.total_break_duration).split('.')[0],
            str(log.net_duration).split('.')[0],
        ])

    return response
