from django.contrib import admin
from django.conf import settings

admin.site.site_header = getattr(settings, "ADMIN_SITE_HEADER", "Kuaför & Berber Yönetim Sistemi")
admin.site.site_title = getattr(settings, "ADMIN_SITE_TITLE", "Kuaför Otomasyon")
admin.site.index_title = getattr(settings, "ADMIN_INDEX_TITLE", "Yönetim Paneli")
