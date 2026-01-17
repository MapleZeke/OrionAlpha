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
package network;

import io.netty.channel.EventLoopGroup;
import io.netty.channel.ServerChannel;
import io.netty.channel.epoll.Epoll;
import io.netty.channel.epoll.EpollEventLoopGroup;
import io.netty.channel.epoll.EpollServerSocketChannel;
import io.netty.channel.epoll.EpollSocketChannel;
import io.netty.channel.kqueue.KQueue;
import io.netty.channel.kqueue.KQueueEventLoopGroup;
import io.netty.channel.kqueue.KQueueServerSocketChannel;
import io.netty.channel.kqueue.KQueueSocketChannel;
import io.netty.channel.nio.NioEventLoopGroup;
import io.netty.channel.socket.SocketChannel;
import io.netty.channel.socket.nio.NioServerSocketChannel;
import io.netty.channel.socket.nio.NioSocketChannel;
import util.Logger;

/**
 * Detects the best available Netty transport for the current platform. Prefers native transports
 * (Epoll on Linux, KQueue on macOS) with automatic fallback to NIO.
 */
public class NettyTransportDetector {

  private static final TransportType TRANSPORT_TYPE;

  static {
    if (Epoll.isAvailable()) {
      TRANSPORT_TYPE = TransportType.EPOLL;
      Logger.logReport("Using Epoll native transport for optimal Linux performance");
    } else if (KQueue.isAvailable()) {
      TRANSPORT_TYPE = TransportType.KQUEUE;
      Logger.logReport("Using KQueue native transport for optimal macOS performance");
    } else {
      TRANSPORT_TYPE = TransportType.NIO;
      Logger.logReport("Using NIO transport (Windows or native transport unavailable)");
    }
  }

  public static Class<? extends ServerChannel> getServerChannelClass() {
    return switch (TRANSPORT_TYPE) {
      case EPOLL -> EpollServerSocketChannel.class;
      case KQUEUE -> KQueueServerSocketChannel.class;
      case NIO -> NioServerSocketChannel.class;
    };
  }

  public static Class<? extends SocketChannel> getClientChannelClass() {
    return switch (TRANSPORT_TYPE) {
      case EPOLL -> EpollSocketChannel.class;
      case KQUEUE -> KQueueSocketChannel.class;
      case NIO -> NioSocketChannel.class;
    };
  }

  public static EventLoopGroup createBossGroup(int threads) {
    return switch (TRANSPORT_TYPE) {
      case EPOLL -> new EpollEventLoopGroup(threads);
      case KQUEUE -> new KQueueEventLoopGroup(threads);
      case NIO -> new NioEventLoopGroup(threads);
    };
  }

  public static EventLoopGroup createWorkerGroup() {
    return switch (TRANSPORT_TYPE) {
      case EPOLL -> new EpollEventLoopGroup();
      case KQUEUE -> new KQueueEventLoopGroup();
      case NIO -> new NioEventLoopGroup();
    };
  }

  public static String getTransportName() {
    return TRANSPORT_TYPE.name();
  }

  private enum TransportType {
    EPOLL,
    KQUEUE,
    NIO
  }
}
