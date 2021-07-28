# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
{
    "name": "EnterpriseMate Backend Theme",
    "author" : "Softhealer Technologies",
    "website": "https://www.softhealer.com",
    "support": "support@softhealer.com",
    "license": "OPL-1",
    "category": "Theme/Backend",
    "version": "14.0.7",
    "summary": "Enterprise Backend Theme, Enterprise Theme, Backend Enterprise Theme, Flexible Enterprise Theme, Enter prise Theme Odoo",
    "description": """Do you want odoo enterpise look in your community version? Are You looking for modern, creative, clean, clear, materialise odoo enterpise look theme for your backend? So you are at the right place, We have made sure that this theme is highly clean, modern, fully customizable enterprise look theme. Cheers!""",
    "depends":
    [
        "web",
        "sh_ent_theme_config",
        "mail"
    ],
    
    "data":
    [
         "data/pwa_configuraion_data.xml",
        "security/ir.model.access.csv",
        "views/views.xml",
        "views/pwa_configuration_view.xml",
        "views/assets.xml",
        "views/login_layout.xml",
    ],

    "qweb": 
    [
        "static/src/xml/sh_thread.xml",
        "static/src/xml/menu.xml",    
        "static/src/xml/navbar.xml",    
        "static/src/xml/form_view.xml",
         "static/src/xml/widget.xml",
         "static/src/xml/global_search.xml",
         "static/src/xml/base.xml"
    ], 
    'images': [
        'static/description/banner.gif',
        'static/description/splash-screen_screenshot.gif'
    ],
    "live_test_url": "https://softhealer.com/contact_us",   
    "installable": True,
    "application": True,
    "price": 65,
    "currency": "EUR",
    "bootstrap": True  
}    
