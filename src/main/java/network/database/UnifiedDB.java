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

import com.zaxxer.hikari.HikariConfig;
import com.zaxxer.hikari.HikariDataSource;
import java.sql.Connection;
import java.sql.SQLException;
import util.Logger;

/**
 * Our ConnectionPool and globally used Database Connection handler. All Connections are to be used
 * from poolConnection() and closed after. Upon shutdown, close() is to be called to shutdown the
 * DataSource.
 *
 * <p>Uses HikariCP 5.1.0 with optimized settings for game server workloads including:
 *
 * <ul>
 *   <li>Connection pooling with configurable min/max sizes
 *   <li>PreparedStatement caching for performance
 *   <li>Connection lifecycle management (timeouts, keepalive)
 *   <li>MariaDB-specific performance optimizations
 *   <li>Optional leak detection for development
 * </ul>
 *
 * @author Eric
 */
public class UnifiedDB {
  public static final int
      // Maximum concurrent connections
      MAXIMUM_POOL_SIZE = 20,
      // Minimum idle connections (saves resources when not under load)
      MINIMUM_IDLE = 5,
      // Connection timeout in milliseconds (30 seconds)
      CONNECTION_TIMEOUT = 30000,
      // Idle timeout in milliseconds (10 minutes)
      IDLE_TIMEOUT = 600000,
      // Max connection lifetime in milliseconds (30 minutes)
      MAX_LIFETIME = 1800000,
      // Keepalive time in milliseconds (5 minutes)
      KEEPALIVE_TIME = 300000,
      // Default connection port
      DefaultPort = 3306;
  public static final String
      // Supported drivers available
      Driver_MySQL = "mysql",
      Driver_MariaDB = "mariadb",
      // Default connection server host
      DefaultHost = "localhost";

  private HikariDataSource dataSource;
  private final String user;
  private final String password;
  private final String dbName;
  private final String serverName;
  private final int port;

  public UnifiedDB(String dbName, String user, String passwd) {
    this.dbName = dbName;
    this.serverName = DefaultHost;
    this.user = user;
    this.password = passwd;
    this.port = DefaultPort;
  }

  public UnifiedDB(String dbName, String serverName, String user, String passwd, int port) {
    this.dbName = dbName;
    this.serverName = serverName;
    this.user = user;
    this.password = passwd;
    this.port = port;
  }

  /** Load the DataSource upon startup for use to access the object. */
  public final void load() {
    if (dataSource == null) {
      HikariConfig config = new HikariConfig();

      // JDBC Connection URL
      config.setJdbcUrl("jdbc:%s://%s:%d/%s".formatted(Driver_MariaDB, serverName, port, dbName));
      config.setUsername(user);
      config.setPassword(password);

      // Pool Sizing - Optimized for game server workload
      config.setMaximumPoolSize(MAXIMUM_POOL_SIZE); // 20 connections max
      config.setMinimumIdle(MINIMUM_IDLE); // Keep 5 idle connections ready

      // Connection Lifecycle Management
      config.setConnectionTimeout(
          CONNECTION_TIMEOUT); // 30 seconds - time to wait for connection from pool
      config.setIdleTimeout(IDLE_TIMEOUT); // 10 minutes - retire idle connections
      config.setMaxLifetime(MAX_LIFETIME); // 30 minutes - maximum connection lifetime
      config.setKeepaliveTime(KEEPALIVE_TIME); // 5 minutes - keep connections alive (HikariCP 5.1+)

      // Pool Identification (for monitoring/logging)
      config.setPoolName("OrionAlpha-DB-Pool");

      // Connection Testing
      config.setConnectionTestQuery("SELECT 1"); // Fast health check query

      // Transaction Management
      config.setAutoCommit(true);

      // Leak Detection (enabled via system property for development)
      // Usage: java -Dhikari.leakDetection=true ...
      if ("true".equals(System.getProperty("hikari.leakDetection", "false"))) {
        config.setLeakDetectionThreshold(60000); // 60 seconds - warn if connection held too long
      }

      // MariaDB PreparedStatement Caching (already present, keeping)
      config.addDataSourceProperty("cachePrepStmts", "true");
      config.addDataSourceProperty("prepStmtCacheSize", "250");
      config.addDataSourceProperty("prepStmtCacheSqlLimit", "2048");
      config.addDataSourceProperty("useServerPrepStmts", "true");

      // Character Encoding - Use utf8mb4 for full Unicode support (emojis, etc.)
      config.addDataSourceProperty("characterEncoding", "utf8mb4");
      config.addDataSourceProperty("useUnicode", "true");

      // MariaDB Performance Optimizations
      config.addDataSourceProperty("rewriteBatchedStatements", "true"); // Optimize batch inserts
      config.addDataSourceProperty("useLocalSessionState", "true"); // Skip redundant SET commands
      config.addDataSourceProperty("cacheResultSetMetadata", "true"); // Cache result metadata
      config.addDataSourceProperty(
          "cacheServerConfiguration", "true"); // Cache server configuration
      config.addDataSourceProperty(
          "elideSetAutoCommits", "true"); // Skip redundant autocommit calls

      // REMOVED: autoReconnect is deprecated in MariaDB Connector/J 3.x
      // HikariCP handles reconnection automatically

      dataSource = new HikariDataSource(config);

      Logger.logReport(
          "HikariCP connection pool initialized: %s (max=%d, min=%d)"
              .formatted(
                  config.getPoolName(), config.getMaximumPoolSize(), config.getMinimumIdle()));
    }
  }

  /**
   * Pools a Connection object from the Data Source. To configure maximum pooled connections, change
   * constant 'MAXIMUM_POOL_SIZE'.
   *
   * <p>Connection timeout properties are set to the HikariCP library defaults.
   *
   * @return A new java.sql.Connection object.
   */
  public Connection poolConnection() {
    try {
      if (dataSource != null) {
        return dataSource.getConnection();
      }
      Logger.logError("Attempting to make a connection before loading the database.");
    } catch (SQLException ex) {
      ex.printStackTrace(System.err);
    }
    return null;
  }

  /**
   * Properly close the DataSource. This should ONLY be called when shutting down the center
   * servers.
   *
   * <p>-> shutdown is now deprecated, resort to close.
   */
  public void close() {
    dataSource.close();
  }
}
