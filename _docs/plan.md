# Together: Shared Household Chores

## MVP Scope

Together is a Django server-rendered responsive web app for exactly two partners sharing one household.

### Core workflow

- Join or create a household with a permanent automatically generated code.
- Choose a display name and avatar color.
- Create custom one-time or recurring chores with custom schedules, due dates, and effort scores from 1 to 10.
- Suggest weekly assignments based on total effort, with manual adjustments.
- Support shared chores and swaps requiring both partners' approval.
- Mark chores complete, show overdue work, and notify both partners.
- Show weekly/monthly history, points, streaks, badges, and custom milestones.
- Support browser push notifications with in-app fallback.
- Work offline and let users resolve sync conflicts.

### Permissions and rules

- Either partner can edit or delete chores.
- Either partner can undo the other partner's completion.
- Shared completion is credited to whoever marks it complete.
- Household deletion requires both partners' approval.
- The household chooses the timezone used for due dates and reminders.
- Partner progress is visible to both partners.

### Technology and delivery

- Django templates and forms; no separate frontend or API in the MVP.
- SQLite and local development first.
- Django admin for development and troubleshooting.
- Support modern desktop and mobile browsers.

### Out of scope

Email/password authentication, email notifications, native mobile apps, cloud deployment, integrations, child accounts, multiple households, and advanced analytics.

## Implementation Status

### Complete

- Django project and SQLite database.
- Household, partner, and chore models.
- Household join flow with browser-backed session identity.
- Responsive dashboard and chore creation form.
- Django admin registration.
- Initial migrations and automated request tests.
- Effort values validated from 1 through 10.
- Migration consistency checked after model changes.

### Next slices

1. Partner approval and exactly-two-partner enforcement.
2. Chore completion, undo, overdue state, and notification fallback.
3. Recurrence generation and effort-balanced assignment suggestions.
4. Swaps, rewards, history, custom milestones, and offline sync.

## Audit Notes

Last checked during development:

- `python manage.py check` passes with no issues.
- `python manage.py test` passes with 9 tests.
- `python manage.py makemigrations --check --dry-run` reports no pending migrations.
- `python manage.py check --deploy` reports 7 warnings because this is local-only configuration: development secret key, `DEBUG=True`, empty `ALLOWED_HOSTS`, and missing HTTPS/security-cookie settings.

Known functional gaps are tracked in [backlog.md](../backlog.md). In particular, onboarding currently accepts a user-supplied code, does not yet enforce exactly two partners, and does not yet implement approval or duplicate-name handling.
