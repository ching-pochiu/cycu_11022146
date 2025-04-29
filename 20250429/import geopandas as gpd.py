import geopandas as gpd
import pandas as pd

class taipei_route_list:
    def read_from_database(self) -> pd.DataFrame:
        # 模擬從資料庫讀取資料
        data = [
            {"route_id": "001", "route_name": "Route 1"},
            {"route_id": "002", "route_name": "Route 2"}
        ]
        return pd.DataFrame(data)

if __name__ == "__main__":
    # Initialize and process route data
    route_list = taipei_route_list()
    
    # 定義一個空的 GeoDataFrame 並設定 CRS
    geo_df = gpd.GeoDataFrame(columns=['wkt_id', 'wkt_string', 'route_id', 'route_name', 'geometry'])
    geo_df.crs = 'EPSG:4326'

    for _, row in route_list.read_from_database().iterrows():
        try:
            # 模擬 taipei_route_info 的行為
            route_info = {"route_id": row["route_id"], "direction": "go"}
            dict_wkt = {"wkt_1": "POINT (121.5 25.0)", "wkt_2": "POINT (121.6 25.1)"}

            # Save the parsed data to a GeoDataFrame
            df = pd.DataFrame(dict_wkt.items(), columns=['wkt_id', 'wkt_string'])
            df['route_id'] = row["route_id"]
            df['route_name'] = row["route_name"]

            # Convert df to GeoDataFrame
            df['geometry'] = gpd.GeoSeries.from_wkt(df['wkt_string'])
            df = gpd.GeoDataFrame(df, geometry='geometry')
            df.crs = 'EPSG:4326'

            # Append the new data to the existing GeoDataFrame
            geo_df = pd.concat([geo_df, df], ignore_index=True)
            print(f"Route ID: {row['route_id']}, Processed {len(dict_wkt)} WKT entries.")
        except Exception as e:
            print(f"Error processing route {row['route_name']}: {e}")

    # Save the combined GeoDataFrame to a GeoPackage
    geo_df.to_file("ebus_taipei_routes.gpkg", layer='data_routes_wkt', driver='GPKG')