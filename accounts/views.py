
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .forms import CVUploadForm
from .utils import extract_text_from_cv, extract_skills_from_cv
from .matching import calculate_job_matches
from .email_service import send_cv_to_company


@login_required
def upload_cv(request):
    candidate = request.user.candidate_profile

    if request.method == 'POST':
        form = CVUploadForm(request.POST, request.FILES)

        if form.is_valid():
            cv = form.save(commit=False)
            cv.candidate = candidate
            cv.save()

            try:
                cv.file.open('rb')
                cv.extracted_text = extract_text_from_cv(cv.file)
                cv.file.close()

                skills = extract_skills_from_cv(cv.extracted_text)

                candidate.skills = ', '.join(skills)
                candidate.save(update_fields=['skills'])

                cv.save(update_fields=['extracted_text'])

                matches = calculate_job_matches(candidate)

                for match in matches:
                    if match.delivery_status == 'pending':
                        send_cv_to_company(match, cv)

                messages.success(
                    request,
                    f'CV-ja u analizua me sukses! '
                    f'Aftesite e identifikuara: {", ".join(skills) if skills else "Asnje."} '
                    f'U gjeten {len(matches)} perputhje me vendet e punes.'
                )

            except Exception:
                if cv.file:
                    cv.file.close()

                messages.warning(
                    request,
                    'CV-ja u ngarkua, por analiza nuk mundi te perfundonte.'
                )

            return redirect('upload_cv')

    else:
        form = CVUploadForm()

    return render(
        request,
        'accounts/upload_cv.html',
        {'form': form}
    )
