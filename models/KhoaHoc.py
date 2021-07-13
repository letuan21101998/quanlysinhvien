# -*- coding: utf-8 -*-

from odoo import models, fields, api


class KhoaHoc(models.Model):
    _name = 'khoa.hoc'
    _inherit = ['mail.thread']
    _rec_name = 'ten_kh'
    _description = 'Khóa học'
    _order = 'ma_kh'

    ma_kh = fields.Char('Mã khóa học', required=True)
    ten_kh = fields.Char('Tên khóa học', required=True)
    nam_hoc = fields.Char('Năm học')

    _sql_constraints = [
        ('ma_kh_uniq', 'unique (ma_kh)', "Mã khóa học đã tổn tại!"),
        ('ten_kh_uniq', 'unique (ten_kh)', "Tên khóa học đã tổn tại!")
    ]

    @api.multi
    @api.returns('self', lambda value: value.id)
    def copy(self, default=None):
        self.ensure_one()
        default = dict(default or {})
        default['ma_kh'] = "%s (Sao chép)" % (self.ma_kh)
        default['ten_kh'] = "%s (Sao chép)" % (self.ten_kh)
        return super(KhoaHoc, self).copy(default)
