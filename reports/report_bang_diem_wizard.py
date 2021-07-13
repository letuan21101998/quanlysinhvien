# -*- coding: utf-8 -*-
from odoo import models, api
import datetime


class report_bang_diem_wizard(models.AbstractModel):
    _name = 'report.quan_ly_sinh_vien.report_bang_diem_wizard'
    _description = u'Báo cáo bảng điểm'

    @api.model
    def _get_report_values(self, docids, data=None):
        now = datetime.datetime.now()
        sv_id = data['form']['sv_id']
        return {
            'doc_ids': docids,
            'sv_id': sv_id,
            'datas': self.get_data(sv_id),
            'profile': self.get_profile(sv_id),
        }

    def get_data(self, sv_id):
        cr = self.env.cr
        res = []
        i = 0
        cr.execute("""
        select mon_hoc.ten_mh,bang_diem.diem_tp1,bang_diem.diem_tp2,bang_diem.diem_lan1,bang_diem.diem_lan2,bang_diem.diem_thi,bang_diem.diem_tk, bang_diem.diem_chu
        from bang_diem inner join ho_so_sv on bang_diem.sv_id = ho_so_sv.id
				        inner join mon_hoc on bang_diem.mon_hoc_id = mon_hoc.id
		where bang_diem.sv_id = %s""", (sv_id,))
        # cr.execute("""
        #         select nhom_mon_hoc.mon_hoc_id,bang_diem.diem_tp1,bang_diem.diem_tp2,bang_diem.diem_lan1,bang_diem.diem_lan2,bang_diem.diem_thi,bang_diem.diem_tk, bang_diem.diem_chu
        #         from bang_diem inner join ho_so_sv on bang_diem.sv_id = ho_so_sv.id
        #                          inner join nhom_mon_hoc on bang_diem.nhom_mon_hoc_id = nhom_mon_hoc.id
        #                          inner join mon_hoc on bang_diem.mon_hoc_id = mon_hoc.id
        # 		where bang_diem.sv_id = %s""", (sv_id,))
        _list = cr.dictfetchall()
        for rec1 in _list:
            i += 1
            item = {
                'stt': i,
                'ten_mh': rec1['ten_mh'],
                # 'ten_mh': rec1['mon_hoc_id'],
                'diem_tp1': rec1['diem_tp1'],
                'diem_tp2': rec1['diem_tp2'],
                'diem_lan1': rec1['diem_lan1'],
                'diem_lan2': rec1['diem_lan2'],
                'diem_thi': rec1['diem_thi'],
                'diem_tk': rec1['diem_tk'],
                'diem_chu': rec1['diem_chu'],
            }
            res.append(item)
        return res

    def get_profile(self, sv_id):
        cr = self.env.cr
        cr.execute("""
        select ho_sv, ten_sv, ma_sv from ho_so_sv where id = %s """, (sv_id,))
        _list1 = cr.dictfetchall()
        item = {
            'ho_sv': _list1[0]['ho_sv'],
            'ten_sv': _list1[0]['ten_sv'],
            'ma_sv': _list1[0]['ma_sv'],
        }
        return item
