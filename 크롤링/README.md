# 🕸️ 웹 크롤링 모음

정적 페이지부터 동적 페이지, 이미지 OCR, 공식 API까지 다양한 방식의 수집 코드입니다. 인터파크 수집 코드는 [추천시스템](../추천시스템) 프로젝트의 데이터로 쓰였습니다.

| 파일 | 대상 | 방식 | 수집 내용 |
|---|---|---|---|
| `1)_크롤링+스크레이핑_.ipynb` | Python 공식 매뉴얼 | urllib + BeautifulSoup | 링크를 따라가며 문서 전체를 재귀적으로 다운로드 |
| `구글플레이스토어_리뷰.ipynb` | Google Play 앱 상세 | Selenium (무한 스크롤 · 더보기 클릭) + BeautifulSoup | 앱 리뷰 |
| `유튜브_댓글.ipynb` | YouTube 영상 | Selenium (무한 스크롤) | 댓글 |
| `유튜브_댓글_API이용.ipynb` | YouTube Data API v3 | google-api-python-client | 댓글 · 답글, 작성일, 좋아요 수 (API 키는 환경변수 `YOUTUBE_API_KEY`) |
| `인터파크_월간랭킹뮤지컬_배우.ipynb` | 인터파크 티켓 월간 랭킹 | Selenium | 뮤지컬별 출연 배우 |
| `인터파크_월간랭킹연극_공연상세 이미지.ipynb` | 인터파크 공연 상세 | Selenium + OpenCV · Tesseract | 상세 이미지 저장 → OCR 전처리 |

## 방식별 정리

| 방식 | 언제 쓰나 | 사용 파일 |
|---|---|---|
| requests / urllib + BeautifulSoup | HTML이 처음부터 다 내려오는 정적 페이지 | 크롤링+스크레이핑 |
| Selenium | 스크롤·클릭으로 내용이 늘어나는 동적 페이지 | 플레이스토어, 유튜브, 인터파크 |
| OCR (Tesseract) | 텍스트가 이미지로만 제공될 때 | 인터파크 공연 상세 |
| 공식 API | 제공되는 경우 가장 안정적 · 약관 준수 | 유튜브 API |

수집한 댓글 · 리뷰에는 작성자 정보가 포함되어 있어, 노트북의 실행 결과는 지우고 코드만 올렸습니다.
