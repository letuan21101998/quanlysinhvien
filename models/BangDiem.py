# -*- coding: utf-8 -*-

from odoo import models, fields, api


class BangDiem(models.Model):
    _name = 'bang.diem'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'nhom_mon_hoc_id'
    _description = 'Bảng điểm'
    _order = 'sv_id'

    sv_id = fields.Many2one('ho.so.sv', 'Mã sinh viên')
    ma_sv = fields.Char(related='sv_id.ma_sv', string='Mã sinh viên')
    so_tc = fields.Selection(related='nhom_mon_hoc_id.mon_hoc_id.so_tc', string='Số tín chỉ', store=False)
    ho_sv = fields.Char(related='sv_id.ho_sv', string='Họ sinh viên')
    ten_sv = fields.Char(related='sv_id.ten_sv', string='Tên sinh viên')
    ten_mh = fields.Char(related='nhom_mon_hoc_id.mon_hoc_id.ten_mh', string='Tên môn học', store=False)
    # ma_mh = fields.Char(related='mon_hoc_id.ma_mh', string='Mã môn học')
    # ten_mh = fields.Char(related='mon_hoc_id.ten_mh', string='Tên môn học')
    # ma_lop_mh = fields.Selection([('01', '01'), ('02', '02')], string='Mã lớp môn học')
    diem_lan1 = fields.Float('Điểm thi lần 1', required=True, track_visibility='always')
    diem_lan2 = fields.Float('Điểm thi lần 2', required=True, track_visibility='always')
    diem_thi = fields.Float('Điểm thi')
    diem_tk = fields.Float('Điểm tổng kết')
    diem_tp1 = fields.Float('Điểm thành phần 1', required=True, track_visibility='always')
    diem_tp2 = fields.Float('Điểm thành phần 2', required=True, track_visibility='always')
    diem_chu = fields.Char('Điểm chữ', required=True)

    mon_hoc_id = fields.Many2one('mon.hoc', 'Môn học')
    nhom_mon_hoc_id = fields.Many2one('nhom.mon.hoc', 'Nhóm môn học')

    # mon_hoc_ids = fields.Many2many(
    #     comodel_name='mon.hoc', relation='bangdiem_monhoc_rel',
    #     column1='bang_diem_id', column2='môn_học_id', string='Môn học')

    # _sql_constraints = [
    #     ('ma_mh_uniq', 'unique (ma_mh)', "Mã môn học đã tổn tại!")
    #     ('ma_lop_mh_uniq', 'unique (ma_lop_mh)', "Mã lớp môn học đã tổn tại!")
    # ]

    # @api.multi
    # @api.returns('self', lambda value: value.id)
    # def copy(self, default=None):
    #     self.ensure_one()
    #     default = dict(default or {})
    #     default['ma_lop_mh'] = "%s (Sao chép)" % (self.ma_lop_mh)
    #     return super(BangDiem, self).copy(default)

    @api.onchange('diem_lan1', 'diem_lan2')
    def onchange_diem_thi(self):
        if self.diem_lan1 >= self.diem_lan2:
            self.diem_thi = self.diem_lan1
        else:
            self.diem_thi = self.diem_lan2

    @api.onchange('diem_tp1', 'diem_tp2', 'diem_thi')
    def _onchange_diem_tk(self):
        if self.diem_thi and self.diem_tp1 and self.diem_tp2:
            self.diem_tk = 0.1 * (self.diem_tp1) + 0.3 * (self.diem_tp2) + 0.6 * (self.diem_thi)

    @api.onchange('diem_tk')
    def _onchange_diem_chu(self):
        if 8.5 <= self.diem_tk <=10:
            self.diem_chu = str('A')
        elif 8.0 <= self.diem_tk <= 8.4:
            self.diem_chu = str('B+')
        elif 7.0 <= self.diem_tk <= 7.9:
            self.diem_chu = str('B')
        elif 6.5 <= self.diem_tk <= 6.9:
            self.diem_chu = str('C+')
        elif 5.5 <= self.diem_tk <= 6.4:
            self.diem_chu = str('C')
        elif 5.0 <= self.diem_tk <= 5.4:
            self.diem_chu = str('D+')
        elif 4.0 <= self.diem_tk <= 4.9:
            self.diem_chu = str('D')
        else:
            self.diem_chu = str('F')

    @api.multi
    def write(self, vals):
        res = super(BangDiem, self).write(vals)
        if res and 'diem_tk' in vals:
            for rec in self:
                rec.sv_id.get_diem_tk(rec.sv_id.id)
        return res
