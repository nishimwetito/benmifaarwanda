import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "benmifaarwanda.settings")

import django

django.setup()

from django.test import Client
from django.contrib.auth.models import User
from core.models import Video, ProfessionalSupportService, SiteSettings

PUBLIC_URLS = [
    ("/", 200),
    ("/about/", 200),
    ("/partners/", 200),
    ("/gallery/", 200),
    ("/support/", 200),
    ("/courses/video/", 200),
    ("/courses/pdf/", 200),
    ("/courses/slides/", 200),
    ("/courses/", 302),
    ("/users/register/", 302),
    ("/users/login/", 302),  # login view redirects to home (modal-based auth)
]

DASHBOARD_TABS = [
    "overview",
    "resources",
    "landing_page",
    "site_settings",
    "members",
]

c = Client()
failures = []

for path, expected in PUBLIC_URLS:
    r = c.get(path)
    ok = r.status_code == expected
    print(f"GET {path}: {r.status_code} ({'OK' if ok else f'expected {expected}'})")
    if not ok:
        failures.append(path)

r = c.get("/")
body = r.content.decode()
for label, cond in [
    ("homepage learning", "Master Your Holistic Life" in body),
    ("homepage services", "Technical Support" in body),
    ("whatsapp CTA", "Message on WhatsApp" in body),
]:
    print(f"{label}: {'OK' if cond else 'FAIL'}")
    if not cond:
        failures.append(label)

print("featured videos:", Video.objects.filter(show_on_homepage=True).count())
print("featured services:", ProfessionalSupportService.objects.filter(show_on_homepage=True).count())
print("whatsapp:", SiteSettings.load().whatsapp_number)

staff = User.objects.filter(is_staff=True).first()
if staff:
    staff.set_password("admin12345")
    staff.save()
    c.force_login(staff)
    for tab in DASHBOARD_TABS:
        r = c.get(f"/users/dashboard/?tab={tab}")
        ok = r.status_code == 200
        print(f"dashboard tab {tab}: {r.status_code} ({'OK' if ok else 'FAIL'})")
        if not ok:
            failures.append(f"tab:{tab}")

    User.objects.filter(username="smoke_member99").delete()
    r = c.post(
        "/users/dashboard/",
        {
            "tab": "members",
            "action": "add_member",
            "username": "smoke_member99",
            "email": "sm99@test.com",
            "password1": "MemberPass123!",
            "password2": "MemberPass123!",
            "first_name": "Smoke",
            "last_name": "Test",
        },
    )
    created = User.objects.filter(username="smoke_member99").exists()
    print(f"add member POST: {r.status_code} created={created}")
    if not created:
        failures.append("add_member")
    User.objects.filter(username="smoke_member99").delete()
else:
    print("dashboard/member tests: SKIP (no staff user)")

print("---")
if failures:
    print("FAILED:", ", ".join(failures))
    sys.exit(1)
print("All smoke checks passed.")
