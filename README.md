# C.C.G
SOFTWARE AND AI BUSINESS APPLICATION DESIGN 프로젝트: Crowdsourced Cloud Gaming 랜딩 페이지 및 데모


## 사용법

### 랜딩 페이지 호스팅하기
1. html5up-hyperspace_modified 폴더를 다운받아서 Netlify에 업로드.

### 랜딩 기록하기
구글 앱스크립트를 백엔드로, 구글 스프레드시트를 DB로 사용한다.
1. Googel_Spread_Sheet.xlsx의 형식대로 본인의 구글 드라이브에 스프레드시트 생성.
2. Google_Apps_Script 코드에서 상단의 <your google spread sheet url> 부분을 수정
3. 본인 구글 드라이브에 앱스크립트 프로젝트를 생성해서 코드를 복사하고 배포
4. 랜딩 페이지 index.html의 <your google apps script deployment url> 부분을 앱스크립트 배포 url로 수정

### 화면 스트리밍 데모 실행하기
1. 화면 스트리밍 호스트가 될 컴퓨터의 IP로 도메인 발급받기 (무료 서비스: Duck DNS)
2. demo.html의 <your_domain> 부분을 발급받은 도메인으로 변경
3. SSL 인증서 발급받기 (무료 서비스: ZeroSSL)
4. server.py 하단의 SSL 키 파일 경로와 SSL 인증서 파일 경로 수정
5. server.py의 <your Netlify landing page url> 부분을 수정
6. 화면 스트리밍 호스트가 될 컴퓨터에서 server.py 실행 (파이썬 버전 및 라이브러리 호환성 주의, 필자는 파이썬 3.9.13 사용)
7. 데모가 작동하는지 확인
8. 스트리밍을 중단하고 싶다면 server.py 실행 중지

