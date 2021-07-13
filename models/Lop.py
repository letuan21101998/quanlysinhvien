# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Lop(models.Model):
    _name = 'lop.lop'
    _inherit = ['mail.thread']
    _rec_name = 'ten_lop'
    _description = 'Lớp'
    _order = 'ma_lop'

    ten_lop = fields.Char('Tên lớp', required=True)
    ma_lop = fields.Char('Mã lớp', required=True)
    ma_khoa = fields.Char(related='khoa_id.ma_khoa', string='Mã khoa', store=False)

    khoa_id = fields.Many2one('khoa.khoa', 'Khoa', required=True)
    ma_lop_ids = fields.One2many('ho.so.sv', 'lop_id', 'Lớp')

    _sql_constraints = [
        ('ma_lop_uniq', 'unique (ma_lop)', "Mã lớp đã tổn tại!")
    ]

    @api.multi
    @api.returns('self', lambda value: value.id)
    def copy(self, default=None):
        self.ensure_one()
        default = dict(default or {})
        default['ma_lop'] = "%s (Sao chép)" % (self.ma_lop)
        default['ten_lop'] = "%s (Sao chép)" % (self.ten_lop)
        return super(Lop, self).copy(default)
