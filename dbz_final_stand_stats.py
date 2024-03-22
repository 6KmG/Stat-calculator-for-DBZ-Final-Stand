import warnings
from matplotlib import pyplot

class Player:
  RACE_STATS = {"android":1, "saiyan":1/3, "human":1/2, "majin":1/2, "frieza":1/2, "namekian":1/2, "jiren":1/2}
  RACES = RACE_STATS.keys()
  MIN_DEATH_LVL = 602
  MIN_PRESTIGE_LVL = 432

  def __init__(self, race: str, level = 1, melee_stat = 0, other_stat = 0, name = "Player_Name", _prestiges = 0, _rebirthed = False):
    if race not in Player.RACES:
      raise ValueError("The given race is incorrect.")
    self.level = round(level)
    self.melee_stat = round(melee_stat) + 2
    self.other_stat = round(other_stat)
    self.race = race
    self.name = name
    self.rebirthed = _rebirthed
    self.dead = False
    self.prestiges = _prestiges

  def formatStats(self) -> str:
    text = "\tPLAYER STATS\n"
    text += f"{'Name' :<18} {player.name :>18} \n"
    text += f"{'Race' :<18} {player.race.capitalize() :>18} \n"
    text += f"{'Level' :<18} {player.level :>18} \n"
    text += f"{'Health Max' :<18} {player.other_stat :>18} \n"
    text += f"{'Ki Max' :<18} {player.other_stat :>18} \n"
    text += f"{'Melee Damage' :<18} {player.melee_stat :>18} \n"
    text += f"{'Ki Damage' :<18} {player.other_stat :>18} \n"
    text += f"{'Melee Resistance' :<18} {player.other_stat :>18} \n"
    text += f"{'Ki Resistance' :<18} {player.other_stat :>18} \n"
    text += f"{'Speed' :<18} {player.other_stat :>18} \n"
    return text

  def levelUp(self, levels: int):
    self.level += levels
    if(self.dead):
      self.other_stat += round(levels)
      self.melee_stat += round(levels * 2)
    else:
      self.other_stat += round(levels * Player.RACE_STATS[self.race])
      self.melee_stat += round(levels * Player.RACE_STATS[self.race]) + levels

  def levelDown(self, levels: int):
    self.level -= levels
    if(self.dead):
      warnings.warn("You're levelling down while being dead, this will cause inconsistencies in your stats")
      self.other_stat -= round(levels)
      self.melee_stat -= round(levels * 2)
    else:
      self.other_stat -= round(levels * Player.RACE_STATS[self.race])
      self.melee_stat -= round(levels * Player.RACE_STATS[self.race]) + levels

  def setLevel(self, level: int):
    difference = level - self.level
    self.level = level
    if(self.dead):
      warnings.warn("You're levelling down while being dead, this will cause inconsistencies in your stats")
      self.other_stat += round(difference)
      self.melee_stat += round(difference * 2)
    else:
      self.other_stat += round(difference * Player.RACE_STATS[self.race])
      self.melee_stat += round(difference * Player.RACE_STATS[self.race]) + difference

  def wishDeath(self):
    if(Player.MIN_DEATH_LVL > self.level or self.rebirthed):
      raise ValueError("The lowest level, when you can wish death is 602.")
    else:
      self.dead = True
  
  def rebirth(self):
    if self.dead and self.level >= 850:
      Player.__init__(
        self, 
        race = self.race, 
        melee_stat = self.melee_stat / 10 + 300, 
        other_stat = self.other_stat / 10 + 300,
        _prestiges = self.prestiges, 
        _rebirthed = True
      )
    else:
      raise ValueError("You can't rebirth below level 850.")
  
  def prestige(self):
    if Player.MIN_PRESTIGE_LVL > self.level:
      raise ValueError("Your level is not high enough to prestige.")
    if self.rebirthed:
      Player.__init__(
        self,
        race = self.race, 
        melee_stat = self.melee_stat / 5 + 300, 
        other_stat = self.other_stat / 5 + 300, 
        _prestiges = self.prestiges + 1,
        _rebirthed = self.rebirthed
      )
    else:
      Player.__init__(
        self, 
        race = self.race, 
        melee_stat = self.melee_stat / 5, 
        other_stat = self.other_stat / 5,
        _prestiges = self.prestiges + 1,
        _rebirthed = self.rebirthed
      )

if __name__=="__main__":
  player = Player("android")
  player.setLevel(602)
  player.wishDeath()
  player.setLevel(2000)
  player.rebirth()
  num_of_prestiges = 5
  melee_stats = [player.melee_stat]
  other_stats = [player.other_stat]

  for i in range(num_of_prestiges):
    player.setLevel(2000)
    player.prestige()
    melee_stats.append(player.melee_stat)
    other_stats.append(player.other_stat)

  print(player.formatStats())
  print(vars(player))

  pyplot.scatter(range(num_of_prestiges + 1), melee_stats)
  pyplot.show()

  pyplot.scatter(range(num_of_prestiges + 1), other_stats)
  pyplot.show()
