# -*- coding: utf-8 -*-
from odoo import models, api
import datetime


class report_mon_hoc_wizard(models.AbstractModel):
    _name = 'report.quan_ly_sinh_vien.report_mon_hoc_wizard'
    _description = u'Báo cáo môn học'

    @api.model
    def _get_report_values(self, docids, data=None):
        now = datetime.datetime.now()
        mon_hoc_id = data['form']['mon_hoc_id']
        name = data['form']['name']
        return {
            'doc_ids': docids,
            'mon_hoc_id': mon_hoc_id,
            'name': name,
            'datas': self.get_data(mon_hoc_id),
            # 'profile': self.get_profile(mon_hoc_id),
        }

    def get_data(self, mon_hoc_id):
        cr = self.env.cr
        res = []
        i = 0
        cr.execute("""
        select ho_so_sv.ho_sv,ho_so_sv.ten_sv,ho_so_sv.ma_sv,bang_diem.diem_tp1,bang_diem.diem_tp2,bang_diem.diem_lan1,bang_diem.diem_lan2,bang_diem.diem_thi,bang_diem.diem_tk
        from bang_diem inner join ho_so_sv on bang_diem.sv_id = ho_so_sv.id
				        inner join nhom_mon_hoc on bang_diem.nhom_mon_hoc_id = nhom_mon_hoc.id
        where bang_diem.nhom_mon_hoc_id = %s
        order by ho_so_sv.ten_sv""", (mon_hoc_id,))
        _list = cr.dictfetchall()
        for rec1 in _list:
            i += 1
            item = {
                'stt': i,
                'ho_sv': rec1['ho_sv'],
                'ten_sv': rec1['ten_sv'],
                'ma_sv': rec1['ma_sv'],
                'diem_tp1': rec1['diem_tp1'],
                'diem_tp2': rec1['diem_tp2'],
                'diem_lan1': rec1['diem_lan1'],
                'diem_lan2': rec1['diem_lan2'],
                'diem_thi': rec1['diem_thi'],
                'diem_tk': rec1['diem_tk'],
            }
            res.append(item)
        return res

    # def get_profile(self, mon_hoc_id):
    #     cr = self.env.cr
    #     cr.execute(""" select mon_hoc.ten_mh from dang_ky_mon_hoc where id = %s """, (mon_hoc_id,))
    #     _list1 = cr.dictfetchall()
    #     item = {
    #         'ten_mh': _list1[0]['mon_hoc_id'],
    #     }
    #     return item
