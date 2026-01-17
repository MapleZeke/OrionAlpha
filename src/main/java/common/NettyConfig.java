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
package common;

import io.netty.channel.WriteBufferWaterMark;

/** Netty performance tuning configuration. */
public class NettyConfig {
  // Buffer sizes
  public static final int SO_RCVBUF = 64 * 1024; // 64KB
  public static final int SO_SNDBUF = 64 * 1024; // 64KB

  // Write buffer water marks (backpressure control)
  public static final int WRITE_BUFFER_LOW_WATER_MARK = 8 * 1024; // 8KB
  public static final int WRITE_BUFFER_HIGH_WATER_MARK = 32 * 1024; // 32KB

  public static final WriteBufferWaterMark WRITE_BUFFER_WATER_MARK =
      new WriteBufferWaterMark(WRITE_BUFFER_LOW_WATER_MARK, WRITE_BUFFER_HIGH_WATER_MARK);

  // Connection settings
  public static final int SO_BACKLOG = 1024;
  public static final boolean SO_REUSEADDR = true;
  public static final boolean TCP_NODELAY = true;
  public static final boolean SO_KEEPALIVE = true;
  public static final boolean AUTO_READ = true;
}
