/*
 * This file is part of OrionAlpha, a MapleStory Emulator Project.
 * Copyright (C) 2018 Eric Smith <notericsoft@gmail.com>
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 */
package network.database;

import common.user.CharacterData;
import common.user.QuestRecord;
import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;

/**
 * Quest database operations
 *
 * @author Eric
 */
public class QuestDB {

  /**
   * Load all quest records for a character
   *
   * @param characterID The character ID
   * @param cd The CharacterData to populate
   */
  public static void rawLoadQuestRecords(int characterID, CharacterData cd) {
    try (Connection con = Database.getDB().poolConnection()) {
      // Load quest states
      try (PreparedStatement ps =
          con.prepareStatement("SELECT * FROM `questrecord` WHERE `CharacterID` = ?")) {
        ps.setInt(1, characterID);
        try (ResultSet rs = ps.executeQuery()) {
          while (rs.next()) {
            QuestRecord record = new QuestRecord(rs.getInt("QuestID"));
            record.load(rs);
            cd.setQuestRecord(record.getQuestID(), record);
          }
        }
      }

      // Load mob kill progress
      try (PreparedStatement ps =
          con.prepareStatement("SELECT * FROM `questmobkill` WHERE `CharacterID` = ?")) {
        ps.setInt(1, characterID);
        try (ResultSet rs = ps.executeQuery()) {
          while (rs.next()) {
            int questID = rs.getInt("QuestID");
            int mobID = rs.getInt("MobID");
            int count = rs.getInt("Count");
            QuestRecord record = cd.getQuestRecord(questID);
            record.setMobKillCount(mobID, count);
          }
        }
      }

      // Load item collect progress
      try (PreparedStatement ps =
          con.prepareStatement("SELECT * FROM `questitemcollect` WHERE `CharacterID` = ?")) {
        ps.setInt(1, characterID);
        try (ResultSet rs = ps.executeQuery()) {
          while (rs.next()) {
            int questID = rs.getInt("QuestID");
            int itemID = rs.getInt("ItemID");
            int count = rs.getInt("Count");
            QuestRecord record = cd.getQuestRecord(questID);
            record.setItemCollectCount(itemID, count);
          }
        }
      }
    } catch (SQLException ex) {
      ex.printStackTrace(System.err);
    }
  }

  /**
   * Save a quest record
   *
   * @param characterID The character ID
   * @param record The quest record to save
   */
  public static void rawSaveQuestRecord(int characterID, QuestRecord record) {
    try (Connection con = Database.getDB().poolConnection()) {
      try (PreparedStatement ps =
          con.prepareStatement(
              "INSERT INTO `questrecord` (`CharacterID`, `QuestID`, `State`, `StartTime`, `CompleteTime`, `Data`) "
                  + "VALUES (?, ?, ?, ?, ?, ?) "
                  + "ON DUPLICATE KEY UPDATE `State` = ?, `CompleteTime` = ?, `Data` = ?")) {
        ps.setInt(1, characterID);
        ps.setInt(2, record.getQuestID());
        ps.setByte(3, record.getState());
        ps.setLong(4, record.getStartTime());
        ps.setLong(5, record.getCompleteTime());
        ps.setString(6, record.getData());
        ps.setByte(7, record.getState());
        ps.setLong(8, record.getCompleteTime());
        ps.setString(9, record.getData());
        ps.executeUpdate();
      }
    } catch (SQLException ex) {
      ex.printStackTrace(System.err);
    }
  }

  /**
   * Update quest state (started/completed)
   *
   * @param characterID The character ID
   * @param questID The quest ID
   * @param state The new state (0=None, 1=Started, 2=Completed)
   */
  public static void rawUpdateQuestState(int characterID, int questID, byte state) {
    try (Connection con = Database.getDB().poolConnection()) {
      String sql;
      if (state == 1) { // Started
        sql =
            "INSERT INTO `questrecord` (`CharacterID`, `QuestID`, `State`, `StartTime`) "
                + "VALUES (?, ?, 1, ?) ON DUPLICATE KEY UPDATE `State` = 1, `StartTime` = ?";
      } else { // Completed
        sql =
            "UPDATE `questrecord` SET `State` = 2, `CompleteTime` = ? "
                + "WHERE `CharacterID` = ? AND `QuestID` = ?";
      }

      try (PreparedStatement ps = con.prepareStatement(sql)) {
        long time = System.currentTimeMillis();
        if (state == 1) {
          ps.setInt(1, characterID);
          ps.setInt(2, questID);
          ps.setLong(3, time);
          ps.setLong(4, time);
        } else {
          ps.setLong(1, time);
          ps.setInt(2, characterID);
          ps.setInt(3, questID);
        }
        ps.executeUpdate();
      }
    } catch (SQLException ex) {
      ex.printStackTrace(System.err);
    }
  }

  /**
   * Save mob kill progress
   *
   * @param characterID The character ID
   * @param questID The quest ID
   * @param mobID The mob ID
   * @param count The kill count
   */
  public static void rawSaveMobKill(int characterID, int questID, int mobID, int count) {
    try (Connection con = Database.getDB().poolConnection()) {
      try (PreparedStatement ps =
          con.prepareStatement(
              "INSERT INTO `questmobkill` (`CharacterID`, `QuestID`, `MobID`, `Count`) "
                  + "VALUES (?, ?, ?, ?) ON DUPLICATE KEY UPDATE `Count` = ?")) {
        ps.setInt(1, characterID);
        ps.setInt(2, questID);
        ps.setInt(3, mobID);
        ps.setInt(4, count);
        ps.setInt(5, count);
        ps.executeUpdate();
      }
    } catch (SQLException ex) {
      ex.printStackTrace(System.err);
    }
  }
}
