# -*- coding: utf-8 -*-
from odoo import models, api
import datetime


class report_bang_tot_nghiep_wizard(models.AbstractModel):
    _name = 'report.quan_ly_sinh_vien.report_bang_tot_nghiep_wizard'
    _description = u'Báo cáo bằng tốt nghiệp'

    @api.model
    def _get_report_values(self, docids, data=None):
        now = datetime.datetime.now()
        ten_khoa = data['form']['ten_khoa']
        sv_id = data['form']['sv_id']
        name = data['form']['name']
        ngay_sinh = data['form']['ngay_sinh']
        nam_tot_nghiep = data['form']['nam_tot_nghiep']
        xep_loai = data['form']['xep_loai']
        hinh_thuc_dao_tao = data['form']['hinh_thuc_dao_tao']
        ngay_tot_nghiep = data['form']['ngay_tot_nghiep']
        thang_tot_nghiep = data['form']['thang_tot_nghiep']
        namm_tot_nghiep = data['form']['namm_tot_nghiep']
        return {
            'doc_ids': docids,
            'ten_khoa': ten_khoa,
            'sv_id': sv_id,
            'name': name,
            'ngay_sinh': ngay_sinh,
            'nam_tot_nghiep': nam_tot_nghiep,
            'xep_loai': xep_loai,
            'hinh_thuc_dao_tao': hinh_thuc_dao_tao,
            'ngay_tot_nghiep': ngay_tot_nghiep,
            'thang_tot_nghiep': thang_tot_nghiep,
            'namm_tot_nghiep': namm_tot_nghiep,
        }
