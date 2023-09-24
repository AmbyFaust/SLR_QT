import os
from datetime import datetime

import xlwt
import csv

from project.database import RLIDto, TargetDto
from project.database.database_manager import db_manager
from project.gui.mark_reviewer.ownership_enum import Ownership
from project.singletons import journal


class ReportGenerator:
    def __init__(self, db_file_names, output_dir='xls_csv_report', filename='report'):
        self.output_dir = os.path.abspath(__file__).replace('.py', '_') + output_dir
        self.create_directory()
        self.filename = filename
        self.sessions = []
        self.xls_filenames = []
        self.csv_rli_filenames = []
        self.csv_targets_filenames = []

        for db_file_name in db_file_names:
            session = db_manager.get_session_by_file_name(db_file_name)
            if session:
                self.sessions.append(session)

                self.xls_filenames.append(os.path.join(self.output_dir, db_file_name +
                                                       '_rli_and_targets_' + self.filename + '.xls'))
                self.csv_rli_filenames.append(os.path.join(self.output_dir, db_file_name +
                                                           '_rli_' + self.filename + '.csv'))
                self.csv_targets_filenames.append(os.path.join(self.output_dir, db_file_name +
                                                               '_targets_' + self.filename + '.csv'))
            else:
                journal.log(f'Не удалось получить файл базы данных {db_file_name}', attr='error')

        self.workbooks = [xlwt.Workbook() for _ in range(len(self.sessions))]

        self.center_alignment_style = xlwt.easyxf("align: horiz center, vert center; font: height 220;")
        self.header_row_style = xlwt.easyxf('pattern: pattern solid, fore_colour light_green;'
                                            'font: bold on, height 220;'
                                            'align: horiz center, vert center;')

        self.rli_columns = [
            {'header': 'Идентификатор РЛИ', 'data_func': lambda data: data.id},
            {'header': 'Время локации', 'data_func': lambda data: data.time_location},
            {'header': 'Наименование РЛИ', 'data_func': lambda data: data.name},
            {'header': 'Признак обработки', 'data_func': lambda data: data.is_processing},
            {'header': 'Ширина', 'data_func': lambda data: data.width},
            {'header': 'Высота', 'data_func': lambda data: data.height},
            {'header': 'Расширение', 'data_func': lambda data: data.resolution},
            {'header': 'Наименование типа источника', 'data_func': lambda data: data.raw_rli.type_source_rli.name},
            {'header': 'Наименование файла', 'data_func': lambda data: data.raw_rli.file.name},
            {'header': 'Путь к файлу', 'data_func': lambda data: data.raw_rli.file.path_to_file},
            {'header': 'Расширение файла', 'data_func': lambda data: data.raw_rli.file.file_extension}
        ]

        self.targets_columns = [
            {'header': 'Идентификатор цели', 'data_func': lambda data: data.id},
            {'header': 'Номер цели', 'data_func': lambda data: data.number},
            {'header': 'Координаты (Широта) (WGS-84)', 'data_func': lambda data: data.object.mark.coordinates.latitude},
            {'header': 'Координаты (Долгота) (WGS-84)',
             'data_func': lambda data: data.object.mark.coordinates.longitude},
            {'header': 'Координаты (Высота)', 'data_func': lambda data: data.object.mark.coordinates.altitude},
            {'header': 'Наименование объекта', 'data_func': lambda data: data.object.name},
            {'header': 'Тип объекта', 'data_func': lambda data: data.object.type},
            {'header': 'Принадлежность объекта', 'data_func': lambda data:
                Ownership.int_to_ownership_type(data.object.relating_object_type)},
            {'header': 'Ширина', 'data_func': lambda data: data.raster_rli.rli.width},
            {'header': 'Высота', 'data_func': lambda data: data.raster_rli.rli.height},
            {'header': 'Расширение', 'data_func': lambda data: data.raster_rli.rli.resolution},
            {'header': 'Meta данные', 'data_func': lambda data: data.object.meta},
            {'header': 'Идентификатор РЛИ', 'data_func': lambda data: data.raster_rli.rli.id},
            {'header': 'Время локации', 'data_func': lambda data: data.raster_rli.rli.time_location},
            {'header': 'Наименование РЛИ', 'data_func': lambda data: data.raster_rli.rli.name},
            {'header': 'Признак обработки', 'data_func': lambda data: data.raster_rli.rli.is_processing},
            {'header': 'Тип источника', 'data_func': lambda data:
                data.raster_rli.rli.raw_rli.type_source_rli},
            {'header': 'Наименование файла', 'data_func': lambda data: data.raster_rli.rli.raw_rli.file.name},
            {'header': 'Путь к файлу', 'data_func': lambda data: data.raster_rli.rli.raw_rli.file.path_to_file},
            {'header': 'Расширение файла', 'data_func': lambda data: data.raster_rli.rli.raw_rli.file.file_extension},
            {'header': 'SPPR TYPE KEY', 'data_func': lambda data: data.sppr_type_key}
        ]

        self.generate_xls_rli_report()
        self.generate_xls_targets_report()
        self.generate_csv_rli_report()
        self.generate_csv_targets_report()

    def create_directory(self):
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    @staticmethod
    def set_column_width(worksheet, column_index, value):
        column_width = len(str(value)) * 300
        if worksheet.col(column_index).width < column_width:
            worksheet.col(column_index).width = column_width

    @staticmethod
    def format_bool(value):
        return 'Обработан' if value else 'Не обработан'

    @staticmethod
    def format_datetime(value):
        return value.strftime("%Y-%m-%d %H:%M:%S")

    def write_xls_header_row(self, worksheet, columns):
        for column_index, column_info in enumerate(columns):
            column_name = column_info['header']
            worksheet.write(0, column_index, column_name, self.header_row_style)
            self.set_column_width(worksheet, column_index, column_name)

    def write_xls_data_row(self, worksheet, columns, row_index, data):
        for column_index, column_info in enumerate(columns):
            value = column_info['data_func'](data)
            if isinstance(value, bool):
                value = self.format_bool(value)
            elif isinstance(value, datetime):
                value = self.format_datetime(value)

            worksheet.write(row_index, column_index, value, self.center_alignment_style)
            self.set_column_width(worksheet, column_index, value)

    def generate_xls_rli_report(self):
        for index in range(len(self.sessions)):
            try:
                worksheet = self.workbooks[index].add_sheet('Отчет по РЛИ за сессию')

                list_of_rli = RLIDto.get_all_rli(required_session=self.sessions[index])

                self.write_xls_header_row(worksheet, self.rli_columns)

                for row_index, rli_data in enumerate(list_of_rli):
                    self.write_xls_data_row(worksheet, self.rli_columns, row_index + 1, rli_data)

                self.workbooks[index].save(self.xls_filenames[index])

                journal.log(f'XLS-РЛИ отчет сгенерирован в {self.output_dir}.', attr='warning')

            except BaseException as exp:
                journal.log(f'Не удалось сгенерировать XLS-РЛИ отчет. {exp}', attr='error')

    def generate_xls_targets_report(self):
        for index in range(len(self.sessions)):
            try:
                worksheet = self.workbooks[index].add_sheet('Отчет по целям за сессию')

                list_of_targets = TargetDto.get_all_targets(required_session=self.sessions[index])

                self.write_xls_header_row(worksheet, self.targets_columns)

                for row_index, target_data in enumerate(list_of_targets):
                    self.write_xls_data_row(worksheet, self.targets_columns, row_index + 1, target_data)

                self.workbooks[index].save(self.xls_filenames[index])

                journal.log(f'XLS-ЦЕЛИ отчет сгенерирован в {self.output_dir}.', attr='warning')

            except BaseException as exp:
                journal.log(f'Не удалось сгенерировать XLS-ЦЕЛИ отчет. {exp}', attr='error')

    def write_csv_data(self, columns, data):
        data_row = []

        for column_info in columns:
            value = column_info['data_func'](data)
            if isinstance(value, bool):
                value = self.format_bool(value)
            elif isinstance(value, datetime):
                value = self.format_datetime(value)
            data_row.append(value)

        return data_row

    def generate_csv_rli_report(self):
        for index in range(len(self.sessions)):
            try:
                list_of_rli = RLIDto.get_all_rli(required_session=self.sessions[index])

                with open(self.csv_rli_filenames[index], 'w', newline='') as csv_file:
                    csv_writer = csv.writer(csv_file)

                    header_row = [column_info['header'] for column_info in self.rli_columns]
                    csv_writer.writerow(header_row)

                    for rli_data in list_of_rli:
                        data_row = self.write_csv_data(self.rli_columns, rli_data)
                        csv_writer.writerow(data_row)

                journal.log(f'CSV-РЛИ отчет сгенерирован в {self.csv_rli_filenames[index]}.', attr='warning')

            except BaseException as exp:
                journal.log(f'Не удалось сгенерировать CSV-РЛИ отчет. {exp}', attr='error')

    def generate_csv_targets_report(self):
        for index in range(len(self.sessions)):
            try:
                list_of_targets = TargetDto.get_all_targets(required_session=self.sessions[index])

                with open(self.csv_targets_filenames[index], 'w', newline='') as csv_file:
                    csv_writer = csv.writer(csv_file)

                    header_row = [column_info['header'] for column_info in self.targets_columns]
                    csv_writer.writerow(header_row)

                    for target_data in list_of_targets:
                        data_row = self.write_csv_data(self.targets_columns, target_data)
                        csv_writer.writerow(data_row)

                journal.log(f'CSV-ЦЕЛИ отчет сгенерирован в {self.csv_targets_filenames[index]}.', attr='warning')

            except BaseException as exp:
                journal.log(f'Не удалось сгенерировать CSV-ЦЕЛИ отчет. {exp}', attr='error')
