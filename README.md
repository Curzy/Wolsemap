# [curzy.xyz](http://curzy.xyz/)
____

### 서울 월세 노선도.

독일의 부동산 사이트 [immobilienscout24](https://www.immobilienscout24.de)의 독일 도시별 지하철 노선도 주변 one-room apartment의 평균 가격을 나타내는 [Miet-Map](https://www.immobilienscout24.de/immobilienbewertung/ratgeber/mietpreise-und-kaufpreise/mietspiegel/miet-map-berlin.html)에 영향을 받아 시작한 프로젝트 입니다.

서울 수도권 지하철 노선을 따라 조금 더 한국에 맞추어 보증금, 월세의 평균 정보를 나타내어 서울에서, 홀로, 살기 위해 가장 기본적이고 중요한 '주'의 비용에 대한 기준을 세울 수 있는 지표를 보여주려 하였습니다.

- nginx + uWSGI + Django로 AWS EC2에서 서비스 하고 있습니다.
- 다방, 직방의 API요청과 응답의 구조를 분석하여 매일 밤 지하철 역별 평균 월세 정보를 가져오고 있습니다
- Django + Celery로 매일밤 지하철 역에 대한 요청을 보내 JSON데이터를 받아 크롤링하며 Network 응답 시간에 따른 Block을 줄이기위해 Threading을 사용하였다가, 파이썬에서 Thread를 활용하는 문제때문에, 변경하였습니다.
- Front에서 JSON으로 가공된 데이터를 react-d3를 활용하여 월세, 보증금의 변화를 그래프로 그리고 있습니다.
- 비동기 태스크를 위한 Celery를 온전히 사용하기 위해 멀티쓰레딩을 제거하고 Celery Worker프로세서의 수를 늘려 크롤링 시간을 줄였습니다.

### Will

- 호선별, 지역별 데이터 통계
- async를 활용하여 더 빠른 크롤링
- 네이버 부동산 데이터 활용
- 지하철 노선도 리디자인
- Dive in SVG
