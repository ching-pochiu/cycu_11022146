import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
from shapely.geometry import Point, LineString
import xml.etree.ElementTree as ET
import os

# 更新路徑，指向正確的資料夾
shp_dir = "C:/Users/User/Desktop/直轄市、縣(市)界線1140318"
bus_stops_csv = "C:/Users/User/Desktop/cycu_11022146/20250520/34B402A8-53D9-483D-9406-24A682C2D6DC-公車站位資訊_6210631053086804136.csv"  # 公車站牌 .csv 檔案
bus_routes_xml = "C:/Users/User/Desktop/桃園公車路線.xml"  # XML 檔案路徑
shp_file = None

# 找出縣市界線的 .shp 檔案
for fname in os.listdir(shp_dir):
    if fname.endswith(".shp"):
        shp_file = os.path.join(shp_dir, fname)
        break

if shp_file is None:
    print("No shapefile found in", shp_dir)
else:
    # 讀取縣市界線 .shp 檔案
    gdf = gpd.read_file(shp_file)
    
    # 檢查欄位名稱
    print("欄位名稱：", gdf.columns)
    
    # 篩選北北基桃的資料
    target_cities = ["臺北市", "新北市", "基隆市", "桃園市"]  # 根據實際欄位值修改
    if "COUNTYNAME" in gdf.columns:
        gdf_filtered = gdf[gdf["COUNTYNAME"].isin(target_cities)]
    else:
        gdf_filtered = gdf  # 如果沒有篩選條件，繪製全部

    # 讀取公車站牌 .csv 檔案
    if os.path.exists(bus_stops_csv):
        bus_stops_df = pd.read_csv(bus_stops_csv)
        # 將經緯度轉換為 GeoDataFrame
        bus_stops_df["geometry"] = bus_stops_df.apply(
            lambda row: Point(float(row["longitude"]), float(row["latitude"])), axis=1
        )
        bus_stops_csv_gdf = gpd.GeoDataFrame(bus_stops_df, geometry="geometry", crs="EPSG:4326")
    else:
        print(f"公車站牌 CSV 檔案 {bus_stops_csv} 不存在")
        bus_stops_csv_gdf = None

    # 解析公車路線 XML 檔案
    if os.path.exists(bus_routes_xml):
        tree = ET.parse(bus_routes_xml)
        root = tree.getroot()

        # 提取路線資料
        routes = []
        for shape in root.findall("Shape"):
            geometry = shape.find("Geometry").text.strip().replace('"', '')
            coords = [
                tuple(map(float, coord.split()))
                for coord in geometry.replace("LINESTRING(", "").replace(")", "").split(",")
            ]
            routes.append(LineString(coords))

        # 建立 GeoDataFrame
        bus_routes_gdf = gpd.GeoDataFrame(geometry=routes, crs="EPSG:4326")
    else:
        print(f"公車路線 XML 檔案 {bus_routes_xml} 不存在")
        bus_routes_gdf = None

    # 確保座標系統一致
    if bus_routes_gdf is not None and bus_routes_gdf.crs != gdf_filtered.crs:
        bus_routes_gdf = bus_routes_gdf.to_crs(gdf_filtered.crs)

    # 繪製地圖
    ax = gdf_filtered.plot(edgecolor='black', figsize=(10, 10), cmap='Pastel1', alpha=0.5)
    if bus_routes_gdf is not None:
        bus_routes_gdf.plot(ax=ax, color='blue', linewidth=1, label='Bus Routes')  # 增加線條寬度
    if bus_stops_csv_gdf is not None:
        bus_stops_csv_gdf.plot(ax=ax, color='red', markersize=5, label='Bus Stops')

    # 動態生成標題
    title_cities = " ".join(target_cities)  # 將篩選的縣市名稱用空格連接
    plt.title(f"{title_cities} 區域地圖（含公車站牌與路線）")

    # 添加圖例和其他設定
    plt.legend()
    plt.axis('equal')
    plt.show()