# -*- coding:utf-8 -*-
from odoo import api, fields, models


class LopLopBaseReport(models.TransientModel):
    _name = 'lop.lop.base.report'
    _description = u'Báo cáo lớp base'

    ma_lop_id = fields.Many2one('lop.lop', 'Lớp')

    @api.multi
    def show_report(self):
        data = {
            'form': {
                'ma_lop_id': self.ma_lop_id.id,
            }
        }
        return self.env.ref('quan_ly_sinh_vien.report_lop_lop_wizard_qweb').report_action(self, data=data)