import os
import sys
from pprint import pprint

BOOK_PATH = 'book/book.txt'
PAGE_SIZE = 1050

book: dict[int, str] = {}


# Функция, возвращающая строку с текстом страницы и ее размер
def _get_part_text(text: str, start: int, page_size: int) -> tuple[str, int]:
    symbol = '?.,!:;'
    text2 = text[start:start + page_size]
    if start+page_size > len(text):
        return text, len(text)
    if start + page_size < len(text):
        if text[start + page_size] in symbol:
            while text2[-1] in symbol:
                text2 = text2[:-1]
    while text2[-1] not in symbol:
        text2 = text2[:-1]
    return text2, len(text2)


# Функция, формирующая словарь книги
def prepare_book(path: str) -> None:
    with open(path, 'r', encoding='utf-8') as f:
        text = f.read().lstrip()
    count = 1
    while text:
        parts, size = _get_part_text(text, 0, PAGE_SIZE)
        book[count] = parts.lstrip()
        text = text[size:]
        count += 1


# Вызов функции prepare_book для подготовки книги из текстового файла
prepare_book(os.path.join(sys.path[0], os.path.normpath(BOOK_PATH)))
