import asyncio
import aiofiles
import os
import shutil
import logging
from pathlib import Path
from argparse import ArgumentParser

# Налаштування логування
logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

# Асинхронна функція для копіювання файлу до нової директорії на основі його розширення
async def copy_file(file_path, output_folder):
    try:
        file_extension = file_path.suffix.lstrip('.') or 'no_extension'
        target_folder = output_folder / file_extension
        
        # Створення папки, якщо вона не існує
        target_folder.mkdir(parents=True, exist_ok=True)
        
        # Копіювання файлу в нову папку
        await asyncio.to_thread(shutil.copy, file_path, target_folder / file_path.name)
        print(f'Копіювання файлу: {file_path} в {target_folder}')
    except Exception as e:
        logging.error(f'Помилка при копіюванні файлу {file_path}: {e}')

# Асинхронна функція для рекурсивного читання папок та пошуку файлів
async def read_folder(source_folder, output_folder):
    tasks = []
    try:
        for root, _, files in os.walk(source_folder):
            for file_name in files:
                file_path = Path(root) / file_name
                tasks.append(copy_file(file_path, output_folder))
        
        # Виконання всіх завдань асинхронно
        await asyncio.gather(*tasks)
    except Exception as e:
        logging.error(f'Помилка при читанні папки {source_folder}: {e}')

# Основна функція для запуску програми
async def main(source_folder, output_folder):
    source_folder = Path(source_folder)
    output_folder = Path(output_folder)
    
    if not source_folder.exists():
        logging.error(f'Вихідна папка {source_folder} не існує.')
        return
    
    # Старт рекурсивного читання та сортування файлів
    await read_folder(source_folder, output_folder)

# Обробка аргументів командного рядка
if __name__ == "__main__":
    parser = ArgumentParser(description="Асинхронний сортувальник файлів за розширенням")
    parser.add_argument("source", help="Вихідна папка для читання файлів")
    parser.add_argument("output", help="Цільова папка для збереження відсортованих файлів")
    
    args = parser.parse_args()
    
    # Запуск асинхронного головного процесу
    asyncio.run(main(args.source, args.output))
