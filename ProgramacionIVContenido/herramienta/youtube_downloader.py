import os
from pytube import YouTube

def download_video(url, save_path):
    """
    Descarga un video de YouTube a la ruta especificada.

    Args:
        url (str): La URL del video de YouTube.
        save_path (str): El directorio donde se guardará el video.
    """
    try:
        yt = YouTube(url)
        # Selecciona la primera transmisión disponible (generalmente la de mejor calidad)
        stream = yt.streams.get_highest_resolution()
        
        print(f"Descargando: '{yt.title}'...")
        stream.download(output_path=save_path)
        print(f"¡Descarga completada! Video guardado en: {save_path}")

    except Exception as e:
        print(f"Ocurrió un error: {e}")

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Descargador de videos de YouTube.")
    parser.add_argument("url", help="La URL del video de YouTube a descargar.")
    parser.add_argument("path", help="La ruta de la carpeta para guardar el video.")
    args = parser.parse_args()

    video_url = args.url
    download_dir = args.path

    # Verificar si el directorio existe, si no, crearlo
    if not os.path.exists(download_dir):
        print(f"El directorio '{download_dir}' no existe, creándolo...")
        os.makedirs(download_dir)

    # Llamar a la función de descarga
    if video_url and download_dir:
        download_video(video_url, download_dir)
    else:
        print("La URL del video y la ruta de la carpeta no pueden estar vacías.")