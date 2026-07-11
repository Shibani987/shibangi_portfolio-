from datetime import date

from django.db import migrations


EDUCATIONS = [
    {
        "degree_name": "Secondary School Certificate",
        "institution_name": "Kalyani Central Model School",
        "university_board": "CBSE",
        "end_date": date(2020, 1, 1),
        "current_status": "completed",
        "cgpa_percentage": "70%",
        "order": 1,
    },
    {
        "degree_name": "Higher Secondary Certificate",
        "institution_name": "Private candidate",
        "university_board": "CBSE",
        "end_date": date(2023, 1, 1),
        "current_status": "completed",
        "cgpa_percentage": "66%",
        "order": 2,
    },
    {
        "degree_name": "Bachelors in Computer Applications",
        "institution_name": "JIS College Of Engineering",
        "start_date": date(2023, 1, 1),
        "end_date": date(2026, 1, 1),
        "current_status": "ongoing",
        "is_ongoing": True,
        "order": 3,
    },
    {
        "degree_name": "English Honours (IGNOU)",
        "institution_name": "Distance Learning",
        "start_date": date(2024, 1, 1),
        "end_date": date(2028, 1, 1),
        "current_status": "ongoing",
        "is_ongoing": True,
        "order": 4,
    },
]


EXPERIENCES = [
    {
        "job_title": "Management Intern",
        "company_name": "JIS College Of Engineering",
        "employment_type": "internship",
        "experience_summary": "6 Months",
        "order": 1,
    },
    {
        "job_title": "Drawing Tutor",
        "company_name": "Freelance / Private",
        "employment_type": "freelance",
        "start_date": date(2020, 1, 1),
        "currently_working": True,
        "order": 2,
    },
]


def seed_resume_entries(apps, schema_editor):
    Education = apps.get_model("portfolio_app", "Education")
    Experience = apps.get_model("portfolio_app", "Experience")

    for data in EDUCATIONS:
        Education.objects.update_or_create(
            degree_name=data["degree_name"],
            institution_name=data["institution_name"],
            defaults={**data, "is_published": True},
        )

    for data in EXPERIENCES:
        Experience.objects.update_or_create(
            job_title=data["job_title"],
            company_name=data["company_name"],
            defaults={**data, "is_published": True},
        )


class Migration(migrations.Migration):

    dependencies = [
        ("portfolio_app", "0014_education_experience"),
    ]

    operations = [
        migrations.RunPython(seed_resume_entries, migrations.RunPython.noop),
    ]
