import string
import requests
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
import matplotlib.pyplot as plt

# Функція для завантаження тексту з URL
def get_text(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Перевірка на помилки HTTP
        return response.text
    except requests.RequestException as e:
        print(f"Помилка завантаження: {e}")
        return None

# Функція для видалення пунктуації
def remove_punctuation(text):
    return text.translate(str.maketrans("", "", string.punctuation))

# Map function: повертає пару слово-одиниця
def map_function(word):
    return word.lower(), 1

# Shuffle function: групування по ключах (словах)
def shuffle_function(mapped_values):
    shuffled = defaultdict(list)
    for key, value in mapped_values:
        shuffled[key].append(value)
    return shuffled.items()

# Reduce function: підсумовує частоти кожного слова
def reduce_function(key_values):
    key, values = key_values
    return key, sum(values)

# Функція MapReduce
def map_reduce(text):
    # Видаляємо пунктуацію
    text = remove_punctuation(text)
    words = text.split()

    # Паралельний Мапінг
    with ThreadPoolExecutor() as executor:
        mapped_values = list(executor.map(map_function, words))

    # Shuffle
    shuffled_values = shuffle_function(mapped_values)

    # Паралельна Редукція
    with ThreadPoolExecutor() as executor:
        reduced_values = list(executor.map(reduce_function, shuffled_values))

    return dict(reduced_values)

# Функція для візуалізації топ 10 слів
def visualize_top_words(word_counts, top_n=10):
    # Сортуємо слова за частотою
    sorted_word_counts = sorted(word_counts.items(), key=lambda item: item[1], reverse=True)[:top_n]
    
    words, counts = zip(*sorted_word_counts)

    plt.barh(words, counts, color='skyblue')
    plt.xlabel('Frequency')
    plt.ylabel('Words')
    plt.title(f'Top {top_n} Most Frequent Words')
    plt.gca().invert_yaxis()  # Інвертуємо осі для кращої читабельності
    plt.show()

if __name__ == '__main__':
    # Вкажіть URL тексту
    url = "https://www.gutenberg.org/cache/epub/12577/pg12577.txt"
    text = get_text(url)

    if text:
        # Виконуємо MapReduce для підрахунку частот слів
        word_counts = map_reduce(text)

        # Візуалізуємо топ 10 слів
        visualize_top_words(word_counts, top_n=10)
    else:
        print("Помилка: Не вдалося отримати текст із URL.")
