import logging
from fuzzywuzzy import fuzz, process
import logging
import time

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='levenshtein.log',
    filemode='w',
    encoding='utf-8'
)

def levenstein(str_1, str_2):
    n, m = len(str_1), len(str_2)
    if n > m:
        str_1, str_2 = str_2, str_1
        n, m = m, n

    current_row = range(n + 1)
    for i in range(1, m + 1):
        previous_row, current_row = current_row, [i] + [0] * n
        for j in range(1, n + 1):
            add, delete, change = previous_row[j] + 1, current_row[j - 1] + 1, previous_row[j - 1]
            if str_1[j - 1] != str_2[i - 1]:
                change += 1
            current_row[j] = min(add, delete, change)

    return current_row[n]

str_1 = input()
str_2 = input()

result = levenstein(str_1, str_2)
logging.info(f"Расстояние Левенштейна между '{str_1}' и '{str_2}': {result}")
print(f'как далеки {str_1} и {str_2}?', result)



# fuzz_examples.py

# Простое сравнение
start = time.time()
a = fuzz.ratio('Привет мир', 'Привет мир')
end = time.time()
logging.info(f"fuzz.ratio (одинаковые): {a}, время: {(end-start)*1000:.2f}мс")
print(a)

start = time.time()
a = fuzz.ratio('Привет мир', 'Привет мир')
end = time.time()
logging.info(f"fuzz.ratio (с кавычками): {a}, время: {(end-start)*1000:.2f}мс")
print(a)

# частичное сравнение
start = time.time()
a = fuzz.partial_ratio('Привет мир', 'Привет мир')
end = time.time()
logging.info(f"fuzz.partial_ratio (одинаковые): {a}, время: {(end-start)*1000:.2f}мс")
print(a)

start = time.time()
a = fuzz.partial_ratio('Привет мир',  'Люблю колбасу, Привет мир')
end = time.time()
logging.info(f"fuzz.partial_ratio (подстрока): {a}, время: {(end-start)*1000:.2f}мс")
print(a)

start = time.time()
a = fuzz.partial_ratio('Привет мир', 'Люблю колбасу, привет мир')
end = time.time()
logging.info(f"fuzz.partial_ratio (регистр): {a}, время: {(end-start)*1000:.2f}мс")
print(a)

# сравнение по токену
start = time.time()
a = fuzz.token_sort_ratio('Привет наш мир',  'мир наш Привет')
end = time.time()
logging.info(f"fuzz.token_sort_ratio (перестановка): {a}, время: {(end-start)*1000:.2f}мс")
print(a)

start = time.time()
a = fuzz.token_sort_ratio('Привет наш мир', 'мир наш любимый Привет')
end = time.time()
logging.info(f"fuzz.token_sort_ratio (лишнее слово): {a}, время: {(end-start)*1000:.2f}мс")
print(a)

start = time.time()
a = fuzz.token_sort_ratio('1 2 Привет наш мир', '1 мир наш 2 Привет')
end = time.time()
logging.info(f"fuzz.token_sort_ratio (с числами): {a}, время: {(end-start)*1000:.2f}мс")
print(a)

# Token Set Ratio
start = time.time()
a = fuzz.token_set_ratio('Привет наш мир',  'мир мир наш наш наш Привет')
end = time.time()
logging.info(f"fuzz.token_set_ratio (повторы): {a}, время: {(end-start)*1000:.2f}мс")
print(a)

# продвинутое обычное сравнение
start = time.time()
a = fuzz.WRatio( 'Привет наш мир', '!ПриВЕТ наш мир!')
end = time.time()
logging.info(f"fuzz.WRatio (знаки препинания): {a}, время: {(end-start)*1000:.2f}мс")
print(a)

start = time.time()
a = fuzz.WRatio('Привет наш мир', '!ПриВЕТ, наш мир!')
end = time.time()
logging.info(f"fuzz.WRatio (запятая): {a}, время: {(end-start)*1000:.2f}мс")
print(a)

# работа со списком
city = ['Москва', 'Санкт-Петербург', 'Саратов', 'Краснодар', 'Воронеж', 'Омск', 'Екатеринбург', 'Омск', 'Красногорск', 'Красногорск', 'Самара']
start = time.time()
a = process.extract('Саратов', city, limit=2)
end = time.time()
logging.info(f"process.extract (Саратов): {a}, время: {(end-start)*1000:.2f}мс")
print(a)

doc1 = open("namesosat")
lines1 = doc1.readlines()
doc2 = open("namerec")
lines2 = doc2.readlines()
files = [doc1, doc2]

start = time.time()
a = process.extract("fjasekdn", lines1)
end = time.time()
logging.info(f"process.extract в namesosat: {a}, время: {(end-start)*1000:.2f}мс")

start = time.time()
b = process.extract("fjasekdn", lines2)
end = time.time()
logging.info(f"process.extract в namerec: {b}, время: {(end-start)*1000:.2f}мс")

print(a)
print(b)