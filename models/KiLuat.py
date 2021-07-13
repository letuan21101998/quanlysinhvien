# -*- coding: utf-8 -*-

from odoo import models, fields, api


class KiLuat(models.Model):
    _name = 'ki.luat'
    _inherit = ['mail.thread']
    _rec_name = 'sv_id'
    _description = 'Thông tin kỉ luật'
    _order = 'sv_id, ngay_kl'

    sv_id = fields.Many2one('ho.so.sv', 'Sinh viên')
    loi_vi_pham = fields.Char(string='Lỗi vi phạm')
    ngay_kl = fields.Date(string='Ngày kỉ luật')
    hinh_thuc_kl = fields.Selection([('canhcao', 'Cảnh cáo'), ('dinhchi', 'Đình chỉ'), ('buocthoihoc', 'Buộc thôi học')], string='Hình thức kỉ luật')
    so_lan_kl = fields.Selection([('1', '1'), ('2', '2'), ('3', '3')], string='Số lần kỉ luật')
    ghi_chu = fields.Text(string='Ghi chú')
    ho_sv = fields.Char(related='sv_id.ho_sv', string='Họ sinh viên', store=False)
    ten_sv = fields.Char(related='sv_id.ten_sv', string='Tên sinh viên', store=False)
