# OrionAlpha
OrionAlpha - A Nexon Replica Emulator Project

----------------------------------------------------------------------
## Resources
 * You can download the game and client [here](https://mega.nz/#!O9Vy3C7Q!0FsLIilRwzImzjUY_9MxOqtvA4wuMn0SDWE65BkGHZk)
 * To emulate a korean locale in the client, you can download LocaleEmulator [here](https://mega.nz/#!T5t00IwA!YByix3DVt-_Pi0IpU-OwUnvhCDyZEPz4JQ6S-kbYHks)
 * You can download the named client IDB [here](https://mega.nz/#!KgdRna6Q!T5Op7_b_JF62QEvHqeYFp2NJcEYeoigqFdOHpREf5pI)
## Requirements/Dependencies
 * Java JDK (21 or higher)
 * javax.json 1.1.4
 * Netty 4.2.9.Final
 * HikariCP 5.1.0
 * MariaDB Connector/J 3.4.0
 * slf4j 2.0.17
 * GraalPy 24.1.1 (Python 3.12 compatible)
 * favr.lib.BCrypt 0.9.0
 ----------------------------------------------------------------------
 ## Building the Project
 
 ### Using Maven
 
 Build the project using Maven:
 ```bash
 mvn clean package
 ```
 
 Or use the Maven Wrapper (recommended for consistent builds):
 ```bash
 ./mvnw clean package
 ```
 
 On Windows:
 ```cmd
 mvnw.cmd clean package
 ```
 
 ### Code Formatting with Spotless
 
 This project uses [Spotless](https://github.com/diffplug/spotless) with Google Java Format for consistent code formatting.
 
 **Check code formatting:**
 ```bash
 mvn spotless:check
 # or
 ./mvnw spotless:check
 ```
 
 **Apply code formatting:**
 ```bash
 mvn spotless:apply
 # or
 ./mvnw spotless:apply
 ```
 
 ### Code Modernization with OpenRewrite
 
 This project includes [OpenRewrite](https://docs.openrewrite.org/) recipes for automated code modernization, including:
 
 - **Java 21 Migration**: Upgrades code through Java 6→7→8→11→17→21
 - **Netty 4.2 Migration**: Updates Netty API usage from 4.1 to 4.2
 - **Static Analysis**: Applies common code quality improvements
 - **Security Fixes**: Implements OWASP Top 10 security best practices
 - **API Modernization**: Updates to modern Java APIs (NIO, concurrency, etc.)
 
 **Dry run (preview changes without applying):**
 ```bash
 mvn rewrite:dryRun
 # or
 ./mvnw rewrite:dryRun
 ```
 
 **Apply modernization recipes:**
 ```bash
 mvn rewrite:run
 # or
 ./mvnw rewrite:run
 ```
 
 **Run a specific recipe:**
 ```bash
 mvn rewrite:run -Drewrite.activeRecipes=org.openrewrite.java.security.OwaspTopTen
 ```
 
 **Use the custom OrionAlpha composite recipe** (defined in `rewrite.yml`):
 ```bash
 mvn rewrite:run -Drewrite.activeRecipes=com.orionalpha.Modernize
 ```
 
 For more information on available recipes, see the [OpenRewrite documentation](https://docs.openrewrite.org/).
 
 ----------------------------------------------------------------------
 ## Architecture
 The OrionAlpha Emulator is split up into two parts: *Login*, and *Game*, each executing on their own thread. 
 
 **Login** is the central server which will have connectivity to each world and can migrate you back and forth. 
 
 **Game** is designed to be each world, and takes the JVM argument `-DgameID=X` to define which world it is. Each Game JVM that controls the world will also control all of its channels (thus, no multi-jvm here).
 
 ----------------------------------------------------------------------
 ## Server Configuration
 Located within the root of the emulator are a few configuration files:
  * Game0, Game1, etc is used to configure each World.
  * Login is used to configure the Login.
  * Shop is used to configure the Cash Shop.
  * Database is used to configure the connection to the database.
  
  The configuration is done within JSON; each property is defined as a key (string), and a value (int or string).
  Below will further explain the defintions of most of the properties used.
  
  Login/Game/Shop:
  * `port` -> The port to be binded for the server's connection acceptor.
  * `centerPort` -> The private port of your login server that connects JVMs together.
  * `PublicIP` -> The public IP address users will connect to.
  * `PrivateIP` -> The private IP address that connects the JVMs together.
  
  Database:
  * `dbPort` -> The port to connect to your database.
  * `dbGameWorld` -> The Schema name of the active database that the emulator connects to.
  * `dbGameWorldSource` -> The IP/hostname to connect to your database.
  * `dbGameWorldInfo` -> The username/password of your database, separated by comma. (e.g "root,password")
  
  Game:
  * `gameWorldId` -> The ID of the world (0 = Scania, 1 = Bera, etc).
  * `channelNo` -> The number of channels for the world.
  * `incExpRate` -> The server's Experience Rate modifier. We use Nexon's standard. (e.g 100 = 1x, 250 = 2.5x, etc)
  * `incMesoRate` -> The server's Meso Rate modifier (Nexon standard).
  * `incDropRate` -> The server's Drop Rate modifier (Nexon standard).
  * `worldName` -> The name of the world. This is sent to and displayed in the login server.
  ----------------------------------------------------------------------
  ## Quest System

OrionAlpha includes a comprehensive quest tracking system.

### Database Tables

The quest system uses three tables:
- `questrecord` - Quest states (not started, started, completed)
- `questmobkill` - Kill quest progress tracking
- `questitemcollect` - Collection quest progress tracking

### Installation

Run the quest system schema:
```bash
mysql -u root -p orionalpha < sql/quest_system.sql
```

Or manually execute the SQL statements from `sql/quest_system.sql` in your database client.

### Script API

Available quest functions in NPC scripts (Python):

```python
# Check quest state (0=not started, 1=started, 2=completed)
state = self.questRecordGetState(questID)

# Start a quest
self.questRecordSet(questID, "start")

# Complete a quest
self.questRecordSet(questID, "complete")

# Reset a quest
self.questRecordSet(questID, "reset")

# Check if started/completed
if self.questRecordIsStarted(questID):
    # Quest is in progress
    pass

if self.questRecordIsCompleted(questID):
    # Quest is completed
    pass

# Custom quest data (for storing quest-specific information)
self.questRecordSetData(questID, "somedata")
data = self.questRecordGetData(questID)

# Mob kill tracking (for "kill X mobs" quests)
count = self.questMobKillGet(questID, mobID)
self.questMobKillIncrement(questID, mobID)
```

### Example Usage

**Starting a quest when player accepts:**
```python
ret = self.askYesNo("Would you like to help me?")
if ret == True:
    self.questRecordSet(1000, "start")
    self.say("Thank you! Go collect 10 mushrooms for me.")
```

**Completing a quest:**
```python
if self.inventoryGetItemCount(4000000) >= 10:
    self.inventoryExchange(0, [4000000, -10])  # Remove items
    self.questRecordSet(1000, "complete")
    self.userIncEXP(100, False)
    self.say("Thank you for your help!")
```

**Checking quest progress:**
```python
if self.questRecordIsStarted(1000):
    self.say("How's the mushroom collection going?")
elif self.questRecordIsCompleted(1000):
    self.say("Thanks again for helping me!")
else:
    self.say("Would you like to help me collect mushrooms?")
```

### Testing

After implementation:
1. Create a test character
2. Talk to NPCs to start quests (e.g., Heena in Maple Island)
3. Check database: `SELECT * FROM questrecord WHERE CharacterID = ?;`
4. Complete quest requirements
5. Verify quest completion in database

  ----------------------------------------------------------------------
  ## Database Configuration

### HikariCP Connection Pool

OrionAlpha uses HikariCP 5.1.0 for high-performance database connection pooling.

#### Configuration
Pool settings can be tuned in `UnifiedDB.java`:
- **Maximum Pool Size**: 20 connections (default)
- **Minimum Idle**: 5 connections
- **Connection Timeout**: 30 seconds
- **Idle Timeout**: 10 minutes
- **Max Lifetime**: 30 minutes
- **Keepalive**: 5 minutes

#### Performance Features
- PreparedStatement caching (250 statements, 2048 SQL limit)
- Batch statement rewriting for faster inserts
- Result metadata caching
- Server configuration caching
- Unicode support (utf8mb4)

#### Development Tools
Enable connection leak detection:
```bash
java -Dhikari.leakDetection=true -jar OrionAlpha.jar
```
This will log warnings if connections are held for more than 60 seconds.

#### Monitoring
The connection pool is named `OrionAlpha-DB-Pool` for easy identification in logs and monitoring tools.
  ----------------------------------------------------------------------
  ## Client Modifications
  Even knowing there's barely anything to edit in such an early version, below are helpful client edits.
  
  ### Modifying IP
  If you intend to use OrionAlpha, you can change the IP in either our client or the clean client.
   * Our client's default IP is `127.0.0.1`
   * Nexon's default IP's are `218.153.9.172` and `218.153.9.173`
  
  ### Enable Multi-Client
  Allow multiple clients to be open/executed simultaneously.
   * Change the instruction at address `005872D9` to `jmp 0058732D`
  
  ### Enable Window Mode
  Forces the client to execute only in Window Mode, and not Full Screen. 
  * Change the instruction at address `00589F92` to `mov dword ptr [esp+0x84], 0x0`
  
  ### Modifying Client Resolution
  Allows you to make the dimensions of the game bigger, for example 1024x768.
  * Change the instruction at address `0058A05E` to `push 0x320` where `0x320` is the Width
  * Change the instruction at address `0058A04F` to `push 0x258` where `0x258` is the Height
  
  ### Activate Chat Repeat Bypass
  Allows you to send the same message into the chat more than 3 times without any issue.
  * Change the instruction at address `00444261` to `jmp 004442A4`
  
  ### Activate Chat Spam Bypass
  Allows you to spam messages constantly without having to wait 2 seconds.
  * Change the instruction at address `004442C8` to `jmp 0044431B`
  
  ### Enable Infinite Text
  Allows you to type as many characters as you want into a single message, literally.
  * Change the instruction at address `0051E38D` to `mov dword ptr [esp+0xC8], 0xFF` where `0xFF` is the maximum
  
  ### Enable Swear Filter
  Allows you to enter curse words without getting a pop-up and restricting your message from sending.
  * Change the instruction at address `004441B8` to `jmp 004441ED`
  
  ### Remove Nexon ADs
  Allows you to disable the ad balloons after closing the client because they're annoying.
  * Change the instruction at address `005878A5` to `nop`
  
  ### Enable Droppable NX
  Allows you to drop cash NX items like any other item.
  * Change the instruction at address `0047965A` to `nop`
  * Change the instruction at address `00479666` to `nop`
  
  ----------------------------------------------------------------------
  ## Performance Optimization
  
  ### Native Transports
  
  OrionAlpha automatically detects and uses the best available Netty transport for your platform:
  
  - **Linux (x86_64/aarch64)**: Epoll native transport (20-30% better performance)
  - **macOS (x86_64/aarch64)**: KQueue native transport (optimized for macOS)
  - **Windows**: NIO transport (automatic fallback)
  
  The server will log which transport is being used at startup.
  
  ### Recommended Deployment
  
  For production game servers:
  - **Linux**: Preferred platform for best performance (Epoll)
  - **Windows**: Fully supported for development/testing (NIO)
  
  ### Channel Options
  
  The server is configured with optimized settings for game server workloads:
  - TCP_NODELAY enabled (Nagle's algorithm disabled for low latency)
  - 64KB send/receive buffers
  - Pooled ByteBuf allocation for reduced GC pressure
  - Write buffer water marks to prevent memory exhaustion under load
  
  ----------------------------------------------------------------------
  ### Re-Enable Admin Actions
  Restores the ability to allow GM/Admins to drop items, mesos, etc.
  * Change the instruction at address `004795D2` to `jmp 004795E9`
  * Change the instruction at address `005002E7` to `jmp 00500318`
  
  ### Modifying Damage Cap
  Allows you to extend the damage cap up to a maximum of `32,767`.
  * Change the instruction at address `005C3E98` to `13337.0` where `13337.0` is the new cap
  
  ### Modifying Meso Cap
  Allows you to drop meso bags exceeding 50,000 by setting a new cap.
  * Change the instruction at address `005003CE` to `cmp eax, 0xC350` where `0xC350` is the new max
  * Change the instruction at address `005003D5` to `mov eax, 0xC350` where `0xC350` is the new max
  
