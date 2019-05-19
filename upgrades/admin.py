from django.contrib import admin
from .models import Upgrades, UpgradesSets, Rarity, Troop, Lvl, SetsInLvl, LvlInTroop


class UpgradesSetsAdmin(admin.ModelAdmin):
    list_display = ['upgrade_set_name', 'set_gold_for_upgrade', 'set_exp_for_upgrade', 'troop']
    list_filter = ['troop']
    search_fields = ['upgrade_set_mame']
    # raw_id_fields = ['item_1', 'item_2', 'item_3', 'item_4']
    # save_on_top = True
    # save_as = True

    class Meta:
        model = UpgradesSets


admin.site.register(UpgradesSets, UpgradesSetsAdmin)


class SetsInLvlInline(admin.TabularInline):
    model = SetsInLvl
    extra = 0


class SetsInLvlAdmin (admin.ModelAdmin):
    list_display = [field.name for field in SetsInLvl._meta.fields]

    class Meta:
        model = SetsInLvl


admin.site.register(SetsInLvl, SetsInLvlAdmin)


class LvlAdmin (admin.ModelAdmin):
    list_display = [field.name for field in Lvl._meta.fields]
    inlines = [SetsInLvlInline]
    list_filter = ['troop']

    class Meta:
        model = Lvl


admin.site.register(Lvl, LvlAdmin)


class UpgradesAdmin(admin.ModelAdmin):
    list_display = ['upgrades_name', 'upgrades_rarity', 'gold_for_upgrade', 'exp_for_upgrade', 'gold_for_sale']
    # fields = ('upgrades_rarity', 'upgrades_name')
    list_filter = ['upgrades_rarity']
    list_editable = ['gold_for_upgrade']
    list_per_page = 100
    # list_display_links = ['upgrades_name', 'upgrades_rarity']
    search_fields = ['upgrades_name']


admin.site.register(Upgrades, UpgradesAdmin)


class LvlInTroopInline(admin.TabularInline):
    model = LvlInTroop
    extra = 0


class LvlInTroopAdmin (admin.ModelAdmin):
    list_display = [field.name for field in LvlInTroop._meta.fields]

    class Meta:
        model = SetsInLvl


admin.site.register(LvlInTroop, LvlInTroopAdmin)


class TroopAdmin(admin.ModelAdmin):
    list_display = ['troop_name', 'total_exp']
    inlines = [LvlInTroopInline]

    class Meta:
        model = Troop


admin.site.register(Troop, TroopAdmin)
admin.site.register(Rarity)
