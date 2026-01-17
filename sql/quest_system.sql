-- Quest System Tables for OrionAlpha
-- Add these tables to your existing database

-- Quest completion tracking
CREATE TABLE IF NOT EXISTS `questrecord` (
  `CharacterID` INT(11) NOT NULL,
  `QuestID` INT(11) NOT NULL,
  `State` TINYINT(4) NOT NULL DEFAULT 0 COMMENT '0=None, 1=Started, 2=Completed',
  `StartTime` BIGINT(20) DEFAULT NULL,
  `CompleteTime` BIGINT(20) DEFAULT NULL,
  `Data` VARCHAR(255) DEFAULT NULL COMMENT 'Quest-specific data (item counts, progress, etc.)',
  PRIMARY KEY (`CharacterID`, `QuestID`),
  KEY `idx_character` (`CharacterID`),
  KEY `idx_quest` (`QuestID`),
  KEY `idx_state` (`State`),
  CONSTRAINT `fk_questrecord_character` FOREIGN KEY (`CharacterID`) REFERENCES `character` (`CharacterID`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Quest kill tracking (for "kill X mobs" quests)
CREATE TABLE IF NOT EXISTS `questmobkill` (
  `CharacterID` INT(11) NOT NULL,
  `QuestID` INT(11) NOT NULL,
  `MobID` INT(11) NOT NULL,
  `Count` INT(11) NOT NULL DEFAULT 0,
  PRIMARY KEY (`CharacterID`, `QuestID`, `MobID`),
  KEY `idx_character_quest` (`CharacterID`, `QuestID`),
  CONSTRAINT `fk_questmobkill_character` FOREIGN KEY (`CharacterID`) REFERENCES `character` (`CharacterID`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Quest item collection tracking
CREATE TABLE IF NOT EXISTS `questitemcollect` (
  `CharacterID` INT(11) NOT NULL,
  `QuestID` INT(11) NOT NULL,
  `ItemID` INT(11) NOT NULL,
  `Count` INT(11) NOT NULL DEFAULT 0,
  PRIMARY KEY (`CharacterID`, `QuestID`, `ItemID`),
  KEY `idx_character_quest` (`CharacterID`, `QuestID`),
  CONSTRAINT `fk_questitemcollect_character` FOREIGN KEY (`CharacterID`) REFERENCES `character` (`CharacterID`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
