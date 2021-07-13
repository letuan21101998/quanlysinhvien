# -*- coding: utf-8 -*-

import os
import time
import base64
import tempfile
import xlrd
import calendar
from datetime import datetime, date
from dateutil import relativedelta
from odoo import api, fields, models,
from odoo.exceptions import Warning, ValidationError
from odoo import SUPERUSER_ID
from io import BytesIO
import xlsxwriter

class HocPhi(models.Model):
    _name = 'hoc.phi'
    _inherit = ['mail.thread']
    _description = 'Học Phí'
    _order = 'sv_id'
    _rec_name = 'sv_id'

    is_import = fields.Boolean('Import dữ liệu', states={'confirmed': [('readonly', True)]})
    file_datas = fields.Binary(u'File import', filters="*.xls,*.xlsx")
    file_name = fields.Char(u'Tên file')

    so_tc = fields.Selection(related='nhom_mon_hoc_id.so_tc', string='Số tín chỉ')
    ma_hk = fields.Char(related='hoc_ky_id.ma_hk', string='Mã học kỳ', store=False)
    ho_sv = fields.Char(related='sv_id.ho_sv', string='Họ sinh viên')
    ten_sv = fields.Char(related='sv_id.ten_sv', string='Tên sinh viên')

    sv_id = fields.Many2one('ho.so.sv', 'Sinh viên')
    nhom_mon_hoc_id = fields.Many2one('nhom.mon.hoc', 'Môn học')
    mon_hoc_id = fields.Many2one('mon.hoc', 'Môn học')
    hoc_ky_id = fields.Many2one('hoc.ky', 'Học kỳ')
    hoc_phi = fields.Integer('Học phí', default=0)
    tong_tc = fields.Integer('Tổng số tín chỉ', default=0)

    #
    # _sql_constraints = [
    #     ('ma_sv_uniq', 'unique(ma_sv)', "Mã sinh viên đã tổn tại!")
    # ]
    #

    # def _set_hoc_phi(self):
    #     if self.ma_hk and self.sv_id:
    #         for rec in self.nhom_mon_hoc_id:
    #             self.tong_tc = self.tong_tc + rec.so_tc
    #             self.hoc_phi = 318000 * self.tong_tc
    #     self.write({
    #         'tong_tc': self.tong_tc,
    #         'hoc_phi': self.hoc_phi
    #     })
    #
    # @api.multi
    # def write(self, vals):
    #     res = super(HocPhi, self).write(vals)
    #     if res and 'tong_tc' in vals:
    #         for rec in self:
    #             rec._set_hoc_phi()
    #     return res

    @api.multi
    def import_data_hocphi(self):
        self.is_import = True
        if not self.file_datas:
            raise ValidationError(u'Chưa chọn file import.')
        tmp = self.file_name.split('.')
        if len(tmp) <= 1:
            raise ValidationError(u"Tệp tin tải lên phải là file excel, theo mẫu")
            ext = tmp[len(tmp) - 1]
        if ext != 'xls' and ext != 'xlsx':
            raise ValidationError(u"Tệp tin tải lên phải là định dạng file excel, theo mẫu")
        data = base64.decodestring(self.file_datas)
        fobj = tempfile.NamedTemporaryFile(delete=False)
        fname = fobj.name
        fobj.write(data)
        fobj.close()
        try:
            workbook = xlrd.open_workbook(fname)
            sheet = workbook.sheet_by_index(0)
            self.exec_import(sheet)
            return True
        except Exception as ex:
            if type(ex) == ValidationError:
                raise ValidationError(ex.name)
            else:
                raise ValidationError(ex)

    def exec_import(self, sheet_data):
        if sheet_data.nrows < 5:
            raise ValidationError(u'Không có dữ liệu import!')

        # Lấy danh sách môn học
        self.env.cr.execute('''SELECT ds.* FROM mon_hoc(%s) ;''',
                            (self.mon_hoc_id.id))
        result_query = self.env.cr.dictfetchall()
        arr_ma_mh = []
        for item in result_query:
            arr_ma_mh.append(item['ma_mh'])

        # Lấy dữ liệu từ file import
        ls_data = []
        ls_ma_mh = []
        errors = []
        if sheet_data.nrows <= 4:
            raise ValidationError(u'File import đang không có dữ liệu. Vui lòng kiểm tra lại!')
        for irow in range(4, sheet_data.nrows):
            row_item = sheet_data.row(irow)
            if len(row_item) < 4:
                raise ValidationError(u'File import sai định dạng file mẫu. Vui lòng tải tập tin mẫu để thực hiện!')
            hoc_phi = 0
            dict_error = {
                'row': irow + 1,
                'error_ma_mh': '',
                'error_hoc_phi': ''
            }
            ls_ma_mh.append(str(row_item[1].value).strip())
            # Validate mã môn học
            if not row_item[1].value or str(row_item[1].value).strip() == '':
                dict_error.update({'error_ma_mh': 'Hàng số %s: Mã môn học không được để trống' % (irow + 1,)})
            elif str(row_item[1].value).strip() not in arr_ma_mh:
                dict_error.update({
                                      'error_ma_mh': 'Hàng số %s: Mã môn học %s không tồn tại' % (
                                      irow + 1, str(row_item[1].value).strip())})
            # Validate error_hoc_phi
            hoc_phi = 0
            if self._validate_float_number(row_item[3].value):
                hoc_phi = float(str(row_item[3].value).strip())
            elif row_item[3].value == '':
                hoc_phi = 0
            else:
                dict_error.update({'error_hoc_phi': 'Hàng số %s: Sai định dạng học phí' % (irow + 1,)})
            if hoc_phi < 0:
                dict_error.update({'error_hoc_phi': 'Hàng số %s: Học phải là số dương' % (irow + 1,)})
            errors.append(dict_error)

            if row_item[1].value in arr_ma_mh and arr_ma_mh.index(row_item[1].value) >= 0:
                data = result_query[arr_ma_mh.index(row_item[1].value)]
                ls_data.append({
                    'mon_hoc_id': data['mon_hoc_id'],
                    'ma_mh': data['ma_mh'],
                    # 'ten_mh': data['ten_mh'],
                    'so_tc': data['so_tc'],
                    'hoc_phi': hoc_phi
                })

        str_errors = ''
        for obj in errors:
            if len(obj.get('error_ma_mh')) > 0:
                str_errors += obj.get('error_ma_mh') + '\n'
            if len(obj.get('error_hoc_phi')) > 0:
                str_errors += obj.get('error_hoc_phi') + '\n'
        if str_errors != '':
            raise ValidationError(str_errors)

        # Import data vào table
        self.import_data_to_table(ls_data)

    @api.multi
    def download_template_file(self):
        buf = BytesIO()
        wb = xlsxwriter.Workbook(buf, {'in_memory': True})
        worksheet = wb.add_worksheet()
        style_excel = xlsxwriter_style.get_style(wb)
        # Style
        style_header_table = wb.add_format({
            'pattern': True, 'bg_color': '#95B3D7', 'font_name': 'Times New Roman',
            'font_color': 'black', 'align': 'center', 'font_size': '11',
            'valign': 'vcenter', 'text_wrap': True, 'bold': True,
            'border': True
        })
        style_body_string_content_left = wb.add_format({
            'bold': False, 'font_name': 'Times New Roman',
            'font_color': 'black', 'align': 'left', 'font_size': '11',
            'valign': 'vcenter', 'text_wrap': True,
            'border': True
        })
        style_body_string_content_center = wb.add_format({
            'bold': False, 'font_name': 'Times New Roman',
            'font_color': 'black', 'align': 'center', 'font_size': '11',
            'valign': 'vcenter', 'text_wrap': True,
            'border': True
        })
        style_body_string_content_right = wb.add_format({
            'bold': False, 'font_name': 'Times New Roman',
            'font_color': 'black', 'align': 'right', 'font_size': '11',
            'valign': 'vcenter', 'text_wrap': True,
            'border': True
        })

