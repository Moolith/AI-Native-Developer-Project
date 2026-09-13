from datetime import date, timedelta

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import Chore, Household, Partner


class HouseholdFlowTests(TestCase):
    def test_dashboard_redirects_without_a_partner_session(self):
        response = self.client.get(reverse('dashboard'))

        self.assertRedirects(response, reverse('join'))

    def test_join_uses_existing_household_and_stores_partner_session(self):
        household = Household.objects.create(code='HOME2028', name='Existing home')

        response = self.client.post(reverse('join'), {
            'code': household.code,
            'name': 'Ignored name',
            'display_name': 'Jordan',
            'avatar_color': '#e8755d',
        })

        self.assertRedirects(response, reverse('dashboard'))
        self.assertEqual(Household.objects.count(), 1)
        self.assertEqual(Partner.objects.get().household, household)
        self.assertEqual(self.client.session['partner_id'], Partner.objects.get().pk)

    def test_join_creates_household_and_partner_then_shows_dashboard(self):
        response = self.client.post(reverse('join'), {
            'code': 'HOME2026',
            'name': 'Our home',
            'display_name': 'Alex',
            'avatar_color': '#245c52',
        })

        self.assertRedirects(response, reverse('dashboard'))
        self.assertEqual(Household.objects.count(), 1)
        self.assertEqual(Partner.objects.get().display_name, 'Alex')

        response = self.client.get(reverse('dashboard'))
        self.assertContains(response, 'Our home')
        self.assertContains(response, 'Small things, done together.')

    def test_partner_can_add_a_chore_for_their_household(self):
        household = Household.objects.create(code='HOME2027')
        partner = Partner.objects.create(household=household, display_name='Sam')
        session = self.client.session
        session['partner_id'] = partner.pk
        session.save()

        response = self.client.post(reverse('create_chore'), {
            'title': 'Take out bins',
            'description': 'Before collection day',
            'frequency': Chore.Frequency.WEEKLY,
            'due_date': date.today() + timedelta(days=2),
            'effort': 4,
            'is_shared': '',
            'assigned_to': partner.pk,
        })

        self.assertRedirects(response, reverse('dashboard'))
        chore = Chore.objects.get()
        self.assertEqual(chore.household, household)
        self.assertEqual(chore.assigned_to, partner)

    def test_dashboard_shows_overdue_chore(self):
        household = Household.objects.create(code='HOME2029')
        partner = Partner.objects.create(household=household, display_name='Taylor')
        Chore.objects.create(
            household=household,
            title='Water plants',
            due_date=timezone.localdate() - timedelta(days=1),
            assigned_to=partner,
        )
        session = self.client.session
        session['partner_id'] = partner.pk
        session.save()

        response = self.client.get(reverse('dashboard'))

        self.assertContains(response, 'Water plants')
        self.assertContains(response, 'Overdue')


class ChoreModelTests(TestCase):
    def test_overdue_is_false_after_completion(self):
        household = Household.objects.create(code='HOME2030')
        chore = Chore.objects.create(
            household=household,
            title='Clean sink',
            due_date=timezone.localdate() - timedelta(days=1),
            completed_at=timezone.now(),
        )

        self.assertFalse(chore.is_overdue)

    def test_household_code_is_generated_in_expected_format(self):
        household = Household.objects.create()

        self.assertEqual(len(household.code), 8)
        self.assertTrue(household.code.isupper())


class ChoreFormTests(TestCase):
    def test_effort_must_be_between_one_and_ten(self):
        household = Household.objects.create(code='HOME2031')

        from .forms import ChoreForm

        for effort in (0, 11):
            form = ChoreForm(data={
                'title': 'Invalid effort',
                'frequency': Chore.Frequency.WEEKLY,
                'due_date': timezone.localdate(),
                'effort': effort,
            }, household=household)

            self.assertFalse(form.is_valid())
            self.assertIn('effort', form.errors)

    def test_assignment_choices_are_limited_to_household_partners(self):
        household = Household.objects.create(code='HOME2032')
        partner = Partner.objects.create(household=household, display_name='Casey')
        other_household = Household.objects.create(code='HOME2033')
        other_partner = Partner.objects.create(household=other_household, display_name='Morgan')

        from .forms import ChoreForm

        form = ChoreForm(household=household)

        self.assertQuerySetEqual(form.fields['assigned_to'].queryset, [partner], transform=lambda item: item)
        self.assertNotIn(other_partner, form.fields['assigned_to'].queryset)
