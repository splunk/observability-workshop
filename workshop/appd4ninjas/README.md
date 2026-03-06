## AppD for Rookies

These are the instructions for AppD for Rookies.

## Setup
```bash
mkdir /opt/appdynamics
```
Place these files in that directory

### Java 1.8

```bash
sudo apt-get update 
sudo apt-get install -y openjdk-8-jdk 
update-java-alternatives -l 
java -version
# If the correct version isn't returning from the last command you can change it and check again
sudo update-java-alternatives --set /usr/lib/jvm/java-1.8.0-openjdk-amd64 
java -version 
```

### MySQL

```bash
sudo apt-get -y install libncurses5 
# Config User 
sudo groupadd mysql 
sudo useradd -r -g mysql -s /bin/false mysql 

# Install 
cd /opt/appdynamics 
mkdir mysql 
cd /opt/appdynamics/mysql 
wget https://downloads.mysql.com/archives/get/p/23/file/mysql-5.7.44-linux-glibc2.12-x86_64.tar.gz 
cd /usr/local 
sudo tar xvf /opt/appdynamics/mysql/mysql-5.7.44-linux-glibc2.12-x86_64.tar.gz 
sudo ln -s mysql-5.7.44-linux-glibc2.12-x86_64 mysql 
# May be unnecessary, but just in case
#cd /opt/appdynamics/mysql 
#sudo mkdir mysql-files 
#sudo chown mysql:mysql mysql-files 
#sudo chmod 750 mysql-files 

# Post-install config 
sudo /usr/local/mysql/bin/mysqld --initialize --user=mysql 
# If it asks, enter the password
# After it runs, note password,
# e.g. A temporary password is generated for root@localhost: qsbrp6_.ir(D 
sudo /usr/local/mysql/bin/mysql_ssl_rsa_setup 
sudo /usr/local/mysql/bin/mysqld_safe --user=mysql & 
/usr/local/mysql/bin/mysql_secure_installation 
# Enter password you noted earlier 
# New password: Welcome1! (for example)
# Validate Password plugin: n (default) 
# Change the password for root: n (default) 
# Remove anonymous user: n (default) 
# Disallow root login remotely: n (default) 
# Remove test database: n (default) 
# Reload privilege tables now: y (*** must type ***) 
 
# Add lab tables (change pw below if needed)
cd /opt/appdynamics/db-scripts
./create_sql_files.sh
/usr/local/mysql/bin/mysql -u root -pWelcome1! < mysql-01.sql 
/usr/local/mysql/bin/mysql -u root -pWelcome1! < mysql-02.sql 
/usr/local/mysql/bin/mysql -u root -pWelcome1! < mysql-03.sql 
/usr/local/mysql/bin/mysql -u root -pWelcome1! < mysql-04.sql 
```

### Tomcat

```bash
cd /usr/local
sudo mkdir apache
cd /usr/local/apache
sudo wget https://archive.apache.org/dist/tomcat/tomcat-9/v9.0.50/bin/apache-tomcat-9.0.50.tar.gz
sudo tar -zxpvf apache-tomcat-9.0.50.tar.gz -C /usr/local/apache
sudo chown -R splunk:splunk /usr/local/apache
mv apache-tomcat-9.0.50 apache-tomcat-9
echo "export CATALINA_HOME='/usr/local/apache/apache-tomcat-9/'" >> ~/.bashrc 
# Exit from the terminal
# Then ssh back in
vi /usr/local/apache/apache-tomcat-9/conf/tomcat-users.xml

# Add the following just before the last </tomcat-users> line:
<!-- User who can access only manager section --> <role rolename="manager-gui" /> <user username="admin" password="welcome1" roles="manager-gui" />
# Exit/save 
vi /usr/local/apache/apache-tomcat-9/webapps/manager/META-INF/context.xml

# Comment out the valve tag, like this 
<!-- <Valve className="org.apache.catalina.valves.RemoteAddrValve" allow="127\.\d+\.\d+\.\d+|::1|0:0:0:0:0:0:0:1" /> --> 
# Exit/save 
# Startup tomcat 
cd /usr/local/apache/apache-tomcat-9/bin
./startup.sh 

# Verify it is up (NOTE: firewall may prevent external access) 
curl localhost:8080
```

If you need to redirect to another port (like 8443):
- Go to tomcat: `cd /usr/local/apache/apache-tomcat-9/bin`
- Shutdown tomcat: `shutdown.sh`
- Edit `/usr/local/apache/apache-tomcat-9/conf/server.xml`
- Change port `8000` to `8443`, for example
- `startup.sh`
- Confirm you can see it: `curl localhost:8443`

### PhantomJS

```bash
udo apt-get update 
sudo apt-get install -y build-essential chrpath libssl-dev libxft-dev 
sudo apt-get install -y libfreetype6 libfreetype6-dev 
sudo apt-get install -y libfontconfig1 libfontconfig1-dev 
cd /opt/appdynamics
wget https://bitbucket.org/ariya/phantomjs/downloads/phantomjs-2.1.1-linux-x86_64.tar.bz2 
sudo tar xvjf phantomjs-2.1.1-linux-x86_64.tar.bz2 -C /usr/local/share/ 
sudo ln -sf /usr/local/share/phantomjs-2.1.1-linux-x86_64/bin/phantomjs /usr/local/bin 
export OPENSSL_CONF=/dev/null 
phantomjs --version 
```

### Install Application
- Unzip `app-war-file/Supercar-Trader.zip` to `app-war-file/Supercar-Trader.war`
- Navigate to Tomcat manager, e.g. http://[address]:8080/
- Click Manager App 
- user: admin, password: welcome1
- Fill in the form
    - Context Path: /Supercar-Trader
    - WAR or Directory Path: file://opt/appdynamics/app-war-file/Supercar-Trader.war
    - Leave other fields blank
    - Click Deploy
- Right-click on the app (path) and open in a new tab. You should see the app.

After this it would be advised to:
- Remove the admin user you created in tomcat
- change the foldername of the manager, from:
 `/usr/local/apache/apache-tomcat-9/webapps/ROOT`
 to
 `/usr/local/apache/apache-tomcat-9/webapps/ROOThidden`
 and restarting Tomcat.

### Start loadgen

```bash
sudo chmod 754 /opt/appdynamics/loadgen/*.sh
# Clean linefeeds
sed -i -e 's/\r$//' /opt/appdynamics/loadgen/*.sh
# If you changed the port in tomcat, use this to change the port
sed -i -e 's/8080/8443/g' /opt/appdynamics/loadgen/*.js 
# Start the loadgen 
cd /opt/appdynamics/loadgen
./start_load.sh 
```