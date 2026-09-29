from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import date, timedelta

from apps.accounts.models import User
from apps.patients.models import Patient
from apps.biomarkers.models import Biomarker
from apps.results.models import TestResult


class Command(BaseCommand):
    help = "Seed database with demo data: P001 patient with sample biomarker results"

    def handle(self, *args, **options):
        self.stdout.write("Starting seed...")

        # 1. Get or create admin user
        admin, created = User.objects.get_or_create(
            username="admin",
            defaults={
                "email": "admin@clinic.com",
                "first_name": "Admin",
                "last_name": "User",
                "role": "ADMIN",
                "is_staff": True,
                "is_superuser": True,
            },
        )
        if created:
            admin.set_password("admin123")
            admin.save()
            self.stdout.write(self.style.SUCCESS("✓ Created admin user (admin/admin123)"))
        else:
            self.stdout.write("✓ Admin user already exists")

        # 2. Get or create doctor user
        doctor, created = User.objects.get_or_create(
            username="dr.sharma",
            defaults={
                "email": "sharma@clinic.com",
                "first_name": "Anita",
                "last_name": "Sharma",
                "role": "DOCTOR",
            },
        )
        if created:
            doctor.set_password("doctor123")
            doctor.save()
            self.stdout.write(self.style.SUCCESS("✓ Created doctor user (dr.sharma/doctor123)"))
        else:
            self.stdout.write("✓ Doctor user already exists")

        # 3. Get or create biomarker
        biomarker, created = Biomarker.objects.get_or_create(
            code="BIO_A",
            defaults={
                "name": "Biomarker A",
                "unit": "mg/dL",
                "reference_min": 20,
                "reference_max": 40,
                "description": "Sample biomarker for demo",
                "is_active": True,
            },
        )
        if created:
            self.stdout.write(self.style.SUCCESS("✓ Created Biomarker A"))
        else:
            self.stdout.write("✓ Biomarker A already exists")

        # 4. Get or create patient
        patient, created = Patient.objects.get_or_create(
            patient_code="P001",
            defaults={
                "full_name": "Mr. XYZ",
                "date_of_birth": date(1972, 4, 10),
                "gender": "M",
                "medical_history": "Type 2 diabetes since 2018, hypertension",
                "is_active": True,
                "created_by": admin,
            },
        )
        if created:
            self.stdout.write(self.style.SUCCESS("✓ Created patient P001 (Mr. XYZ)"))
        else:
            self.stdout.write("✓ Patient P001 already exists")

        # 5. Create sample results: 42 → 38 → 31 → 25 over 4 weeks
        base_date = date(2026, 9, 1)
        sample_values = [
            (42, base_date),
            (38, base_date + timedelta(days=7)),
            (31, base_date + timedelta(days=14)),
            (25, base_date + timedelta(days=21)),
        ]

        created_count = 0
        for value, test_date in sample_values:
            result, created = TestResult.objects.get_or_create(
                patient=patient,
                biomarker=biomarker,
                test_date=test_date,
                defaults={
                    "value": value,
                    "unit": biomarker.unit,
                    "notes": f"Sample result {value} on {test_date}",
                    "recorded_by": doctor,
                },
            )
            if created:
                created_count += 1

        self.stdout.write(self.style.SUCCESS(f"✓ Created {created_count} sample results"))

        self.stdout.write(
            self.style.SUCCESS(
                "\nSeed complete!\n"
                "Login credentials:\n"
                "  Admin:  admin / admin123\n"
                "  Doctor: dr.sharma / doctor123\n"
                "Demo data:\n"
                "  Patient: P001 (Mr. XYZ)\n"
                "  Biomarker: Biomarker A (42 → 38 → 31 → 25)\n"
            )
        )