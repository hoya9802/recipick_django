from google_auth_oauthlib.flow import InstalledAppFlow
import os

# 인증에 필요한 스코프 설정
SCOPES = ['https://www.googleapis.com/auth/gmail.send']

# credentials.json 파일 위치
CREDENTIALS_FILE = 'recipick_app/user/secrets/credentials.json'


def generate_token():
    """
    credentials.json을 사용하여 OAuth 인증을 진행하고 token.json 파일을 생성합니다.
    """
    flow = InstalledAppFlow.from_client_secrets_file(
        CREDENTIALS_FILE, SCOPES
    )
    # access_type='offline'을 명시적으로 추가
    creds = flow.run_local_server(
        port=8080,
        redirect_uri_trailing_slash=True,  # 슬래시(/) 끝나는 URI 사용
        access_type='offline',
        prompt='consent'
    )

    # token.json 파일로 저장
    token_path = 'recipick_app/user/secrets/token.json'
    with open(token_path, 'w') as token:
        token.write(creds.to_json())
    print(f"token.json 파일이 {token_path}에 성공적으로 생성되었습니다!")


if __name__ == '__main__':
    if not os.path.exists(CREDENTIALS_FILE):
        print(f"'{CREDENTIALS_FILE}' 파일을 찾을 수 없습니다. 파일 경로를 확인하세요.")
    else:
        generate_token()
