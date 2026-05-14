from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from .models import Incident, Category, SystemLog, Feedback, Notification, IncidentImage
from accounts.models import User
from django.urls import reverse_lazy
from django.db.models import Q
from django.contrib import messages
from .forms import IncidentForm



class HomeView(View):
    def get(self, request):
        return render(request, 'incidents/home.html')

class DashboardView(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        queryset = Incident.objects.all()
        
        
        if user.role == 'CITIZEN':
            queryset = queryset.filter(citizen=user)
        elif user.role == 'OPERATOR' and user.region:
            queryset = queryset.filter(region=user.region)
        elif user.role == 'TECHNICIAN':
            queryset = queryset.filter(technician=user)
        
        # Search/Filter
        status = request.GET.get('status')
        category_id = request.GET.get('category')
        region = request.GET.get('region')
        date = request.GET.get('date')
        if status:
            queryset = queryset.filter(status=status)
        if category_id:
            queryset = queryset.filter(category_id=category_id)
        if region:
            queryset = queryset.filter(region=region)
        if date:
            queryset = queryset.filter(created_at__date=date)
            
        incidents = queryset.order_by('-created_at')
        categories = Category.objects.all()
        regions = Incident._meta.get_field('region').choices
        
        # Calculate counts
        total_count = incidents.count()
        in_progress_count = incidents.filter(status='IN_PROGRESS').count()
        reopened_count = incidents.filter(status='REOPENED').count()
        resolved_count = incidents.filter(status='RESOLVED').count()
        closed_count = incidents.filter(status='CLOSED').count()
        rejected_count = incidents.filter(status='REJECTED').count()
        
        context = {
            'incidents': incidents,
            'categories': categories,
            'regions': regions,
            'total_count': total_count,
            'in_progress_count': in_progress_count,
            'reopened_count': reopened_count,
            'resolved_count': resolved_count,
            'closed_count': closed_count,
            'rejected_count': rejected_count,
        }
        
        if user.role == 'OPERATOR':
            context['technicians'] = User.objects.filter(role='TECHNICIAN')
            
        return render(request, 'incidents/dashboard.html', context)


class IncidentCreateView(LoginRequiredMixin, View):
    def get(self, request):
        form = IncidentForm()
        return render(request, 'incidents/incident_form.html', {'form': form})

    def post(self, request):
        form = IncidentForm(request.POST, request.FILES)
        if form.is_valid():
            incident = form.save(commit=False)
            incident.citizen = request.user
            incident.region = request.user.region
            incident.city = request.user.city
            incident.save()
            
           
            images = request.FILES.getlist('images')
            for img in images:
                IncidentImage.objects.create(incident=incident, image=img)
                
       
            operators = User.objects.filter(role='OPERATOR')
            if incident.region:
                operators = operators.filter(region=incident.region)
            for op in operators:
                Notification.objects.create(user=op, message=f"Yangi muammo yaratildi: {incident.title}")
                
            return redirect('dashboard')
        return render(request, 'incidents/incident_form.html', {'form': form})

class IncidentUpdateView(LoginRequiredMixin, UserPassesTestMixin, View):
    def test_func(self):
        incident = get_object_or_404(Incident, pk=self.kwargs['pk'])
        return incident.citizen == self.request.user and incident.status == 'NEW'

    def get(self, request, pk):
        incident = get_object_or_404(Incident, pk=pk)
        form = IncidentForm(instance=incident)
        return render(request, 'incidents/incident_form.html', {'form': form, 'incident': incident})

    def post(self, request, pk):
        incident = get_object_or_404(Incident, pk=pk)
        form = IncidentForm(request.POST, request.FILES, instance=incident)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
        return render(request, 'incidents/incident_form.html', {'form': form, 'incident': incident})

class IncidentDeleteView(LoginRequiredMixin, UserPassesTestMixin, View):
    def test_func(self):
        incident = get_object_or_404(Incident, pk=self.kwargs['pk'])
        return incident.citizen == self.request.user and incident.status == 'NEW'

    def get(self, request, pk):
        incident = get_object_or_404(Incident, pk=pk)
        return render(request, 'incidents/incident_confirm_delete.html', {'incident': incident})

    def post(self, request, pk):
        incident = get_object_or_404(Incident, pk=pk)
        incident.delete()
        return redirect('dashboard')

class IncidentDetailView(LoginRequiredMixin, View):
    def get(self, request, pk):
        incident = get_object_or_404(Incident, pk=pk)
        context = {'incident': incident}
        if request.user.role == 'OPERATOR':
            context['technicians'] = User.objects.filter(role='TECHNICIAN')
        return render(request, 'incidents/incident_detail.html', context)

@login_required
def update_status(request, pk):
    incident = get_object_or_404(Incident, pk=pk)
    user = request.user
    
    if request.method == 'POST':
        action = request.POST.get('action')
        uz_action = "Amal bajarildi"
        
        if user.role == 'OPERATOR':
            if action == 'REJECT':
                incident.status = 'REJECTED'
                uz_action = "Rad etildi"
                Notification.objects.create(user=incident.citizen, message=f"Sizning muammongiz rad etildi: {incident.title}")
            elif action == 'ASSIGN':
                tech_id = request.POST.get('technician')
                if tech_id:
                    tech = User.objects.get(id=tech_id)
                    if tech.category == incident.category:
                        incident.technician = tech
                        incident.status = 'IN_PROGRESS'
                        uz_action = f"Texnikka biriktirildi: {tech.username}"
                        Notification.objects.create(user=tech, message=f"Sizga yangi ish biriktirildi: {incident.title}")

        elif user.role == 'TECHNICIAN' and incident.technician == user:
            if action == 'RESOLVE' and incident.status in ['IN_PROGRESS', 'REOPENED']:
                incident.status = 'RESOLVED'
                incident.result_comment = request.POST.get('result_comment')
                if 'result_photo' in request.FILES:
                    incident.result_photo = request.FILES['result_photo']
                uz_action = "Bajarilgan deb belgilandi (hisobot bilan)"
                Notification.objects.create(user=incident.citizen, message=f"Muammo hal etildi: {incident.title}. Iltimos, tekshiring va baho bering.")

        elif user.role == 'CITIZEN' and incident.citizen == user:
            if action == 'CLOSE' and incident.status == 'RESOLVED':
                try:
                    rating = int(request.POST.get('rating', 5))
                except (ValueError, TypeError):
                    rating = 5
                comment = request.POST.get('comment', '')
                Feedback.objects.create(incident=incident, rating=rating, comment=comment)
                
                if rating <= 2:
                    incident.status = 'REOPENED'
                    incident.priority = 'HIGH'
                    uz_action = f"Past baho ({rating}) berildi. Muammo qayta ochildi."
                    operators = User.objects.filter(role='OPERATOR')
                    for op in operators:
                        Notification.objects.create(user=op, message=f"Past baho! Muammo qayta ochildi: {incident.title}")
                else:
                    incident.status = 'CLOSED'
                    uz_action = "Yopildi va baholandi"
        
        incident.save()
        SystemLog.objects.create(incident=incident, user=user, action=uz_action)
        
    return redirect('incident_detail', pk=pk)

@login_required
def mark_notifications_read(request):
    request.user.notifications.filter(is_read=False).update(is_read=True)
    return redirect(request.META.get('HTTP_REFERER', 'dashboard'))

class NotificationListView(LoginRequiredMixin, View):
    def get(self, request):
        notifications = request.user.notifications.all().order_by('-created_at')
        return render(request, 'incidents/notifications.html', {'notifications': notifications})
