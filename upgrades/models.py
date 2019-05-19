from django.db import models
from django.db.models.signals import post_save


class Rarity(models.Model):
    rarity = models.CharField(max_length=10)

    def __str__(self):
        return self.rarity


class Troop(models.Model):
    troop_name = models.CharField(max_length=24)
    total_exp = models.IntegerField(blank=True, null=True, default=None)
    total_gold = models.IntegerField(blank=True, null=True, default=None)

    def __str__(self):
        return self.troop_name


class Upgrades(models.Model):
    upgrades_rarity = models.ForeignKey(Rarity, on_delete=models.CASCADE, blank=True, null=True, default=None)
    upgrades_name = models.CharField(max_length=34)
    gold_for_sale = models.IntegerField(blank=True, null=True, default=None)
    gold_for_upgrade = models.IntegerField(blank=True, null=True, default=None)
    exp_for_upgrade = models.IntegerField(blank=True, null=True, default=None)
    icon = models.ImageField(upload_to='upgrades/images/', blank=True)
    upgrades_property = models.CharField(max_length=24, blank=True, null=True, default=None)

    def __str__(self):
        return "%s, %s" % (self.upgrades_rarity, self.upgrades_name)


class UpgradesSets(models.Model):
    upgrade_set_name = models.CharField(max_length=34)
    item_1 = models.ForeignKey(Upgrades, on_delete=models.CASCADE, related_name='+', blank=True, null=True, default=None)
    item_2 = models.ForeignKey(Upgrades, on_delete=models.CASCADE, related_name='+', blank=True, null=True, default=None)
    item_3 = models.ForeignKey(Upgrades, on_delete=models.CASCADE, related_name='+', blank=True, null=True, default=None)
    item_4 = models.ForeignKey(Upgrades, on_delete=models.CASCADE, related_name='+', blank=True, null=True, default=None)
    set_gold_for_sale = models.IntegerField(blank=True, null=True, default=None)
    set_gold_for_upgrade = models.IntegerField(blank=True, null=True, default=None)
    set_exp_for_upgrade = models.IntegerField(blank=True, null=True, default=None)
    troop = models.ForeignKey(Troop, on_delete=models.CASCADE, related_name='+', blank=True, null=True, default=None)

    def __str__(self):
        return "%s, %s" % (self.upgrade_set_name, self.troop)

    class Meta:
        verbose_name = 'Upgrade set'
        verbose_name_plural = 'Upgrade sets'

    def save(self, *args, **kwargs):

        self.set_exp_for_upgrade = (self.item_1.exp_for_upgrade + self.item_2.exp_for_upgrade +
                                    self.item_3.exp_for_upgrade + self.item_4.exp_for_upgrade)
        self.set_gold_for_sale = (self.item_1.gold_for_sale + self.item_2.gold_for_sale +
                                  self.item_3.gold_for_sale + self.item_4.gold_for_sale)
        self.set_gold_for_upgrade = (self.item_1.gold_for_upgrade + self.item_2.gold_for_upgrade +
                                     self.item_3.gold_for_upgrade + self.item_4.gold_for_upgrade)

        super(UpgradesSets, self).save(*args, **kwargs)


class Lvl(models.Model):
    lvl_name = models.CharField(max_length=34)
    exp_per_lvl_gain = models.PositiveIntegerField(blank=True, null=True, default=None)
    gold_per_lvl_need = models.PositiveIntegerField(blank=True, null=True, default=None)
    troop = models.ForeignKey(Troop, on_delete=models.CASCADE, related_name='+', blank=True, null=True, default=None)

    def __str__(self):
        return "%s, %s" % (self.troop, self.lvl_name)
#     lvl    1/2/3/4/5/6/7/8/9/0/1/2/3/4/5/6/7/8/9/0/1/2/3
#   g trooos 1/1/2/1/3/2/2/2/////////////////////////////2  44
#     troops 1/1/2/3/3/3/3/3/4/3/4/4/3/3/3/3/3/3/3/3/3/3/3  64


class SetsInLvl(models.Model):
    upgradesSets = models.ForeignKey(UpgradesSets, on_delete=models.CASCADE, related_name='+', blank=True, null=True, default=None)
    lvl = models.ForeignKey(Lvl, on_delete=models.CASCADE, related_name='+', blank=True, null=True, default=None)
    exp_gain = models.PositiveIntegerField(blank=True, null=True, default=None)
    gold_need = models.PositiveIntegerField(blank=True, null=True, default=None)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return "%s" % self.upgradesSets.upgrade_set_name

    def save(self, *args, **kwargs):
        exp_gain = self.upgradesSets.set_exp_for_upgrade
        self.exp_gain = exp_gain
        gold_need = self.upgradesSets.set_gold_for_upgrade
        self.gold_need = gold_need

        super(SetsInLvl, self).save(*args, **kwargs)


def sets_in_lvl_post_save(sender, instance, created, **kwargs):
    lvl = instance.lvl
    all_sets_in_lvl = SetsInLvl.objects.filter(lvl=lvl, is_active=True)

    exp_per_lvl_gain = 0
    gold_per_lvl_need = 0

    for set_in_lvl in all_sets_in_lvl:
        exp_per_lvl_gain += set_in_lvl.exp_gain
        gold_per_lvl_need += set_in_lvl.gold_need

    instance.lvl.exp_per_lvl_gain = exp_per_lvl_gain
    instance.lvl.gold_per_lvl_need = gold_per_lvl_need
    instance.lvl.save(force_update=True)


post_save.connect(sets_in_lvl_post_save, sender=SetsInLvl)


class LvlInTroop(models.Model):
    lvl = models.ForeignKey(Lvl, on_delete=models.CASCADE, related_name='+', blank=True, null=True, default=None)
    troop = models.ForeignKey(Troop, on_delete=models.CASCADE, related_name='+', blank=True, null=True, default=None)
    exp_per_lvl_gain = models.PositiveIntegerField(blank=True, null=True, default=None)
    gold_per_lvl_need = models.PositiveIntegerField(blank=True, null=True, default=None)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return "%s" % self.lvl.lvl_name

    def save(self, *args, **kwargs):
        exp_per_lvl_gain = self.lvl.exp_per_lvl_gain
        self.exp_per_lvl_gain = exp_per_lvl_gain
        gold_per_lvl_need = self.lvl.gold_per_lvl_need
        self.gold_per_lvl_need = gold_per_lvl_need

        super(LvlInTroop, self).save(*args, **kwargs)


def lvl_in_troop_post_save(sender, instance, created, **kwargs):
    troop = instance.troop
    all_lvl_in_troop = LvlInTroop.objects.filter(troop=troop, is_active=True)

    total_exp = 0
    total_gold = 0

    for lvl_in_troop in all_lvl_in_troop:
        total_exp += lvl_in_troop.exp_per_lvl_gain
        total_gold += lvl_in_troop.gold_per_lvl_need

    instance.troop.total_exp = total_exp
    instance.troop.total_gold = total_gold
    instance.troop.save(force_update=True)


post_save.connect(lvl_in_troop_post_save, sender=LvlInTroop)