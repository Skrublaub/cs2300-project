from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, ARRAY
from database import Base

class MonsterSenses(Base):
    __tablename__ = 'monsterSenses'
    sense = Column(String, primary_key=True, index=True)
    monsterStatUnit = Column(String, index=True)
    statNumber = Column(Integer, index=True)

class MonsterHasSense(Base):
    __tablename__ = 'monsterHasSense'
    monsterName = Column(String, ForeignKey("monsters.monsterName"),primary_key=True, index=True)
    senseName = Column(String, ForeignKey("sense.senseName"), index=True)

class MonsterActions(Base):
    __tablename__ = 'monsterActions'
    actionName = Column(String, primary_key=True, index=True)
    monsterName = Column(String, ForeignKey("monsters.monsterName"), index=True)
    recharge = Column(Integer, index=True)
    dc = Column(Integer, index=True)
    dcStat = Column(String, index=True)
    hitPlus = Column(Integer, index=True)
    reach = Column(Integer, index=True)
    amtTarget = Column(Integer, index=True)
    amtDamageDice = Column(ARRAY(Integer), index=True)
    maxDamageAmt = Column(ARRAY(Integer), index=True)
    damageType = Column(ARRAY(String), index=True)
    damageAdd = Column(ARRAY(Integer), index=True)
    spellLevel = Column(ARRAY(Integer), index=True)
    isSpellsCast = Column(Boolean, index=True)

class MonsterSkills(Base):
    __tablename__ = 'monsterSkills'
    monsterName = Column(String, ForeignKey("monsters.monsterName"),primary_key=True, index=True)
    monsterSkill = Column(String, ForeignKey("skill.skillName"), index=True)
    monsterBonus = Column(Integer, index=True)

class Monsters(Base):
    __tablename__ = 'monsters'
    monsterName = Column(String, primary_key=True, index=True)
    hitPoints = Column(Integer, index=True)
    profBonus = Column(Integer, index=True)
    cr = Column(Integer, index=True)
    speed = Column(ARRAY(Integer), index=True)
    abilityScores = Column(ARRAY(Integer), index=True)
    monsterSize = Column(String, index=True)
    alignment = Column(String, index=True)
    monsterType = Column(String, index=True)
    infoSource = Column(String, index=True)
    favoredEnvironment= Column(ARRAY(String), index=True)

class MonsterLang(Base):
    __tablename__ = 'monsterLang'
    monsterName = Column(String, ForeignKey("monster.monsterName"),primary_key=True, index=True)
    languageName = Column(String, ForeignKey("languages.languageName"), index=True)

class Race(Base):
    __tablename__ = 'race'
    raceName = Column(String, primary_key=True, index=True)
    raceSize = Column(String, index=True)
    alignment = Column(String, index=True)
    bookSource = Column(String, index=True)
    raceAge = Column(String, index=True)
    speed = Column(ARRAY(Integer), index=True)
    abilityScoresNum = Column(ARRAY(Integer), index=True)
    abilityScoresName = Column(ARRAY(Integer), index=True)

class RaceLanguages(Base):
    __tablename__ = 'raceLanguages'
    raceName = Column(String, ForeignKey("race.raceName"),primary_key=True, index=True)
    languageName = Column(String, ForeignKey("languages.languageName"), index=True)

class Languages(Base):
    __tablename__ = 'languages'
    languageName = Column(String, primary_key=True, index=True)
    languageType = Column(String, index=True)
    languageScript = Column(String, index=True)
    bookSource = Column(String, index=True)
    typicalSpeakers = Column(ARRAY(String), index=True)

class BackgroundLang(Base):
    __tablename__ = 'backgroundLang'
    bgName = Column(String, ForeignKey("background.bgName"),primary_key=True, index=True)
    languageName = Column(String, ForeignKey("languages.languageName"), index=True)

class Background(Base):
    __tablename__ = 'background'
    bgName = Column(Integer, primary_key=True, index=True)
    description = Column(String, index=True)
    feature = Column(String, index=True)
    featureDescription = Column(String, index=True)
    suggestedCharacteristicDesc = Column(String, index=True)
    bookSource = Column(String, index=True)
    equipment = Column(ARRAY(String), index=True)
    personalityTrait = Column(ARRAY(String), index=True)
    ideal = Column(ARRAY(String), index=True)
    bond = Column(ARRAY(String), index=True)
    flaw = Column(ARRAY(String), index=True)

class BackgroundSkill(Base):
    __tablename__ = 'backgroundSkill'
    bgName = Column(String, ForeignKey("background.bgName"),primary_key=True, index=True)
    skillName = Column(String, ForeignKey("skill.skillName"), index=True)

class Skills(Base):
    __tablename__ = 'skills'
    relatedAbility = Column(String, index=True)
    skillName = Column(String, ForeignKey("skill.skillName"),primary_key=True, index=True)

class ClassSkills(Base):
    __tablename__ = 'classSkills'
    className = Column(String, ForeignKey("class.className"),primary_key=True, index=True)
    skillName = Column(String, ForeignKey("skill.skillName"), index=True)

class Tools(Base):
    __tablename__ = 'tools'

    toolName = Column(String, primary_key=True, index=True)
    toolCost = Column(Integer, index=True)
    weight = Column(Integer, index=True)
    costUnit = Column(String, index=True)
    weightUnit = Column(String, index=True)
    bookSource = Column(String, index=True)
    description = Column(String, index=True)
    isArtisan = Column(Boolean, index=True)
    activityName =  Column(ARRAY(String), index=True)
    activityDC =  Column(ARRAY(Integer), index=True)


class CanUseTool(Base):
    __tablename__ = 'canUseTool'
    className = Column(String, ForeignKey("class.className"),primary_key=True, index=True)
    toolName = Column(String, ForeignKey("tool.toolName"), index=True)

class StartsTool(Base):
    __tablename__ = 'startsTool'
    className = Column(String, ForeignKey("class.className"),primary_key=True, index=True)
    toolName = Column(String, ForeignKey("tool.toolName"), index=True)

class Weapons(Base):
    __tablename__ = 'weapons'

    weaponName = Column(String, primary_key=True, index=True)
    toolCost = Column(Integer, index=True)
    weight = Column(Integer, index=True)
    damageDiceMax = Column(Integer, index=True)
    amtDamageDice = Column(Integer, index=True)
    costUnit = Column(String, index=True)
    weightUnit = Column(String, index=True)
    throwingRange = Column(String, index=True)
    damageType = Column(String, index=True)
    bookSource = Column(String, index=True)
    properties = Column(String, index=True)
    weaponSubtype = Column(String, index=True)
    isMartial = Column(Boolean, index=True)
    isRanged = Column(Boolean, index=True)
    canThrow = Column(Boolean, index=True)

class StartsWeapon(Base):
    __tablename__ = 'startsWeapon'
    className = Column(String, ForeignKey("class.className"),primary_key=True, index=True)
    weaponName = Column(String, ForeignKey("weapon.weaponName"), index=True)

class CanUseWeapon(Base):
    __tablename__ = 'canUseWeapon'
    className = Column(String, ForeignKey("class.className"),primary_key=True, index=True)
    weaponName = Column(String, ForeignKey("weapon.weaponName"), index=True)

class Armor(Base):
    __tablename__ = 'armor'

    armorName = Column(String, primary_key=True, index=True)
    costAmt = Column(Integer, index=True)
    weight = Column(Integer, index=True)
    AC = Column(Integer, index=True)
    armorType = Column(String, index=True)
    costUnit = Column(String, index=True)
    weightUnit = Column(String, index=True)
    bookSource = Column(String, index=True)
    desc = Column(String, index=True)
    
class StartsArmor(Base):
    __tablename__ = 'startsArmor'
    className = Column(String, ForeignKey("class.className"),primary_key=True, index=True)
    armorName = Column(String, ForeignKey("armor.armorName"), index=True)

class CanWear(Base):
    __tablename__ = 'canWear'
    className = Column(String, ForeignKey("class.className"),primary_key=True, index=True)
    armorName = Column(String, ForeignKey("armor.armorName"), index=True)

class Class(Base):
    __tablename__ = 'class'

    className = Column(String, primary_key=True, index=True)
    hitDie = Column(Integer, index=True)
    desc = Column(String, index=True)
    skillChooseAmt = Column(Integer, index=True)
    startEquip = Column(ARRAY(String), index=True)
    multiclassAbility = Column(ARRAY(String), index=True)
    multiclassAbilityBothRequired = Column(Boolean, index=True)
    multiclassArmor = Column(ARRAY(String), index=True)
    multiclassWeapon = Column(ARRAY(String), index=True)


class ClassCanCast(Base):
    __tablename__ = 'classCanCast'
    className = Column(String, ForeignKey("class.className"),primary_key=True, index=True)
    spellName = Column(String, ForeignKey("spells.spellName"), index=True)

class Spells(Base):
    __tablename__ = 'spells'

    spellName = Column(String, primary_key=True, index=True)
    spellRadius = Column(Integer, index=True)
    spellRange = Column(Integer, index=True)
    spellLevel = Column(Integer, index=True)
    duration = Column(Integer, index=True)
    damageDice = Column(Integer, index=True)
    maxDamage = Column(Integer, index=True)
    desc = Column(String, index=True)
    castTime = Column(String, index=True)
    components = Column(String, index=True)
    school = Column(String, index=True)
    concentration = Column(Boolean, index=True)
    