# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Khoa(models.Model):
    _name = 'khoa.khoa'
    _inherit = ['mail.thread']
    _rec_name = 'ten_khoa'
    _description = 'Khoa'
    _order = 'ma_khoa'

    ten_khoa = fields.Char('Tên khoa', required=True)
    ma_khoa = fields.Char('Mã khoa', required=True)
    ma_lop_ids = fields.One2many('lop.lop', 'khoa_id', 'Tên lớp')

    _sql_constraints = [
        ('ma_khoa_uniq', 'unique (ma_khoa)', "Mã khoa đã tổn tại!"),
        ('ten_khoa_uniq', 'unique (ten_khoa)', "Tên khoa đã tổn tại!")
    ]

    @api.multi
    @api.returns('self', lambda value: value.id)
    def copy(self, default=None):
        self.ensure_one()
        default = dict(default or {})
        default['ma_khoa'] = "%s (Sao chép)" % (self.ma_khoa)
        default['ten_khoa'] = "%s (Sao chép)" % (self.ten_khoa)
        return super(Khoa, self).copy(default)
