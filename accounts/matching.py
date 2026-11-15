from .models import Job, JobMatch


def calculate_job_matches(candidate):
    candidate_skills = {
        skill.strip().lower()
        for skill in candidate.skills.split(',')
        if skill.strip()
    }

    active_jobs = Job.objects.filter(is_active=True)

    matches = []

    for job in active_jobs:
        required_skills = {
            requirement.skill_name.strip().lower()
            for requirement in job.requirements.all()
            if requirement.skill_name.strip()
        }

        if not required_skills:
            continue

        matched_skills = candidate_skills.intersection(
            required_skills
        )

        if not matched_skills:
            continue

        match_percentage = (
            len(matched_skills) / len(required_skills)
        ) * 100

        job_match, created = JobMatch.objects.update_or_create(
            candidate=candidate,
            job=job,
            defaults={
                'match_percentage': round(match_percentage, 2),
                'matched_skills': sorted(matched_skills),
            }
        )

        matches.append(job_match)

    return matches