"""Regenerate ARCHIVED original SVG diagrams (Python standard library only).

Run: python scripts/generate-diagrams.py
The active AI-generated images, question Markdown and schedule are never modified.
"""
from pathlib import Path
from html import escape

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'archive' / 'diagrams'
OUT.mkdir(parents=True, exist_ok=True)
INK = '#172b35'
TEAL = '#087f73'
BLUE = '#3566b8'
RED = '#bd5340'
MUTED = '#5c7079'

class Diagram:
    def __init__(self, number, category, title, subtitle, takeaway):
        self.parts = [f'''<svg xmlns="http://www.w3.org/2000/svg" width="1400" height="900" viewBox="0 0 1400 900" role="img" aria-labelledby="title desc">
<title id="title">{escape(title)}</title><desc id="desc">{escape(subtitle)}. {escape(takeaway)}</desc>
<defs><marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse"><path d="M 0 0 L 10 5 L 0 10 z" fill="context-stroke"/></marker></defs>
<rect width="1400" height="900" fill="#f4f7f7"/>
<g font-family="Malgun Gothic, Noto Sans KR, Arial, sans-serif">''']
        self.text(64, 53, '만듦 / DAILY CS', 19, TEAL, bold=True)
        self.text(1336, 53, f'{number:02d} / {category}', 19, MUTED, anchor='end')
        self.text(64, 124, title, 44, INK, bold=True)
        self.text(64, 172, subtitle, 24, MUTED)
        self.rect(44, 210, 1312, 515, '#ffffff', '#e0e9e8', 24)
        self.rect(44, 754, 1312, 90, '#e2f0eb', 'none', 18)
        self.text(74, 808, takeaway, 25, TEAL, bold=True)
        self.text(64, 876, 'MANDEUM  ·  직접 제작한 학습용 개념도', 16, MUTED)
        self.text(1336, 876, '세부 조건과 참고 문서는 본문에서 확인하세요.', 16, MUTED, anchor='end')

    def rect(self, x,y,w,h,fill='#eff5f5',stroke='#d4e2e0',r=14):
        self.parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}" stroke="{stroke}" stroke-width="2"/>')

    def text(self,x,y,value,size=25,color=INK,bold=False,anchor='start'):
        self.parts.append(f'<text x="{x}" y="{y}" fill="{color}" font-size="{size}" font-weight="{700 if bold else 400}" text-anchor="{anchor}">{escape(value)}</text>')

    def lines(self,x,y,values,size=24,color=INK,gap=37,anchor='start',bold=False):
        for n,v in enumerate(values): self.text(x,y+n*gap,v,size,color,bold,anchor)

    def arrow(self,x1,y1,x2,y2,color=TEAL,dashed=False):
        dash = 'stroke-dasharray="8 8"' if dashed else ''
        self.parts.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="3" {dash} marker-end="url(#arrow)"/>')

    def line(self,x1,y1,x2,y2,color='#d6e1e3',dashed=False):
        dash = 'stroke-dasharray="7 7"' if dashed else ''
        self.parts.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="2" {dash}/>')

    def card(self,x,y,w,h,title,body=(),fill='#eff5f5',color=TEAL):
        self.rect(x,y,w,h,fill)
        self.text(x+24,y+42,title,27,color,True)
        self.lines(x+24,y+82,body,23,MUTED)

    def save(self, slug):
        (OUT / f'{slug}.svg').write_text('\n'.join(self.parts)+ '\n</g></svg>\n', encoding='utf-8')

d=Diagram(1,'운영체제','프로세스는 공간, 스레드는 실행 흐름','공유하는 자원과 따로 유지하는 실행 상태를 구분해 보세요.','핵심  /  같은 프로세스의 스레드는 주소 공간을 공유합니다.')
d.rect(84,250,730,428,'#f7fbfa','#8bbfb4')
d.text(110,295,'프로세스 A · 하나의 주소 공간',29,TEAL,True)
d.card(110,320,676,106,'코드 · 데이터 · 힙', ['두 스레드가 함께 사용하는 자원'])
d.card(110,474,315,152,'스레드 A1',['자신의 스택','레지스터 · 실행 위치'])
d.card(471,474,315,152,'스레드 A2',['자신의 스택','레지스터 · 실행 위치'])
d.arrow(265,473,265,429);d.arrow(628,473,628,429)
d.rect(862,250,452,428,'#f7f9fd','#a4b7d6')
d.text(888,295,'프로세스 B',29,BLUE,True)
d.card(888,320,400,106,'별도 주소 공간',['코드 · 데이터 · 힙'],'#eef3fb',BLUE)
d.card(888,474,400,152,'스레드 B1',['자신의 스택','레지스터 · 실행 위치'],'#eef3fb',BLUE)
d.arrow(1088,473,1088,429,BLUE)
d.save('process-and-thread')

d=Diagram(2,'운영체제','두 번 증가했는데, 결과는 1?','동기화되지 않은 읽기 → 계산 → 쓰기가 겹치는 실행 순서입니다.','핵심  /  읽기부터 쓰기까지 보호하거나 원자적 증가를 사용합니다.')
d.text(143,265,'시간 ↓',22,MUTED,True)
d.text(455,265,'스레드 A',28,TEAL,True,anchor='middle')
d.text(930,265,'스레드 B',28,BLUE,True,anchor='middle')
d.line(180,292,180,664)
for i,(a,b) in enumerate([('0을 읽음',''),('','0을 읽음'),('0 + 1을 계산 → 1 기록',''),('','0 + 1을 계산 → 1 기록')]):
    y=295+i*79
    d.text(166,y+38,str(i+1),23,MUTED,anchor='end')
    d.line(210,y+62,1230,y+62)
    if a:d.rect(270,y,370,55,'#e6f3ef');d.text(455,y+36,a,23,TEAL,anchor='middle')
    if b:d.rect(745,y,370,55,'#edf2fc');d.text(930,y+36,b,23,BLUE,anchor='middle')
d.rect(365,635,690,58,'#fff0e9','#e9c0af')
d.text(710,673,'초깃값 0  →  기대한 값 2  /  실제 결과 1',26,RED,True,anchor='middle')
d.save('race-condition')

d=Diagram(3,'운영체제','서로 기다리면 멈추는 교착 상태','이미 가진 락을 놓지 않고 상대의 락을 기다리는 상황입니다.','핵심  /  모든 경로가 X → Y 순서로 락을 얻도록 통일합니다.')
d.card(135,365,360,178,'스레드 A',['보유: 락 X','필요: 락 Y'],'#e9f4ef')
d.card(905,365,360,178,'스레드 B',['보유: 락 Y','필요: 락 X'],'#edf2fc',BLUE)
d.arrow(470,310,930,310,RED)
d.text(700,286,'A는 B가 가진 Y를 기다림',25,RED,anchor='middle')
d.line(470,310,470,362,RED);d.line(930,310,930,362,RED)
d.arrow(930,592,470,592,RED)
d.text(700,634,'B는 A가 가진 X를 기다림',25,RED,anchor='middle')
d.line(470,546,470,592,RED);d.line(930,546,930,592,RED)
d.text(700,451,'순환 대기',32,RED,True,anchor='middle')
d.text(700,490,'진행 불가',23,MUTED,anchor='middle')
d.save('deadlock')

d=Diagram(4,'네트워크','TCP 연결의 세 번의 확인','예시 초기 시퀀스 번호: 클라이언트 100 / 서버 500','핵심  /  서로의 초기 시퀀스 번호를 확인해 연결 상태를 만듭니다.')
d.rect(180,242,240,65);d.text(300,286,'클라이언트',28,TEAL,True,anchor='middle')
d.rect(980,242,240,65,'#edf2fc');d.text(1100,286,'서버',28,BLUE,True,anchor='middle')
d.line(300,308,300,688,dashed=True);d.line(1100,308,1100,688,dashed=True)
d.text(700,353,'① SYN  ·  seq=100',25,TEAL,True,anchor='middle');d.arrow(306,376,1094,405)
d.text(700,445,'② SYN + ACK  ·  seq=500, ack=101',25,BLUE,True,anchor='middle');d.arrow(1094,463,306,494,BLUE)
d.text(700,544,'③ ACK  ·  seq=101, ack=501',25,TEAL,True,anchor='middle');d.arrow(306,565,1094,596)
d.text(700,672,'SYN은 시퀀스 번호 1개를 소비합니다.  ·  데이터 없는 시작 예시',22,MUTED,anchor='middle')
d.save('tcp-three-way-handshake')

d=Diagram(5,'네트워크','DNS: 이름의 답을 찾아가는 과정','필요한 캐시가 없는 경우를 단순화한 예시입니다.','핵심  /  캐시가 유효하면 전체 조회 경로를 반복하지 않아도 됩니다.')
d.card(90,425,270,120,'사용자 기기',['www.example.com'])
d.card(485,388,300,180,'재귀 리졸버',['조회 수행','결과를 캐시에 보관'])
d.arrow(366,452,479,452);d.arrow(479,525,366,525,BLUE)
d.text(420,430,'요청',20,TEAL,anchor='middle');d.text(420,557,'응답',20,BLUE,anchor='middle')
d.card(1000,244,305,110,'① 루트 DNS',['.com 담당 안내'])
d.card(1000,416,305,110,'② .com TLD',['권한 서버 안내'])
d.card(1000,588,305,110,'③ 권한 DNS',['A / AAAA 응답'])
d.arrow(790,408,992,284);d.arrow(992,322,790,442,BLUE)
d.arrow(790,467,992,453);d.arrow(992,490,790,498,BLUE)
d.arrow(790,523,992,624);d.arrow(992,662,790,556,BLUE)
d.text(505,650,'초록: 문의  /  파랑: 응답',22,MUTED)
d.save('dns-resolution')

d=Diagram(6,'네트워크','304: 본문은 그대로, 유효한지만 확인','저장된 응답이 오래되어 재검증이 필요한 상황입니다.','핵심  /  304는 통신을 생략하는 것이 아니라 본문 재전송을 줄입니다.')
d.card(100,250,390,145,'브라우저 캐시',['저장한 본문','ETag: "v1"'])
d.card(910,250,390,145,'서버',['현재 표현의 ETag','"v1" → 변경 없음'],'#edf2fc',BLUE)
d.text(700,451,'If-None-Match: "v1"',25,TEAL,True,anchor='middle');d.arrow(303,474,1097,474)
d.text(700,548,'304 Not Modified  ·  응답 본문 없음',25,BLUE,True,anchor='middle');d.arrow(1097,568,303,568,BLUE)
d.rect(100,618,1200,62,'#e6f3ef')
d.text(700,658,'브라우저는 저장한 본문을 재사용합니다.',27,TEAL,True,anchor='middle')
d.save('http-cache-validation')

d=Diagram(7,'데이터베이스','인덱스로 검색 범위를 좁히기','조회 조건: 가격 ≥ 30 AND 가격 < 40  /  구간 선택 개념도','핵심  /  조회 비용을 줄이는 대신 저장 공간과 변경 관리 비용이 듭니다.')
d.rect(460,253,480,70);d.text(700,299,'정렬된 키로 탐색 경로 선택',28,TEAL,True,anchor='middle')
for x,label,color,fill in [(120,'0 ≤ 가격 < 20',MUTED,'#f2f5f6'),(530,'20 ≤ 가격 < 40',TEAL,'#dff2e9'),(940,'40 ≤ 가격',MUTED,'#f2f5f6')]:
    d.arrow(700,326,x+170,417,color)
    d.rect(x,423,340,84,fill)
    d.text(x+170,475,label,26,color,True,anchor='middle')
d.arrow(700,511,700,562)
d.rect(440,570,520,85,'#e8f4ee','#8bbfb4')
d.text(700,604,'해당 구간에서 30~39 검색',26,TEAL,True,anchor='middle')
d.text(700,638,'필요한 데이터 행으로 접근',23,MUTED,anchor='middle')
d.text(1095,613,'실제 노드 구조는',20,MUTED,anchor='middle');d.text(1095,644,'구현에 따라 다릅니다.',20,MUTED,anchor='middle')
d.save('database-btree-index')

d=Diagram(8,'데이터베이스','두 번째 조회에도 같은 값일까요?','PostgreSQL · 같은 트랜잭션 A의 일반 SELECT · A 자신의 변경 없음','핵심  /  Read Committed는 명령별, Repeatable Read는 같은 스냅샷입니다.')
d.rect(335,244,440,62,'#eff5f5');d.text(555,285,'Read Committed',27,TEAL,True,anchor='middle')
d.rect(825,244,440,62,'#edf2fc');d.text(1045,285,'Repeatable Read',27,BLUE,True,anchor='middle')
d.text(100,354,'A의 첫 조회',25,INK,True)
d.text(555,362,'100',42,TEAL,True,anchor='middle');d.text(1045,362,'100',42,BLUE,True,anchor='middle')
d.rect(335,405,930,74,'#fff1e6','#e5c7a8')
d.text(800,452,'트랜잭션 B: 잔액을 80으로 변경 후 COMMIT',25,RED,True,anchor='middle')
d.arrow(555,486,555,534);d.arrow(1045,486,1045,534,BLUE)
d.text(100,580,'A의 두 번째 조회',25,INK,True)
d.text(555,590,'80',46,TEAL,True,anchor='middle');d.text(1045,590,'100',46,BLUE,True,anchor='middle')
d.text(555,648,'새 명령의 스냅샷',25,MUTED,anchor='middle');d.text(1045,648,'기존 스냅샷 유지',25,MUTED,anchor='middle')
d.save('transaction-isolation')

d=Diagram(9,'자료구조','스택과 큐: 먼저 나오는 것은?','두 자료구조에 A → B → C 순서로 넣었습니다.','핵심  /  스택은 최근 항목부터, FIFO 큐는 먼저 들어온 항목부터 꺼냅니다.')
d.text(370,280,'STACK · LIFO',30,TEAL,True,anchor='middle')
d.text(1030,280,'QUEUE · FIFO',30,BLUE,True,anchor='middle')
d.line(700,260,700,672)
for i,letter in enumerate(['C','B','A']):
    d.rect(245,333+i*81,250,67,'#e2f1eb')
    d.text(370,378+i*81,letter,32,TEAL,True,anchor='middle')
d.arrow(510,366,620,366);d.text(620,336,'먼저 꺼냄',21,TEAL,anchor='end')
for i,letter in enumerate(['A','B','C']):
    d.rect(824+i*137,378,112,100,'#eaf0fb')
    d.text(880+i*137,442,letter,34,BLUE,True,anchor='middle')
d.arrow(878,488,878,555,BLUE);d.text(1030,548,'A부터 꺼냄',23,BLUE,anchor='middle')
d.text(370,647,'꺼내는 순서  C → B → A',28,TEAL,True,anchor='middle')
d.text(1030,647,'꺼내는 순서  A → B → C',28,BLUE,True,anchor='middle')
d.save('stack-and-queue')

d=Diagram(10,'자료구조','해시 충돌은 키 비교로 구분합니다','설명용 함수 h(key) = key % 4  /  체이닝으로 충돌 처리','핵심  /  같은 버킷에 도착해도 같은 키라는 뜻은 아닙니다.')
d.card(93,293,300,100,'키 5 → 나머지 1',[], '#e7f3ed')
d.card(93,469,300,100,'키 9 → 나머지 1',[], '#edf2fc',BLUE)
for i in range(4):
    y=260+i*101
    d.rect(530,y,210,79,'#def0e7' if i==1 else '#f1f5f5')
    d.text(635,y+50,f'버킷 {i}',27,TEAL if i==1 else MUTED,i==1,anchor='middle')
d.arrow(396,344,523,393);d.arrow(396,520,523,415,BLUE)
d.arrow(748,400,816,400)
d.card(825,358,205,106,'키 5',['값 A'])
d.arrow(1038,410,1102,410)
d.card(1110,358,205,106,'키 9',['값 B'],'#edf2fc',BLUE)
d.lines(825,556,['조회할 키가 9라면?','키 5와 다름 → 다음 항목','키 9와 같음 → 값 B 반환'],24,MUTED,gap=42)
d.save('hash-table-collision')

print(f'Generated 10 SVG diagrams in {OUT}')
