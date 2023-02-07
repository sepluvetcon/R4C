from django.utils.timezone import get_current_timezone
from datetime import datetime, timedelta

from .serializers import RobotSerializer
from robots.models import Robot

import openpyxl
import json
import time
import os


def get_last_week_robots():
	'''
	Функция получает из базы данных queryset роботов произведенных 
	за последнюю неделю и возвращает его.
	'''
	last_week = datetime.now(tz=get_current_timezone()) - timedelta(days=7)
	last_week_robots = Robot.objects.filter(created__gte=last_week)
	return last_week_robots


def get_processed_robots_data():
	'''
	Функция получает queryset роботов произведенных за последнюю 
	неделю от функции get_last_week_robots. Обрабатывает эго, считает 
	количество роботов с одинаковыми моделями, версиями и возвращает 
	в виде словаря.
	'''
	robots_json = RobotSerializer(get_last_week_robots(), many=True).data
	robots_list = []
	for i in range(len(robots_json)):
		robots_list.append(dict(robots_json[i])) 
	processed_robots_data = {}
	for robot in robots_list:
		if robot['model'] not in processed_robots_data:
			processed_robots_data[robot['model']] = {}
		if robot['version'] not in processed_robots_data[robot['model']]:
			processed_robots_data[robot['model']][robot['version']] = {'quantity': 0, 'robots': []}
		processed_robots_data[robot['model']][robot['version']]['robots'].append(robot)
		processed_robots_data[robot['model']][robot['version']]['quantity'] += 1
	return processed_robots_data

# Имя сводки по суммарным показателям производства роботов за последнюю неделю.
filename = 'robots_report.' + time.strftime('%Y.%m.%d') + '.xlsx'


def get_path_to_excel_file():
	'''
	Функция получает словарь роботов произведенных за последнюю 
	неделю от функции get_processed_robots_data, сохраняет их в
	excel файл и возвращает путь к этому файлу.
	'''
	robots = get_processed_robots_data()
	workbook = openpyxl.Workbook()
	workbook.remove(workbook.active)

	for robot_model in robots.keys():
		workbook.create_sheet(robot_model)

	for i in range(len(workbook.worksheets)):
		current_worksheet = workbook.worksheets[i]
		current_worksheet['A1'] = 'Модель'
		current_worksheet['B1'] = 'Версия'
		current_worksheet['C1'] = 'Количество за неделю'
		current_worksheet.column_dimensions['C'].width = 22
		for robot in robots:
			robots_with_same_model = robots[robot]

			for robot_with_same_model in robots_with_same_model:
				robots_with_same_model_and_version = robots_with_same_model[robot_with_same_model]
				robots_quantity = robots_with_same_model_and_version['quantity']
				ready_robots_list = robots_with_same_model_and_version['robots']
				
				for robot in ready_robots_list:
					row = 2
					if current_worksheet.title == robot['model']:
						for current_version in robots_with_same_model.keys():
							current_worksheet[row][0].value = robot['model']
							current_worksheet[row][1].value = current_version
							current_worksheet[row][2].value = robots_with_same_model[current_version]['quantity']
							row += 1

	workbook.save(filename)
	workbook.close()
	path_to_file = os.path.join(os.path.basename(filename))
	return path_to_file
