
import os
import base64
import mimetypes
from pathlib import Path

import requests

from django.utils import timezone


def send_cv_to_company(job_match, cv):
    api_key = os.getenv('BREVO_API_KEY')
    sender_email = os.getenv('BREVO_SENDER_EMAIL')
    sender_name = os.getenv(
        'BREVO_SENDER_NAME',
        'CV AI System'
    )

    company = job_match.job.company
    recipient_email = company.user.email

    if not api_key or not sender_email or not recipient_email:
        print("BREVO ERROR: Mungon API Key ose adresa e emailit.")

        job_match.delivery_status = 'failed'
        job_match.save(update_fields=['delivery_status'])
        return False

    try:
        file_path = Path(cv.file.name)
        file_name = file_path.name

        mime_type, _ = mimetypes.guess_type(file_name)

        with cv.file.open('rb') as file:
            file_content = file.read()

        encoded_file = base64.b64encode(
            file_content
        ).decode('utf-8')

        payload = {
            'sender': {
                'name': sender_name,
                'email': sender_email,
            },
            'to': [
                {
                    'email': recipient_email,
                    'name': company.company_name,
                }
            ],
            'subject': (
                f"CV e re per poziten: {job_match.job.title}"
            ),
            'textContent': (
                f"Pershendetje {company.company_name},\n\n"
                f"Ju keni pranuar nje CV te re per poziten "
                f"{job_match.job.title}.\n\n"
                f"Kandidati: {job_match.candidate.full_name}\n"
                f"Perputhja: {job_match.match_percentage}%\n"
                f"Aftesite e perbashketa: "
                f"{', '.join(job_match.matched_skills)}\n\n"
                f"CV-ja eshte bashkengjitur ne kete email.\n\n"
                f"CV AI System"
            ),
            'attachment': [
                {
                    'name': file_name,
                    'content': encoded_file,
                }
            ],
        }

        if mime_type:
            payload['attachment'][0]['contentType'] = mime_type

        response = requests.post(
            'https://api.brevo.com/v3/smtp/email',
            headers={
                'accept': 'application/json',
                'api-key': api_key,
                'content-type': 'application/json',
            },
            json=payload,
            timeout=30,
        )

        response.raise_for_status()

        job_match.delivery_status = 'sent'
        job_match.sent_at = timezone.now()
        job_match.save(
            update_fields=['delivery_status', 'sent_at']
        )

        print("BREVO SUCCESS:", response.status_code)

        return True

    except requests.RequestException as error:
        print("BREVO ERROR:", error)

        if error.response is not None:
            print("BREVO RESPONSE:", error.response.text)

        job_match.delivery_status = 'failed'
        job_match.save(update_fields=['delivery_status'])
        return False

    except Exception as error:
        print("EMAIL ERROR:", error)

        job_match.delivery_status = 'failed'
        job_match.save(update_fields=['delivery_status'])
        return False
