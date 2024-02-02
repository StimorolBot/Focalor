import os


def get_list_img(path: str) -> list:
    if os.path.exists(path) and os.path.isdir(path):
        return os.listdir(path)
    else:
        raise FileNotFoundError("[!] Директория не найдена")

