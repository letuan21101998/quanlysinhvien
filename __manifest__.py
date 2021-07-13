# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Student management',
    'version': '1.0',
    'summary': 'Demo for python-odoo class',
    'sequence': 1,
    'description': """

    """,
    'category': 'Accounting',
    'website': 'https://www.odoo.com/page/billing',
    'depends': [
        'base', 'sms'
    ],
    'data': [
        'security/account_security.xml',
        'security/ir.model.access.csv',

        'views/HoSoSV_view.xml',
        'views/BangDiem_view.xml',
        'views/MonHoc_view.xml',
        'views/HocKy_view.xml',
        'views/KhoaHoc_view.xml',
        'views/Lop_view.xml',
        'views/Khoa_view.xml',
        'views/KiLuat_view.xml',
        'views/KhenThuong_view.xml',
        # 'views/HocPhi_view.xml',
        'reports/report_bang_diem_template.xml',
        'reports/report_bang_diem.xml',
        'reports/report_mon_hoc_template.xml',
        'reports/report_mon_hoc.xml',
        'reports/report_lop_template.xml',
        'reports/report_lop.xml',
        'reports/report_bang_tot_nghiep.xml',
        'reports/report_bang_tot_nghiep_template.xml',
        'views/quan_ly_sinh_vien_templates.xml',
        'views/NhomMonHoc_view.xml',
    ],
    'author': 'Minh Tuấn',
    'images': ['static/description/logo.png'],
    'installable': True,
    'application': True,
    'auto_install': False,
}
