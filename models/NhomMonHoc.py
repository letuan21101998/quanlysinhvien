# -*- coding: utf-8 -*-

from odoo import models, fields, api


class NhomMonHoc(models.Model):
    _name = 'nhom.mon.hoc'
    _inherit = ['mail.thread']
    _rec_name = 'nhom_mh'
    _description = 'Nhóm môn học'
    _order = 'nhom_mh'

    nhom_mh = fields.Selection([('01', '01'), ('02', '02')], string='Nhóm môn học')
    ma_mh = fields.Char(related='mon_hoc_id.ma_mh', string='Mã môn học', store=False)
    ma_hk = fields.Char(related='hoc_ky_id.ma_hk', string='Mã học kỳ', store=False)
    so_tc = fields.Selection(related='mon_hoc_id.so_tc', string='Số tín chỉ', store=False)
    # ho_sv = fields.Char(related='sv_id.ho_sv', string='Họ sinh viên', store=False)
    # ten_sv = fields.Char(related='sv_id.ten_sv', string='Tên sinh viên', store=False)
    ten_gv = fields.Char('Tên giáo viên')

    hoc_ky_id = fields.Many2one(comodel_name='hoc.ky', string='Học kỳ')
    mon_hoc_id = fields.Many2one('mon.hoc', 'Môn học')
    bang_diem_ids = fields.One2many('bang.diem', 'nhom_mon_hoc_id', 'Danh sách bảng điểm')
    # hoc_phi_ids = fields.One2many('hoc.phi', 'nhom_mon_hoc_id', 'Danh sách bảng điểm')
    # sv_id = fields.Many2one('ho.so.sv','Mã sinh viên')

    # bang_diem_id = fields.Many2one('bang.diem', 'Bảng điểm')
    # bang_diem_ids = fields.Many2many(
    #     comodel_name='bang.diem', relation='bangdiem_monmoc_rel',
    #     column1='mon_hoc_id', column2='bang_diem_id', string='Bảng điểm')

    # _sql_constraints = [
    #     ('nhom_mh_uniq', 'unique (nhom_mh)', "Nhóm môn học đã tổn tại!")
    # ]

    @api.multi
    @api.returns('self', lambda value: value.id)
    def copy(self, default=None):
        self.ensure_one()
        default = dict(default or {})
        default['nhom_mh'] = "%s (Sao chép)" % (self.nhom_mh)
        return super(NhomMonHoc, self).copy(default)

    def name_get(self):
        res = []
        for order in self:
            name = '%s - %s' % (order.mon_hoc_id.ten_mh, order.nhom_mh)
            res.append((order.id, name))
        return res
