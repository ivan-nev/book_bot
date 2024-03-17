from pprint import pprint
text = 'Да? Вы точно уверены? Может быть, вам это показалось?.., Ну, хорошо, приходите завтра, тогда и посмотрим, что можно сделать. И никаких возражений! Завтра, значит, завтра!'




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


print(*_get_part_text(text, 0, 169), sep='\n')

# Не удаляйте эти объекты - просто используйте
book: dict[int, str] = {}
PAGE_SIZE = 1050


# Дополните эту функцию, согласно условию задачи
def prepare_book(path: str) -> None:
    with open(path, 'r', encoding='utf-8') as f:
        text = f.read().lstrip()
    count = 1
    while text:
        parts, size = _get_part_text(text,0,PAGE_SIZE)
        book[count] = parts.lstrip()
        text = text[size:]
        count += 1
    pprint(book)

prepare_book('book.txt')