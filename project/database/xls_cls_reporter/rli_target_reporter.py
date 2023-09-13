import os
import xlwt

from project.database.session_controller.session_controller import session_controller


class ReportGenerator:
    def __init__(self, output_dir='xls_report', filename='report'):
        self.output_dir = output_dir
        self.session = session_controller.get_session()
        self.filename = filename
        self.file_extensions = ['.xls', '.cls']
        self.create_directory()
        self.file_paths = [os.path.join(self.output_dir, self.filename + file_extension)
                           for file_extension in self.file_extensions]

        self.workbook = xlwt.Workbook()

        self.center_alignment_style = xlwt.easyxf("align: horiz center, vert center; font: height 220;")
        self.header_row_style = xlwt.easyxf('pattern: pattern solid, fore_colour light_green;'
                                            'font: bold on, height 220;'
                                            'align: horiz center, vert center;')

        self.rli_columns = [
            {'header': 'Индентификатор РЛИ', 'data_func': lambda data: data.id},
            {'header': 'Сессия', 'data_func': self.session.},
            {'header': 'Идентификатор файла', 'data_func': lambda data: data.file_id},
            {'header': 'Наименование файла', 'data_func': lambda data: session.query(FileEntity).
                get(data.file_id).name},
            {'header': 'Путь к файлу', 'data_func': lambda data: session.query(FileEntity).
                get(data.file_id).path_to_file},
            {'header': 'Расширение файла', 'data_func': lambda data: session.query(FileEntity).
                get(data.file_id).file_extension},
            {'header': 'Идентификатор типа источника', 'data_func': lambda data: data.type_source_rli_id},
            {'header': 'Наименование типа источника', 'data_func': lambda data: session.query(TypeSourceRLIEntity).
                get(data.type_source_rli_id).name},
            {'header': 'Дата и время получения', 'data_func': lambda data: data.date_receiving}
        ]

        self.targets_columns = [
            {'header': 'Идентификатор цели', 'data_func': lambda data: data.id},
            {'header': 'Идентификатор сессии', 'data_func': lambda data: self.session_id},
            {'header': 'Номер цели', 'data_func': lambda data: data.number},
            {'header': 'Идентификатор объекта', 'data_func': lambda data: data.object_id},
            {'header': 'Идентификатор Отметки', 'data_func': lambda data: session.query(ObjectEntity).
                get(data.object_id).mark_id},
            {'header': 'Наименование объекта', 'data_func': lambda data: session.query(ObjectEntity).
                get(data.object_id).name},
            {'header': 'Тип объекта', 'data_func': lambda data: session.query(ObjectEntity).
                get(data.object_id).type},
            {'header': 'Принадлежность объекта (идентификатор)', 'data_func': lambda data: session.query(ObjectEntity).
                get(data.object_id).relating_object_id},
            {'header': 'Meta данные', 'data_func': lambda data: session.query(ObjectEntity).
                get(data.object_id).meta},
            {'header': 'Идентификатор РЛИ', 'data_func': lambda data: session.query(RLIEntity).
                get(session.query(RasterRLIEntity).get(data.raster_rli_id).rli_id).id},
            {'header': 'Время локации', 'data_func': lambda data: session.query(RLIEntity).
                get(session.query(RasterRLIEntity).get(data.raster_rli_id).rli_id).time_location},
            {'header': 'Наименование РЛИ', 'data_func': lambda data: session.query(RLIEntity).
                get(session.query(RasterRLIEntity).get(data.raster_rli_id).rli_id).name},
            {'header': 'Признак обработки', 'data_func': lambda data: session.query(RLIEntity).
                get(session.query(RasterRLIEntity).get(data.raster_rli_id).rli_id).is_processing},
            {'header': 'Идентификатор сырого РЛИ', 'data_func': lambda data: session.query(RLIEntity).
                get(session.query(RasterRLIEntity).get(data.raster_rli_id).rli_id).raw_rli_id},
            {'header': 'Дата и время отправки', 'data_func': lambda data: data.datetime_sending},
            {'header': 'SPPR TYPE KEY', 'data_func': lambda data: data.sppr_type_key}
        ]

        self.generate_xls_report_raw_rli()
        self.generate_xls_report_targets()

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

    def generate_xls_report_raw_rli(self):
        worksheet = self.workbook.add_sheet('Отчет по сырому РЛИ за сессию')

        list_of_raw_rli = self.get_raw_rli_data()

        self.write_header_row(worksheet, self.rli_columns)

        for row_index, raw_rli_data in enumerate(list_of_raw_rli):
            self.write_data_rli_row(worksheet, row_index + 1, raw_rli_data)

        self.workbook.save(self.file_path)
        print('XLS report generated at {}'.format(self.file_path))

    def get_raw_rli_data(self):
        ids_of_files_with_session_id = [
            x.id for x in session.query(FileEntity).filter_by(session_id=self.session_id).all()
        ]

        return session.query(RawRLIEntity).filter(RawRLIEntity.file_id.in_(ids_of_files_with_session_id)).all()

    def write_header_row(self, worksheet, columns):
        for column_index, column_info in enumerate(columns):
            column_name = column_info['header']
            worksheet.write(0, column_index, column_name, self.header_row_style)
            self.set_column_width(worksheet, column_index, column_name)

    def write_data_rli_row(self, worksheet, row_index, raw_rli_data):
        for column_index, column_info in enumerate(self.rli_columns):
            value = column_info['data_func'](raw_rli_data)
            if isinstance(value, datetime):
                value = self.format_datetime(value)
            worksheet.write(row_index, column_index, value, self.center_alignment_style)
            self.set_column_width(worksheet, column_index, value)

    def generate_xls_report_targets(self):
        worksheet = self.workbook.add_sheet('Отчет по целям за сессию')

        list_of_targets = TargetEntity.get_targets_by_session_id(self.session_id)

        self.write_header_row(worksheet, self.targets_columns)

        for row_index, target_data in enumerate(list_of_targets):
            self.write_data_target_row(worksheet, row_index + 1, target_data)

        self.workbook.save(self.file_path)
        print('XLS report generated at {}'.format(self.file_path))

    def write_data_target_row(self, worksheet, row_index, target_data):
        for column_index, column_info in enumerate(self.targets_columns):
            value = column_info['data_func'](target_data)
            if isinstance(value, bool):
                value = self.format_bool(value)
            elif isinstance(value, datetime):
                value = self.format_datetime(value)

            worksheet.write(row_index, column_index, value, self.center_alignment_style)
            self.set_column_width(worksheet, column_index, value)