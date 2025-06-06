import geopandas as gpd
import zipfile
import os

# from sentinela import utils  # Descomente se precisar de funções auxiliares

def extract_zip(zip_path, extract_to):
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)

def load_shapefile_from_zip(zip_path):
    temp_folder = "./data/temp_shapefiles"
    os.makedirs(temp_folder, exist_ok=True)
    
    extract_zip(zip_path, temp_folder)
    
    # Procura o .shp extraído
    for root, dirs, files in os.walk(temp_folder):
        for file in files:
            if file.endswith(".shp"):
                shp_path = os.path.join(root, file)
                gdf = gpd.read_file(shp_path)
                print(f"Arquivo carregado: {shp_path}")
                return gdf
    raise FileNotFoundError("Shapefile não encontrado no zip.")

# Exemplo de uso:
if __name__ == "__main__":
    path = "./data/raw/floods/floods/aldeias_pontos.zip"
    gdf = load_shapefile_from_zip(path)
    print(gdf.head())
