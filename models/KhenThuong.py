# -*- coding: utf-8 -*-

from odoo import models, fields, api


class KhenThuong(models.Model):
    _name = 'khen.thuong'
    _inherit = ['mail.thread']
    _rec_name = 'sv_id'
    _description = 'Thành tích khen thưởng'
    _order = 'sv_id, ngay_kt'

    sv_id = fields.Many2one('ho.so.sv', 'Sinh viên')
    thanh_tich = fields.Char(string='Thành tích')
    ngay_kt = fields.Date(string='Ngày khen thưởng')
    hinh_thuc_kt = fields.Selection(
        [('tuyenduong', 'Tuyên dương'), ('huanchuong', 'Huân Chương'), ('bangkhen', 'Bằng khen')], string ='Hình thức khen thưởng')
    danh_muc_kt = fields.Selection([('ttt', 'Thành tích tốt'), ('ntvt', 'Người tốt việc tốt'), ('khac', 'Khác')], string='Danh mục khen thưởng')
    ghi_chu = fields.Text(string='Ghi chú')
    ho_sv = fields.Char(related='sv_id.ho_sv', string='Họ sinh viên', store=False)
    ten_sv = fields.Char(related='sv_id.ten_sv', string='Tên sinh viên', store=False)
