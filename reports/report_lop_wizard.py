# -*- coding: utf-8 -*-
from odoo import models, api
import datetime


class report_lop_lop_wizard(models.AbstractModel):
    _name = 'report.quan_ly_sinh_vien.report_lop_wizard'
    _description = u'Báo cáo lớp'

    @api.model
    def _get_report_values(self, docids, data=None):
        now = datetime.datetime.now()
        ma_lop_id = data['form']['ma_lop_id']
        return {
            'doc_ids': docids,
            'ma_lop_id': ma_lop_id,
            'datas': self.get_data(ma_lop_id),
            'profile': self.get_profile(ma_lop_id),
        }

    def get_data(self, ma_lop_id):
        cr = self.env.cr
        res = []
        i = 0
        cr.execute("""
        select ho_sv,ten_sv,ma_sv,ngay_sinh,so_dt  from ho_so_sv where lop_id = %s""", (ma_lop_id,))
        _list = cr.dictfetchall()
        for rec1 in _list:
            i += 1
            item = {
                'stt': i,
                'ho_sv': rec1['ho_sv'],
                'ten_sv': rec1['ten_sv'],
                'ma_sv': rec1['ma_sv'],
                'ngay_sinh': rec1['ngay_sinh'],
                'so_dt': rec1['so_dt'],
            }
            res.append(item)
        return res

    def get_profile(self, ma_lop_id):
        cr = self.env.cr
        cr.execute(""" select ten_lop from lop_lop where id = %s """, (ma_lop_id,))
        _list1 = cr.dictfetchall()
        item = {
            'ten_lop': _list1[0]['ten_lop'],
        }
        return item
