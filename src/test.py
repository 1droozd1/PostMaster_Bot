import os
def get_jpg_filenames(directory):
    # Проверяем, существует ли директория
    if not os.path.exists(directory):
        os.makedirs(directory)
        return 0
    
    # Получаем список всех файлов в директории
    files = os.listdir(directory)
    
    # Фильтруем список файлов, оставляя только файлы с расширением .jpg
    jpg_files = [int(file.split(".")[0]) for file in files if file.lower().endswith('.jpg')]
    
    return max(jpg_files)

print(get_jpg_filenames('./data'))