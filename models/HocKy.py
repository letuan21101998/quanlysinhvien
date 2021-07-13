# -*- coding: utf-8 -*-

from odoo import models, fields, api


class HocKy(models.Model):
    _name = 'hoc.ky'
    _inherit = ['mail.thread']
    _rec_name = 'ten_hk'
    _description = 'Học kỳ'
    _order = 'ma_hk'

    ma_hk = fields.Char('Mã học kỳ', required=True)
    ten_hk = fields.Char(string='Tên học kỳ')
    nam_hoc = fields.Char(string='Năm học')

    _sql_constraints = [
        ('ma_hk_uniq', 'unique (ma_hk)', "Mã học kỳ đã tổn tại!")
    ]

    @api.multi
    @api.returns('self', lambda value: value.id)
    def copy(self, default=None):
        self.ensure_one()
        default = dict(default or {})
        default['ma_hk'] = "%s (Sao chép)" % (self.ma_hk)
        return super(HocKy, self).copy(default)

    def name_get(self):
        res = []
        for order in self:
            name = '%s  %s' % (order.ten_hk, order.nam_hoc)
            res.append((order.id, name))
        return res
