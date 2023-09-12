# Напишите функцию, которая получает на вход директорию и рекурсивно обходит её и все вложенные директории.
# Результаты обхода сохраните в файлы json, csv и pickle.
# ○ Для дочерних объектов указывайте родительскую директорию.
# ○ Для каждого объекта укажите файл это или директория.
# ○ Для файлов сохраните его размер в байтах, а для директорий размер файлов в ней с учётом всех вложенных файлов и
# директорий.
import csv
import json
import os
import pickle

dir_info = {}
dir_p = None


def calculate_dir_size():
    global dir_info
    global dir_p

    folders = [[k, v[0], v[1], v[2]] for k, v in dir_info.items()]

    while True:
        # for f in folders:
        #     if f[1] == 'dir':
        #         print(f"{f = }")
        if all([obj[1] in ('file', '-') for obj in folders]):
            break
        for i in range(len(folders)):
            # перебираю папки
            name, f_d, par_dir, size = folders[i]
            if f_d == 'dir':
                # создаю список в котором буду сохранять результаты проверок входящих объектов
                c_dir = [True]
                for line in folders:
                    if line[2] == name:
                        c_dir.append(line[1] in ('file', '-'))
                #   если все входящие объекты оказались файлами, то я добавляю  их размер к размеру род. папки
                if all(c_dir):
                    for item in folders:
                        if item[2] == name:
                            print(f'was-{folders[i] =}, {folders[i][3] =}')
                            file_size = item[3]
                            folders[i][3] += file_size
                            print(f'is -{folders[i] =}, {folders[i][3] =}')

            # меняю в исходном словаре размер директории на полученный и присваиваю этой директории тип файла, чтобы ее
            # размер м б учитывать в родительских папках
            dir_info[name][2] = folders[i][3]
            folders[i][1] = '-'



def describe_dir(path):
    global dir_info
    global dir_p
    global current_working_folder

    os.chdir(path)
    objects_list = ['object_name', 'parents_dir', 'file/dir', 'size']
    for dir_path, dir_name, file_name in os.walk(path):
        dir_p = path.rsplit('/')[-1]
        for file in file_name:
            dir_info[file] = ["file", dir_path.rsplit('/')[-1], file.__sizeof__()]
        for folder in dir_name:
            dir_info[folder] = ["dir", dir_path.rsplit('/')[-1], folder.__sizeof__()]
    print(f'{dir_info = }')
    calculate_dir_size()
    print(f'{dir_info = }')

    # в файлы json,
    os.chdir(os.getcwd())
    dir_info_for_csv = [[k, v[0], v[1], v[2]] for k, v in dir_info.items()]
    dir_info_for_csv = [objects_list] + dir_info_for_csv

    with (open(os.path.join(current_working_folder, 'dir_and_files.json'), 'w', encoding='utf-8') as f_json,
          open(os.path.join(current_working_folder, 'dir_and_files.csv'), 'w', encoding='utf-8') as f_csv,
          open(os.path.join(current_working_folder, 'dir_and_files.pickle'), 'wb') as f_pickle
          ):
        json.dump(dir_info, f_json, indent=4)

        csv_write = csv.writer(f_csv, dialect='excel-tab', delimiter='\t', quoting=csv.QUOTE_MINIMAL)
        csv_write.writerows(dir_info_for_csv)

        pickle.dump(dir_info, f_pickle)


# describe_dir(os.path.join(os.getcwd(), '..', 'seminar8'))
current_working_folder = "/Users/anastasiabuglakova/Documents/GEEK/Погружение в Python/hw8"
describe_dir("/Users/anastasiabuglakova/Documents/GEEK/Диплом")
# Соберите из созданных на уроке и в рамках домашнего задания функций пакет для работы с файлами разных форматов.
