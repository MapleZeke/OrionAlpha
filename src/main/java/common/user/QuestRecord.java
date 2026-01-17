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
package common.user;

import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.HashMap;
import java.util.Map;

/**
 * Represents a character's quest progress.
 *
 * @author Eric
 */
public class QuestRecord {
  private int questID;
  private byte state; // 0=None, 1=Started, 2=Completed
  private long startTime;
  private long completeTime;
  private String data; // Quest-specific data

  // Quest kill/collect tracking
  private final Map<Integer, Integer> mobKills = new HashMap<>();
  private final Map<Integer, Integer> itemCollects = new HashMap<>();

  public QuestRecord(int questID) {
    this.questID = questID;
    this.state = 0;
    this.data = "";
  }

  public void load(ResultSet rs) throws SQLException {
    this.questID = rs.getInt("QuestID");
    this.state = rs.getByte("State");
    this.startTime = rs.getLong("StartTime");
    this.completeTime = rs.getLong("CompleteTime");
    this.data = rs.getString("Data");
    if (this.data == null) {
      this.data = "";
    }
  }

  // Getters and setters
  public int getQuestID() {
    return questID;
  }

  public byte getState() {
    return state;
  }

  public void setState(byte state) {
    this.state = state;
  }

  public long getStartTime() {
    return startTime;
  }

  public void setStartTime(long startTime) {
    this.startTime = startTime;
  }

  public long getCompleteTime() {
    return completeTime;
  }

  public void setCompleteTime(long completeTime) {
    this.completeTime = completeTime;
  }

  public String getData() {
    return data;
  }

  public void setData(String data) {
    this.data = data;
  }

  // State helpers
  public boolean isStarted() {
    return state == 1;
  }

  public boolean isCompleted() {
    return state == 2;
  }

  public void start() {
    this.state = 1;
    this.startTime = System.currentTimeMillis();
  }

  public void complete() {
    this.state = 2;
    this.completeTime = System.currentTimeMillis();
  }

  // Mob kill tracking
  public int getMobKillCount(int mobID) {
    return mobKills.getOrDefault(mobID, 0);
  }

  public void setMobKillCount(int mobID, int count) {
    mobKills.put(mobID, count);
  }

  public void incrementMobKill(int mobID) {
    mobKills.put(mobID, getMobKillCount(mobID) + 1);
  }

  // Item collect tracking
  public int getItemCollectCount(int itemID) {
    return itemCollects.getOrDefault(itemID, 0);
  }

  public void setItemCollectCount(int itemID, int count) {
    itemCollects.put(itemID, count);
  }
}
