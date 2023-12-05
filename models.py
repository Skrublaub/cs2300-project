from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, ARRAY
from database import Base

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
    className = Column(String, ForeignKey("class.className"))
    spellName = Column(String, ForeignKey("spells.spellName"))

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
    