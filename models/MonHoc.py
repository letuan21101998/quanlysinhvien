# -*- coding: utf-8 -*-

from odoo import models, fields, api


class MonHoc(models.Model):
    _name = 'mon.hoc'
    _inherit = ['mail.thread']
    _rec_name = 'ten_mh'
    _description = 'Môn học'
    _order = 'ma_mh'

    ma_mh = fields.Char('Mã môn học')
    # ma_hk = fields.Char(related='hoc_ky_id.ma_hk', string='Mã học kỳ', store=False)
    ten_mh = fields.Char('Tên môn học')
    so_tc = fields.Selection([('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'),('5', '5'),('6', '6'), ('7','7')], string='Số tín chỉ')


    # hoc_ky_id = fields.Many2one(comodel_name='hoc.ky', string='Học kỳ')
    # bang_diem_ids = fields.One2many('bang.diem', 'mon_hoc_id', 'Danh sách bảng điểm')

    # bang_diem_id = fields.Many2one('bang.diem', 'Bảng điểm')
    # bang_diem_ids = fields.Many2many(
    #     comodel_name='bang.diem', relation='bangdiem_monmoc_rel',
    #     column1='mon_hoc_id', column2='bang_diem_id', string='Bảng điểm')

    _sql_constraints = [
        ('ten_mh_uniq', 'unique (ten_mh, ma_mh)', "Môn học đã tổn tại!")
    ]

    @api.multi
    @api.returns('self', lambda value: value.id)
    def copy(self, default=None):
        self.ensure_one()
        default = dict(default or {})
        default['ma_hk'] = "%s (Sao chép)" % (self.ma_hk)
        default['ten_mh'] = "%s (Sao chép)" % (self.ten_mh)
        return super(MonHoc, self).copy(default)
