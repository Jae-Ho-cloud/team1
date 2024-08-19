import pandas as pd

#2015~2020년 기간 동안의 시도별 온실가스 배출량, 흡수량 및 중립도 데이터를 dataframe으로 읽어옴
co2_data = pd.read_csv('Data\시도별 온실가스 중립도 (2015_2020년).csv', low_memory=False)

#최신 데이터를 지도에 시각화하기 위해 2020년 데이터만 필터해서 co2_data_2020에 저장
co2_data_2020 = co2_data[co2_data['년도']==2020]

#온실가스 배출량 및 흡수량의 단위를 소숫점 2째짜리 까지 백만ton 단위로 변경
co2_data_2020.loc[ : , '온실가스배출량'] = round(co2_data_2020['온실가스배출량']/1000000, 2)
co2_data_2020.loc[ : , '온실가스흡수량'] = round(co2_data_2020['온실가스흡수량']/1000000, 2)

#온실가스 중립도를 소숫점 2자리까지만 표시하도록 변경
co2_data_2020.loc[ : , '온실가스중립도'] = round(co2_data_2020['온실가스중립도'], 2)

# 컴럼 index에 단위를 표시
co2_data_2020.rename(columns={'온실가스배출량': '온실가스배출량(백만ton)', '온실가스흡수량': '온실가스흡수량(백만ton)', '온실가스중립도':'온실가스중립도(%)'}, inplace=True)

import geopandas as gpd
import folium
import branca.colormap as cm

# 대한민국 시도 경계 데이터를 GeoJSON 포맷으로 로드
url = 'https://raw.githubusercontent.com/southkorea/southkorea-maps/master/kostat/2013/json/skorea_provinces_geo_simple.json'
gdf = gpd.read_file(url)

# 시도별 지도 데이터를 dataframe에 저장

map_data = pd.DataFrame({
    'Province': ['서울특별시', '부산광역시', '대구광역시', '인천광역시', '광주광역시', '대전광역시', 
                 '울산광역시', '세종특별자치시', '경기도', '강원도', '충청북도', '충청남도', 
                 '전라북도', '전라남도', '경상북도', '경상남도', '제주특별자치도'],
    'Latitude': [37.5665, 35.1796, 35.8722, 37.4563, 35.1595, 36.3504,
                 35.5399, 36.4802, 37.2752, 37.8854, 36.6357, 36.5184,
                 35.8205, 34.8160, 36.5760, 35.1796, 33.4996],
    'Longitude': [126.9780, 129.0756, 128.6014, 126.7052, 126.8526, 127.3845,
                  129.3114, 127.2890, 127.0096, 127.7298, 127.4914, 126.7998,
                  127.1088, 126.4637, 128.5057, 128.2115, 126.5312]
})

# co2_data_2020과 map_data를 merge해서 시도별 온실가스 데이터와 시도별 위도, 경도 정보를 한 데이터프레임에 저장
co2_data_2020_w_map = pd.merge(co2_data_2020, map_data, left_on='시도명', right_on='Province', how='left')
co2_data_2020_w_map.drop(columns='Province', inplace=True)

# 지도 객체 생성
m = folium.Map(location=[36.5, 127.5], zoom_start=7)

# 녹색-빨강 색상 팔레트 생성
colormap = cm.LinearColormap(
    colors=['green', 'red'],
    index=[co2_data_2020_w_map['온실가스중립도(%)'].min(), co2_data_2020_w_map['온실가스중립도(%)'].max()],
    vmin=co2_data_2020_w_map['온실가스중립도(%)'].min(),
    vmax=co2_data_2020_w_map['온실가스중립도(%)'].max(),
    caption='co2_neutrality'
)

# Choropleth layer 추가: 온실가스중립도(%)
folium.Choropleth(
    geo_data=gdf,
    name="co2_neutrality",
    data=co2_data_2020_w_map,
    columns=["시도명", "온실가스중립도(%)"],
    key_on="feature.properties.name",
    fill_color="RdYlGn",
    fill_opacity=0.5,
    line_opacity=0.5,
    legend_name="온실가스중립도(%)",
).add_to(m)

# 시도별로 온실가스 배출량에 비례한 크기의 원형 마커를 추가하고, 시도명, 배출량, 흡수량 및 중립도 등의 상세 정보를 볼 수 있는 popup 추가
for i in range(len(co2_data_2020_w_map)):
    folium.Circle(
        location=[co2_data_2020_w_map.iloc[i]['Latitude'], co2_data_2020_w_map.iloc[i]['Longitude']],
        radius=co2_data_2020_w_map.iloc[i]['온실가스배출량(백만ton)'] * 300,  # 온실가스 배출량에 비례한 반지름 크기 (값에 따라 조정 가능)
        color='red',
        fill=True,
        fill_color='grey',
        fill_opacity=0.3,
        popup=(
            f"""
            <div style="width: 130px;">
                <b>{co2_data_2020_w_map.iloc[i]['시도명']}</b><br>
                배출량: {co2_data_2020_w_map.iloc[i]['온실가스배출량(백만ton)']:,}(백만ton)<br>
                흡수량: {co2_data_2020_w_map.iloc[i]['온실가스흡수량(백만ton)']:,}(백만ton)<br>
                중립도: {co2_data_2020_w_map.iloc[i]['온실가스중립도(%)']}%
            </div>
            """
        )
    ).add_to(m)


# 레이어 컨트롤 추가
folium.LayerControl().add_to(m)

# 지도를 HTML 파일로 저장
m.save('korea_co2_neutrality_map_with_circles_by_generation.html')


# 지도 객체 생성
m = folium.Map(location=[36.5, 127.5], zoom_start=7)

# 녹색-빨강 색상 팔레트 생성
colormap = cm.LinearColormap(
    colors=['green', 'red'],
    index=[co2_data_2020_w_map['온실가스중립도(%)'].min(), co2_data_2020_w_map['온실가스중립도(%)'].max()],
    vmin=co2_data_2020_w_map['온실가스중립도(%)'].min(),
    vmax=co2_data_2020_w_map['온실가스중립도(%)'].max(),
    caption='co2_neutrality'
)

# Choropleth layer 추가: 온실가스중립도(%)
folium.Choropleth(
    geo_data=gdf,
    name="co2_neutrality",
    data=co2_data_2020_w_map,
    columns=["시도명", "온실가스중립도(%)"],
    key_on="feature.properties.name",
    fill_color="RdYlGn",
    fill_opacity=0.5,
    line_opacity=0.5,
    legend_name="온실가스중립도(%)",
).add_to(m)

# 시도별로 온실가스 배출량에 비례한 크기의 원형 마커를 추가하고, 시도명, 배출량, 흡수량 및 중립도 등의 상세 정보를 볼 수 있는 popup 추가
for i in range(len(co2_data_2020_w_map)):
    folium.Circle(
        location=[co2_data_2020_w_map.iloc[i]['Latitude'], co2_data_2020_w_map.iloc[i]['Longitude']],
        radius=co2_data_2020_w_map.iloc[i]['온실가스흡수량(백만ton)'] * 3000,  # 온실가스 배출량에 비례한 반지름 크기 (값에 따라 조정 가능)
        color='blue',
        fill=True,
        fill_color='grey',
        fill_opacity=0.3,
        popup=(
            f"""
            <div style="width: 130px;">
                <b>{co2_data_2020_w_map.iloc[i]['시도명']}</b><br>
                배출량: {co2_data_2020_w_map.iloc[i]['온실가스배출량(백만ton)']:,}(백만ton)<br>
                흡수량: {co2_data_2020_w_map.iloc[i]['온실가스흡수량(백만ton)']:,}(백만ton)<br>
                중립도: {co2_data_2020_w_map.iloc[i]['온실가스중립도(%)']}%
            </div>
            """
        )
    ).add_to(m)


# 레이어 컨트롤 추가
folium.LayerControl().add_to(m)

# 지도를 HTML 파일로 저장
m.save('korea_co2_neutrality_map_with_circles_by_absorption.html')




