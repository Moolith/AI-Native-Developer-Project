from django.shortcuts import redirect, render
from django.utils import timezone

from .forms import ChoreForm, HouseholdForm, PartnerForm
from .models import Chore, Household, Partner


def get_current_partner(request):
	partner_id = request.session.get('partner_id')
	if partner_id:
		return Partner.objects.filter(pk=partner_id).select_related('household').first()
	return None


def dashboard(request):
	partner = get_current_partner(request)
	if partner is None:
		return redirect('join')
	chores = partner.household.chores.select_related('assigned_to').all()
	return render(request, 'chores/dashboard.html', {
		'partner': partner,
		'household': partner.household,
		'chores': chores,
		'today': timezone.localdate(),
	})


def join(request):
	if request.method == 'POST':
		household_form = HouseholdForm(request.POST)
		partner_form = PartnerForm(request.POST)
		if household_form.is_valid() and partner_form.is_valid():
			household, _ = Household.objects.get_or_create(
				code=household_form.cleaned_data['code'],
				defaults={'name': household_form.cleaned_data['name'] or 'Our home'},
			)
			partner = Partner.objects.create(
				household=household,
				display_name=partner_form.cleaned_data['display_name'],
				avatar_color=partner_form.cleaned_data['avatar_color'],
			)
			request.session['partner_id'] = partner.pk
			return redirect('dashboard')
	else:
		household_form = HouseholdForm()
		partner_form = PartnerForm()
	return render(request, 'chores/join.html', {
		'household_form': household_form,
		'partner_form': partner_form,
	})


def create_chore(request):
	partner = get_current_partner(request)
	if partner is None:
		return redirect('join')
	form = ChoreForm(request.POST or None, household=partner.household)
	if request.method == 'POST' and form.is_valid():
		chore = form.save(commit=False)
		chore.household = partner.household
		chore.save()
		return redirect('dashboard')
	return render(request, 'chores/chore_form.html', {'form': form, 'partner': partner})
