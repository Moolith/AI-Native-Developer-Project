# Together: Household Chores

A Django server-rendered prototype for managing shared household chores.

## Local setup

From the project directory:

```powershell
cd "C:\Users\HP Zbook\Desktop\Prova github copilot\AI-Native Developer Project"
.\.venv\Scripts\Activate.ps1
python manage.py migrate
```

If PowerShell blocks activation, run this once in the current terminal:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
```

## Run the app

```powershell
python manage.py runserver
```

Open http://127.0.0.1:8000/.

The dashboard currently supports household entry, browser-backed partner identity, and chore creation.

## Run checks and tests

```powershell
python manage.py check
python manage.py makemigrations --check --dry-run
python manage.py test
```

The current suite covers 9 scenarios across onboarding, dashboard access, chore creation, effort validation, household-scoped assignment choices, overdue display, completion state, and generated household codes.

## Development status

Implemented: Django project setup, SQLite, household/partner/chore models, initial migrations, responsive templates, Django admin registration, and the first automated test slice.

Not implemented yet: partner approval, the two-partner limit, generated invite-code workflow, completion actions, recurring occurrence generation, effort balancing, swaps, reminders/push notifications, rewards/history, household deletion approval, and offline synchronization. See [backlog.md](backlog.md).

## Deployment note

This configuration is intentionally local-development-only. `DEBUG` is enabled, the secret key is a development key, `ALLOWED_HOSTS` is empty, and secure-cookie/HTTPS settings are not configured. Do not deploy it without a production settings layer and a real secret key.
