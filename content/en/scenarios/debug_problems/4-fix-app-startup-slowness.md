---
title: Fix Application Startup Slowness
linkTitle: 5.4 Fix Application Startup Slowness
weight: 4
time: 10 minutes
---

In this section, we'll use what we learned from the profiling data in **Splunk Observability Cloud** to resolve the slowness we saw when starting our application. 

### Examining the Source Code

Open the corresponding source file once again (`./doorgame/src/main/java/com/splunk/profiling/workshop/UserData.java`) and focus on the following code:

````
public class UserData {

    static final String DB_URL = "jdbc:mysql://mysql/DoorGameDB";
    static final String USER = "root";
    static final String PASS = System.getenv("MYSQL_ROOT_PASSWORD");
    static final String SELECT_QUERY = "select * FROM DoorGameDB.Users, DoorGameDB.Organizations";

    HashMap<String, User> users;

    public UserData() {
        users = new HashMap<String, User>();
    }

    public void loadUserData() {

        // Load user data from the database and store it in a map
        Connection conn = null;
        Statement stmt = null;
        ResultSet rs = null;

        try{
            conn = DriverManager.getConnection(DB_URL, USER, PASS);
            stmt = conn.createStatement();
            rs = stmt.executeQuery(SELECT_QUERY);
            while (rs.next()) {
                User user = new User(rs.getString("UserId"), rs.getString("FirstName"), rs.getString("LastName"));
                users.put(rs.getString("UserId"), user);
            }
````

After speaking with a database engineer, you discover that the SQL query being executed includes a cartesian join: 

````
select * FROM DoorGameDB.Users, DoorGameDB.Organizations
````

Cartesian joins are notoriously slow, and shouldn't be used, in general.  

Upon further investigation, you discover that there are 10,000 rows in the user table, and 1,000 rows in the organization table. When we execute a cartesian join using both of these tables, we end up with 10,000 x 1,000 rows being returned, which is 10,000,000 rows! 

Furthermore, the query ends up returning duplicate user data, since each record in the user table is repeated for each organization. 

So when our code executes this query, it tries to load 10,000,000 user objects into the HashMap, which explains why it takes so long to execute, and why it consumes so much heap memory.

### Let's Fix That Bug

After consulting the engineer that originally wrote this code, we determined that the join with the Organizations table was inadvertent. 

So when loading the users into the HashMap, we simply need to remove this table from the query. 

Open the corresponding source file once again (`./doorgame/src/main/java/com/splunk/profiling/workshop/UserData.java`) and change the following line of code: 

``` java
    static final String SELECT_QUERY = "select * FROM DoorGameDB.Users, DoorGameDB.Organizations";
```

to: 

``` java
    static final String SELECT_QUERY = "select * FROM DoorGameDB.Users";
```

Now the method should perform much more quickly, and less memory should be used, as it's loading the correct number of users into the HashMap (10,000 instead of 10,000,000). 

### Rebuild and Redeploy Application

Let's test our changes by using the following commands to re-build and re-deploy the Door Game application: 

``` bash
cd workshop/profiling
./5-redeploy-doorgame.sh
```

Once the application has been redeployed successfully, visit The Door Game again to confirm that your fix is in place:
`http://<your IP address>:81`

Clicking `Let's Play` should take us to the game more quickly now (though performance could still be improved):   

![Choose Door](../images/door_game_choose_door.png)

Start the game a few more times, then return to **Splunk Observability Cloud** to confirm that the latency of the `GET new-game` operation has decreased. 

## What did we accomplish?

* We discovered why our SQL query was so slow. 
* We applied a fix, then rebuilt and redeployed our application. 
* We confirmed that the application starts a new game more quickly.  

In the next section, we'll explore continue playing the game and fix any remaining performance issues that we find. 