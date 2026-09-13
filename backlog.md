# Together Django Backlog

## MVP

### 1. Complete household onboarding
- Add partner approval for joining a household.
- Enforce the two-partner household limit.
- Preserve browser-backed identity and allow recovery with the household code.
- Add tests for valid joins, duplicate names, rejected joins, and full households.

### 2. Add chore lifecycle actions
- Add complete and undo actions to the dashboard.
- Credit shared chores to the partner who completes them.
- Allow either partner to edit or delete chores.
- Add tests for completion, undo, edit, and delete permissions.

### 3. Implement recurring chores
- Generate the next occurrence for daily, weekly, monthly, and custom schedules.
- Store completion history without losing the recurring chore definition.
- Add tests for due dates, next occurrences, and overdue status.

### 4. Build effort-balanced assignments
- Calculate each partner's assigned effort for the current period.
- Suggest assignments that minimize the effort difference.
- Recalculate suggestions when chores or effort estimates change.
- Keep manual assignment changes intact until the next balancing run.

### 5. Add swaps and shared chores
- Let either partner propose a chore swap.
- Require the other partner to approve or reject the swap.
- Show pending swap requests in the dashboard.
- Add tests for approval, rejection, and stale requests.

### 6. Add reminders and overdue notifications
- Add household timezone configuration.
- Mark incomplete chores past their due date as overdue.
- Add in-app reminders and browser push notifications when permission is available.
- Fall back to in-app reminders when browser permission is denied.

### 7. Add rewards and history
- Record completion, on-time completion, and streak events.
- Calculate points and display each partner's progress to both partners.
- Add fixed and custom badges or milestones.
- Add weekly and monthly history views.

### 8. Add household safety controls
- Require both partners to approve household deletion.
- Add confirmation screens and an audit record before deletion.
- Add tests covering cancellation and final approval.

### 9. Add offline support
- Cache the dashboard and chore actions for offline use.
- Queue local changes for synchronization when connectivity returns.
- Detect conflicts and let the user choose which update to keep.
- Add browser-level tests for offline completion and conflict resolution.

### 10. Finish product validation
- Add responsive layout tests for desktop and mobile browsers.
- Verify Django admin support for households, partners, chores, and history.
- Add deployment documentation after the local MVP is stable.
- Run `manage.py check`, migrations, the full test suite, and a manual end-to-end workflow.

## Out of Scope for MVP

- Email/password authentication
- Email notifications
- Native mobile applications
- Cloud deployment
- Third-party integrations
- Child accounts
- Multiple households per account
- Advanced analytics
