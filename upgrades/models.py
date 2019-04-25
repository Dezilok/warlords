from django.db import models

from django.db.models.signals import post_save

# Create your models here.


class Rarity(models.Model):
    rarity = models.CharField(max_length=10)

    def __str__(self):
        return self.rarity


class Heroes(models.Model):
    heroes_name = models.CharField(max_length=24)
    exp = models.IntegerField(blank=True, null=True, default=None)

    def __str__(self):
        return self.heroes_name

    def save(self, *args, **kwargs):
        # self.exp = sum(UpgradesSets.set_exp_for_upgrade)
        super(Heroes, self).save(*args, **kwargs)


class Upgrades(models.Model):
    upgrades_rarity = models.ForeignKey(Rarity, on_delete=models.CASCADE, blank=True, null=True, default=None)
    upgrades_name = models.CharField(max_length=34)
    gold_for_sale = models.IntegerField(blank=True, null=True, default=None)
    gold_for_upgrade = models.IntegerField(blank=True, null=True, default=None)
    exp_for_upgrade = models.IntegerField(blank=True, null=True, default=None)
    icon = models.ImageField(upload_to='upgrades/images/', blank=True)
    upgrades_property = models.CharField(max_length=24, blank=True, null=True, default=None)

    def __str__(self):
        return self.upgrades_name


class UpgradesSets(models.Model):
    name = models.CharField(max_length=34)
    item_1 = models.ForeignKey(Upgrades, on_delete=models.CASCADE, related_name='+', blank=True, null=True, default=None)
    item_2 = models.ForeignKey(Upgrades, on_delete=models.CASCADE, related_name='+', blank=True, null=True, default=None)
    item_3 = models.ForeignKey(Upgrades, on_delete=models.CASCADE, related_name='+', blank=True, null=True, default=None)
    item_4 = models.ForeignKey(Upgrades, on_delete=models.CASCADE, related_name='+', blank=True, null=True, default=None)
    set_gold_for_sale = models.IntegerField(blank=True, null=True, default=None)
    set_gold_for_upgrade = models.IntegerField(blank=True, null=True, default=None)
    set_exp_for_upgrade = models.IntegerField(blank=True, null=True, default=None)
    heroes = models.ManyToManyField(Heroes, related_name='UpgradesSets')

    def __str__(self):
        return self.name

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
    name = models.CharField(max_length=10)


class Setsinlvl(models.Model):
    upgradesSets = models.ForeignKey(UpgradesSets, on_delete=models.CASCADE, related_name='+', blank=True, null=True, default=None)
    lvl = models.ForeignKey(Lvl, on_delete=models.CASCADE, related_name='+', blank=True, null=True, default=None)
    is_active = models.BooleanField(default=True)



