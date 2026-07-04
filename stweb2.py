# rail.py
import datetime
import streamlit as st
import csv
import io
import operator as op
import matplotlib.pyplot as plt
import random
# 한글 폰트 설정 - Windows 기준
plt.rc('font', family='Malgun Gothic')
plt.rcParams['axes.unicode_minus'] = False

st.title('지하철 승하차 인원 분석')

file = st.file_uploader('CSV 파일 업로드', type='csv')

if file is not None:

    # =========================
    # 1. CSV 파일 읽기
    # =========================

    text = io.TextIOWrapper(file, encoding='utf-8-sig')
    data = csv.reader(text)

    header = next(data)
    data = list(data)

    st.write('컬럼명:', header)
    st.write('첫 번째 데이터:', data[0])

    # 승차/하차 인원 int 변환
    for row in data:
        row[3] = int(row[3])
        row[4] = int(row[4])

    # =========================
    # 2. 특정역 승하차 인원 변화
    # =========================

    st.header('특정역 승하차 인원 변화')

    station_list = []

    for row in data:
        if row[2] not in station_list:
            station_list.append(row[2])

    station_list.sort()

    station = st.selectbox('역 선택', station_list)

    in_count = []
    out_count = []
    date = []

    for row in data:
        if station == row[2]:
            date.append(row[0])
            in_count.append(row[3])
            out_count.append(row[4])

    fig, ax = plt.subplots(figsize=(8, 4))

    ax.plot(date, in_count, 'r', label='승차')
    ax.plot(date, out_count, 'b', label='하차')

    ax.set_title(station + ' 승하차 인원 변화')
    ax.set_xlabel('사용일자')
    ax.set_ylabel('인원수')
    ax.legend()

    plt.xticks(rotation=45)
    st.pyplot(fig)

    # =========================
    # 3. 승차 인원 TOP 10
    # =========================

    st.header('승차 인원 TOP 10')

    dic = {}

    for row in data:
        station = row[2]
        count = row[3]

        if station in dic.keys():
            dic[station] += count
        else:
            dic[station] = count

    dic = sorted(dic.items(), key=op.itemgetter(1), reverse=True)[:10]

    top10_station = []
    top10_count = []

    for row in dic:
        top10_station.append(row[0])
        top10_count.append(row[1])

    fig, ax = plt.subplots(figsize=(8, 5))

    ax.barh(top10_station, top10_count, color='r')
    ax.set_title('승차 인원 TOP 10')
    ax.set_xlabel('승차 인원')

    st.pyplot(fig)

    # =========================
    # 4. 하차 인원 TOP 10
    # =========================

    st.header('하차 인원 TOP 10')

    dic2 = {}

    for row in data:
        station = row[2]
        count = row[4]

        if station in dic2.keys():
            dic2[station] += count
        else:
            dic2[station] = count

    dic2 = sorted(dic2.items(), key=op.itemgetter(1), reverse=True)[:10]

    top10_station2 = []
    top10_count2 = []

    for row in dic2:
        top10_station2.append(row[0])
        top10_count2.append(row[1])

    fig, ax = plt.subplots(figsize=(8, 5))

    ax.barh(top10_station2, top10_count2, color='b')
    ax.set_title('하차 인원 TOP 10')
    ax.set_xlabel('하차 인원')

    st.pyplot(fig)

else:
    st.info('CSV 파일을 업로드하세요.')
st.title(':sparkles:로또 생성기:sparkles:')


def generate_lotto():
    lotto = set()

    while len(lotto) < 6:
        number = random.randint(1, 46)
        lotto.add(number)

    lotto = list(lotto)
    lotto.sort()
    return lotto

# st.subheader(f'행운의 번호: :green[{generate_lotto()}]')
# st.write(f"생성된 시각: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}")

button = st.button('오늘의 번호')

if button:
    for i in range(1, 6):
        st.subheader(f'{i}. 번호: :green[{generate_lotto()}]')
    st.write(f"생성된 시각: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}")

