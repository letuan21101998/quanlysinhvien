# -*- coding:utf-8 -*-
from odoo import api, fields, models


class BangTotNghiepBaseReport(models.TransientModel):
    _name = 'bang.tot.nghiep.base.report'
    _description = u'Bằng tốt nghiệp base'

    sv_id = fields.Many2one('ho.so.sv', "Mã sinh viên")

    @api.multi
    def show_report(self):
        data = {
            'form': {
                'ten_khoa': self.sv_id.ma_khoa_id.ten_khoa,
                'sv_id': self.sv_id.id,
                'ho_sv': self.sv_id.ho_sv,
                'ten_sv': self.sv_id.ten_sv,
                'name': self.sv_id.ho_sv + ' ' + self.sv_id.ten_sv,
                'ngay_sinh': self.sv_id.ngay_sinh,
                'nam_tot_nghiep': self.sv_id.ngay_tot_nghiep.year,
                'xep_loai': self.sv_id.xep_loai_tn,
                'hinh_thuc_dao_tao': self.sv_id.hinh_thuc_dao_tao,
                'ngay_tot_nghiep': self.sv_id.ngay_tot_nghiep.day,
                'thang_tot_nghiep': self.sv_id.ngay_tot_nghiep.month,
                'namm_tot_nghiep': self.sv_id.ngay_tot_nghiep.year,
            }
        }
        return self.env.ref('quan_ly_sinh_vien.report_bang_tot_nghiep_wizard_qweb').report_action(self, data=data)
