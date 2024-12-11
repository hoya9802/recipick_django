import base64
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


# Gmail API 인증 및 서비스 생성
def get_gmail():
    try:
        creds = Credentials.from_authorized_user_file(
            'user/secrets/token.json',
            ['https://www.googleapis.com/auth/gmail.send']
        )
        service = build('gmail', 'v1', credentials=creds)
        return service
    except Exception as e:
        print(f"Error initializing Gmail service: {e}")
        raise


def send_email(to_email, subject, body):
    try:
        service = get_gmail()

        message = {
            'raw': base64.urlsafe_b64encode(
                f"To: {to_email}\nSubject: {subject}\n\n{body}".encode("utf-8")
            ).decode("utf-8")
        }

        # Gmail API를 사용하여 이메일 전송
        service.users().messages().send(userId="me", body=message).execute()
        print(f"Email sent to {to_email}")
    except HttpError as error:
        print(f"An error occurred while sending email: {error}")
        raise
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        raise
