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
package launcher;

import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

/**
 * Unified launcher for OrionAlpha servers. Starts Login, Game, and Shop servers in the correct
 * sequence using separate JVM processes.
 *
 * @author OrionAlpha Team
 */
public class OrionLauncher {
  private static final List<Process> processes = new ArrayList<>();
  private static final String DEFAULT_CLASSPATH = "target/OrionAlpha.jar";
  private static final String DEFAULT_WZPATH = "data/";

  public static void main(String[] args) {
    // Parse command-line arguments
    boolean noShop = hasFlag(args, "--no-shop");
    boolean loginOnly = hasFlag(args, "--login-only");
    int worlds = getWorldCount(args);

    // Register shutdown hook for graceful termination
    Runtime.getRuntime()
        .addShutdownHook(
            new Thread(
                () -> {
                  System.out.println("Shutting down all servers...");
                  for (Process process : processes) {
                    if (process.isAlive()) {
                      process.destroy();
                      try {
                        // Wait up to 5 seconds for graceful shutdown
                        if (!process.waitFor(5, java.util.concurrent.TimeUnit.SECONDS)) {
                          process.destroyForcibly();
                        }
                      } catch (InterruptedException e) {
                        process.destroyForcibly();
                      }
                    }
                  }
                  System.out.println("All servers stopped.");
                }));

    try {
      System.out.println("=== OrionAlpha Unified Launcher ===");
      System.out.println("Configuration:");
      System.out.println("  - Login Server: enabled");
      System.out.println("  - Shop Server: " + (!noShop && !loginOnly ? "enabled" : "disabled"));
      System.out.println("  - Game Worlds: " + (loginOnly ? 0 : worlds));
      System.out.println();

      // Step 1: Start Login Server
      System.out.println("[1/4] Starting Login Server...");
      Process loginProcess = startProcess("login.LoginApp", "-Xmx200m");
      processes.add(loginProcess);
      Thread.sleep(5000);
      System.out.println("Login Server started.");

      if (loginOnly) {
        System.out.println("\nLogin-only mode: Skipping Game and Shop servers.");
        System.out.println("Press Ctrl+C to stop the server.");
        waitForProcesses();
        return;
      }

      // Step 2: Start Shop Server (if enabled)
      if (!noShop) {
        System.out.println("[2/4] Starting Shop Server...");
        Process shopProcess = startProcess("shop.ShopApp", "-Xmx200m");
        processes.add(shopProcess);
        Thread.sleep(2000);
        System.out.println("Shop Server started.");
      } else {
        System.out.println("[2/4] Shop Server disabled (--no-shop).");
      }

      // Step 3: Start Game Servers
      System.out.println("[3/4] Starting Game Server(s)...");
      for (int i = 0; i < worlds; i++) {
        System.out.println("  Starting Game World " + i + "...");
        Process gameProcess = startProcess("game.GameApp", "-Xmx400m", "-DgameID=" + i);
        processes.add(gameProcess);
        if (i < worlds - 1) {
          Thread.sleep(2000);
        }
      }
      System.out.println("Game Server(s) started.");

      // Step 4: All servers running
      System.out.println("[4/4] All servers are now running!");
      System.out.println("\nPress Ctrl+C to stop all servers.");

      // Wait for all processes to complete
      waitForProcesses();

    } catch (IOException e) {
      System.err.println("Failed to start server process: " + e.getMessage());
      e.printStackTrace();
      System.exit(1);
    } catch (InterruptedException e) {
      System.out.println("Launcher interrupted.");
      Thread.currentThread().interrupt();
    }
  }

  /**
   * Starts a server process with the specified main class and JVM arguments.
   *
   * @param mainClass The fully qualified main class name
   * @param jvmArgs Additional JVM arguments (e.g., "-Xmx400m", "-DgameID=0")
   * @return The started Process
   * @throws IOException if the process cannot be started
   */
  private static Process startProcess(String mainClass, String... jvmArgs) throws IOException {
    List<String> command = new ArrayList<>();

    // Get the Java executable path
    String javaHome = System.getProperty("java.home");
    String javaExec = javaHome + "/bin/java";
    command.add(javaExec);

    // Add JVM arguments
    for (String arg : jvmArgs) {
      command.add(arg);
    }

    // Add standard arguments
    command.add("-Dwzpath=" + DEFAULT_WZPATH);

    // Add classpath
    command.add("-cp");
    String classpath = System.getProperty("java.class.path");
    if (classpath == null || classpath.isEmpty()) {
      classpath = DEFAULT_CLASSPATH;
    }
    command.add(classpath);

    // Add main class
    command.add(mainClass);

    // Create and configure ProcessBuilder
    ProcessBuilder pb = new ProcessBuilder(command);
    pb.inheritIO(); // Redirect all output to parent process

    // Start the process
    return pb.start();
  }

  /**
   * Checks if a flag is present in the command-line arguments.
   *
   * @param args Command-line arguments
   * @param flag The flag to check for (e.g., "--no-shop")
   * @return true if the flag is present
   */
  private static boolean hasFlag(String[] args, String flag) {
    for (String arg : args) {
      if (arg.equalsIgnoreCase(flag)) {
        return true;
      }
    }
    return false;
  }

  /**
   * Gets the number of game worlds to start from command-line arguments.
   *
   * @param args Command-line arguments
   * @return The number of worlds (default 1)
   */
  private static int getWorldCount(String[] args) {
    for (String arg : args) {
      if (arg.startsWith("--worlds=")) {
        try {
          int worlds = Integer.parseInt(arg.substring("--worlds=".length()));
          if (worlds < 1) {
            System.err.println("Warning: Invalid world count '" + worlds + "', using default 1");
            return 1;
          }
          return worlds;
        } catch (NumberFormatException e) {
          System.err.println("Warning: Invalid world count format '" + arg + "', using default 1");
          return 1;
        }
      }
    }
    return 1; // Default to 1 world
  }

  /**
   * Waits for all server processes to complete. This keeps the launcher running until all servers
   * exit or are terminated.
   */
  private static void waitForProcesses() {
    for (Process process : processes) {
      try {
        process.waitFor();
      } catch (InterruptedException e) {
        Thread.currentThread().interrupt();
        break;
      }
    }
  }
}
