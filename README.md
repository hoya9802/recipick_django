# 🍽️ Recipick - 레시피 공유 플랫폼 🍽️
![image](https://github.com/user-attachments/assets/5ff0bf6d-a23c-4959-98cc-afaddf5dd735)
### 🧑‍🍳 다양한 요리를 해보며 맛있게 살자!

 **Recipick**은 1인 가구의 요리 고민을 해결해주는 종합 플랫폼입니다!
 
---

## 프로젝트 소개

### 🛠️ Architecture
![Screenshot 2024-12-16 121513](https://github.com/user-attachments/assets/39fae645-8b29-4380-8892-50069a405dde)
<br><br/>

### 🔎 ERD
![image](https://github.com/user-attachments/assets/42ba3db3-7c21-4ce2-9b15-e9ebfcc406fb)
<br><br/>


## 개발 방법론
### Test-Driven Development (TDD)
우리는 TDD를 통해 개발을 진행했습니다. TDD는 테스트를 먼저 작성하고, 그 테스트를 통과하는 코드를 작성하는 방식으로, 코드의 안정성과 신뢰성을 높이는 데 큰 도움이 되었습니다.

### Lint 도구
코드의 일관성과 스타일을 유지하기 위해 Flake8을 사용했습니다. Flake8은 코드의 잠재적인 오류를 사전에 발견하고, 코드 스타일 가이드를 준수하도록 도와줍니다.

<br>

## 팀원 구성
|이은택|김혜지|
|---|---|
|![image](https://github.com/user-attachments/assets/3cea9f8f-c401-412b-9ca3-7d7cb82a1ef6)|![image](https://github.com/user-attachments/assets/855687a1-4765-4492-abca-119cca7fe9af)|
|[@hoya9802](https://github.com/hoya9802)|[@hjkim977](https://github.com/hjkim977)|

<br>

## 기능 소개

💡 **요리 보기** : 
  - 유저들의 다양한 레시피를 보고 나만의 레시피도 공유할 수 있어요!
   
💡 **재료 무료 나눔** :
  - 남는 재료를 무료로 나눔받고, 나눔하여 요리에 필요한 재료를 구할 수 있어요!
  
💡 **요리 실험 일지** :
  - 나만의 요리 실험 일지를 공유하고, 다른 사람들의 실험 일지도 확인할 수 있어요!
  
💡 **요리 지식인** :
  - 요리에 관하여 궁금한 점이 있으면 물어보고 댓글을 통해 답변을 받아볼 수 있어요!
  
💡 **AI 추천 레시피** :
  - 집에 있는 재료를 바탕으로 이전에 먹어보지 못한 색다른 요리를 추천받을 수 있어요!

💡 **유통기한 알림** :
  - 남은 재료들의 유통기한과 소비기한을 확인해 볼 수 있어요!

<br>

## 기능 미리보기
### 회원가입및 아이디 & 패스워드 찾기
![회원가입및아이디&패스워드찾기](https://github.com/user-attachments/assets/72c7a394-9de9-4399-b704-f2a4b2dcf20a)

 - 홈페이지에 접속하기 위해서는 회원가입을 해야 접속이 가능
 - Gmail API를 사용하여 아이디와 패스워드를 회원가입시 입력한 이메일을 통해서 발급

### 회원정보 수정
![회원정보 수정](https://drive.google.com/uc?id=1AivuAlWRDxu-yPbVyO4ZZ4B1NF7sOUQR)

 - 개인 프로필 정보들을 하나 또는 전체 수정이 가능
 - 비밀번호는 동일하게 2번 입력해야 수정이 가능

### 메인 페이지
![메인페이지](https://github.com/user-attachments/assets/98e25295-83ea-476b-92c5-cb58805c2604)

 - 배너 사진을 통해 웹사이트의 기능을 간단하게 소개
 - Best 레시피 : 사람 이모티콘을 가장 많이 받은 상위 5개의 레시피
 - 지구인은 이해할 수 없는 음식 : 외계인 이모티콘을 가장 많이 받은 상위 5개의 레시피
 - 요리의 재발견 : 좋아요를 가장 많이 받은 상위 3개의 요리실험일지

### 요리보기
![요리보기](https://github.com/user-attachments/assets/4d70add1-510e-4c52-9a2d-15c9a97777dd)

- 사람, 외계인에 투표 가능 (중복 투표, 다중 투표 불가) / 두번 누르면 투표 취소
- 한 페이지마다 12개씩 게시
- 요리 상세 페이지에 재료를 누르면 해당 재료를 가지고 있는 모든 레시피와 요리실험일지를 검색


### 신고하기
![신고하기](https://github.com/user-attachments/assets/d3907c27-a1af-4eca-9daa-70fb9b508a34)

 - 물건 상세보기를 누르면 우측 하단에 신고하기 버튼 활성화
 - 신고 내역은 관리자 페이지에서 확인 후 해당 유저 조치

### 재료 무료나눔
![재료무료나눔](https://github.com/user-attachments/assets/6ff74366-f285-4462-b524-d28c32550e2c)

 - 채팅을 통해서 나눔자와 1대1 채팅가능
 - 나눔자는 나눔 이후 나눔완료 버튼을 눌러서 나눔 종료 가능 (나눔 완료 버튼 이후에는 삭제만 가능)
 - 나눔이 종료된 상품은 여전히 목록에 보이지만 채팅은 불가능

### 요리실험 일지
![요리실험일지](https://github.com/user-attachments/assets/c9ea13a6-43d7-41af-bc6e-065218346cd4)

 - 좋아요 기능 (중복 투표 불가)
 - 재료 버튼을 누르면 해당 재료를 가지고 있는 게시글 검색

### 요리 지식인
![요리지식인](https://github.com/user-attachments/assets/982ee90b-2fae-4b32-a454-904e561ab81c)

 - 댓글 기능
 - 내가 올린 댓글 수정&삭제 가능

### AI 추천 레시피
![Ai레시피추천](https://github.com/user-attachments/assets/bc1c9559-db08-4dea-8e24-eded664dd8e0)

 - 영어로 재료들을 하나씩 추가 (최대 5개까지 가능)
 - 생성형 AI가 새로운 레시피를 추천 (단 영어로 추천)
 - 요리의 이름 / 내가 입력한 재료 / 요리를 만들때 필요한 재료 / 요리 만드는 방법 추천

### 유통기한&공지사항
![유통기한&공지사항](https://drive.google.com/uc?id=1RXY6nb1WB7nlDw6wZYCFRvjlOgAMqg1T)

 - 재료의 유통기한 확인 가능
 - 웹사이트의 공지사항을 확인 가능

### 레시피 수정&삭제
![레시피수정 삭제](https://github.com/user-attachments/assets/b0b7304b-f23f-478c-b55a-177bcadbe992)

 - 내가 올린 레시피들을 확인 가능
 - 확인 후 레시피를 수정 및 삭제 가능

### 회원탈퇴
![회원탈퇴](https://drive.google.com/uc?id=1Oik6KQBKKx6GYoJFG7xzmhtM5HpscJp4)

 - 회원정보 수정페이지에서 패스워드 한번 더 입력하면 계정 삭제


## 🔥 향후 계획
- 배포 진행 예정
- 아쉬운 부분은 꾸준히 수정 예정

