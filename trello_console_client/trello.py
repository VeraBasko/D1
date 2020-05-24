import sys
import requests

BASE_URL = "https://api.trello.com/1/{}"
AUTH_PARAMS = {
    'key': "086deb0eff8e250ae07ad03608b913aa",
    'token': "38365a62229a222b0a0baba22b66b08d867ee4296c2c3c2a992467ab09e69602", }
BOARD_ID = "Ww5hFPbt"


def read():
    # Получим данные всех колонок на доске:
    column_data = requests.get(BASE_URL.format('boards') + '/' + BOARD_ID + '/lists', params=AUTH_PARAMS).json()

    # Теперь выведем название каждой колонки и всех заданий, которые к ней относятся:
    for column in column_data:
        print(column['name'])
        # Получим данные всех задач в колонке и перечислим все названия
        task_data = requests.get(BASE_URL.format('lists') + '/' + column['id'] + '/cards', params=AUTH_PARAMS).json()
        if not task_data:
            print('\t' + 'Нет задач!')
            continue
        for task in task_data:
            print('\t' + task['name'])


def create(name, column_name):
    # Получим данные всех колонок на доске
    column_data = requests.get(BASE_URL.format('boards') + '/' + BOARD_ID + '/lists', params=AUTH_PARAMS).json()

    # Переберём данные обо всех колонках, пока не найдём ту колонку, которая нам нужна
    for column in column_data:
        if column['name'] == column_name:
            # Создадим задачу с именем _name_ в найденной колонке
            requests.post(BASE_URL.format('cards'), data={'name': name, 'idList': column['id'], **AUTH_PARAMS})
            break


def move(name, column_name):
    # Получим данные всех колонок на доске
    column_data = requests.get(BASE_URL.format('boards') + '/' + BOARD_ID + '/lists', params=AUTH_PARAMS).json()

    # Среди всех колонок нужно найти задачу по имени и получить её id
    task_id = None
    for column in column_data:
        column_tasks = requests.get(BASE_URL.format('lists') + '/' + column['id'] + '/cards', params=AUTH_PARAMS).json()
        for task in column_tasks:
            if task['name'] == name:
                task_id = task['id']
                break
        if task_id:
            break

            # Теперь, когда у нас есть id задачи, которую мы хотим переместить
    # Переберём данные обо всех колонках, пока не найдём ту, в которую мы будем перемещать задачу
    for column in column_data:
        if column['name'] == column_name:
            # И выполним запрос к API для перемещения задачи в нужную колонку
            requests.put(BASE_URL.format('cards') + '/' + task_id + '/idList',
                         data={'value': column['id'], **AUTH_PARAMS})
            break


if __name__ == "__main__":
    if len(sys.argv) <= 2:
        read()
    elif sys.argv[1] == 'create':
        create(sys.argv[2], sys.argv[3])
    elif sys.argv[1] == 'move':
        move(sys.argv[2], sys.argv[3])