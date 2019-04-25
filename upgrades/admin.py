from django.contrib import admin
from .models import Upgrades, UpgradesSets, Rarity, Heroes, Lvl, Setsinlvl


class HeroesInline(admin.TabularInline):
    model = UpgradesSets.heroes.through
    extra = 0


class HeroesAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Heroes._meta.fields]
    inlines = [
        HeroesInline,
    ]

    class Meta:
        model = Heroes


admin.site.register(Heroes, HeroesAdmin)


class UpgradesSetsAdmin(admin.ModelAdmin):
    list_display = [field.name for field in UpgradesSets._meta.fields]
    inlines = [
        HeroesInline,
    ]
    exclude = ('heroes',)

    class Meta:
        model = UpgradesSets


admin.site.register(UpgradesSets, UpgradesSetsAdmin)


class SetsinlvlInline(admin.TabularInline):
    model = Setsinlvl
    extra = 0


class SetsinlvlAdmin (admin.ModelAdmin):
    list_display = [field.name for field in Setsinlvl._meta.fields]

    class Meta:
        model = Setsinlvl


admin.site.register(Setsinlvl, SetsinlvlAdmin)


class LvlAdmin (admin.ModelAdmin):
    list_display = [field.name for field in Lvl._meta.fields]
    inlines = [SetsinlvlInline]

    class Meta:
        model = Lvl


admin.site.register(Lvl, LvlAdmin)

class UpgradesAdmin(admin.ModelAdmin):
     list_display = ['upgrades_rarity', 'upgrades_name']
    # fields = ('upgrades_rarity', 'upgrades_name')


# admin.site.register(Heroes, HeroesAdmin)
admin.site.register(Upgrades, UpgradesAdmin)
#admin.site.register(UpgradesSets)
admin.site.register(Rarity)
#admin.site.register(Heroes)
# Register your models here.
