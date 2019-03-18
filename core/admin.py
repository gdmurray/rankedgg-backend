from django.contrib import admin
from .models import Player, Report, PlayerMeta


# Register your models here.
class ReportInline(admin.TabularInline):
    extra = 2
    model = Report
    fields = ('operator', 'region', 'sender_ip')


class PlayerMetaInline(admin.TabularInline):
    extra = 0
    model = PlayerMeta
    fields = ('NA_mmr', 'NA_rank', 'EU_mmr', 'EU_rank', 'AS_mmr', 'AS_rank')


class PlayerAdmin(admin.ModelAdmin):
    list_display = ('username', 'p_id', 'last_queried')
    inlines = (ReportInline, PlayerMetaInline)
    model = Player
    fields = ('p_id', 'p_user', 'username', 'current_level', 'current_mmr', 'last_queried')


admin.site.register(Player, PlayerAdmin)
