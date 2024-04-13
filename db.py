import mariadb
import os
from dotenv import load_dotenv
import sys
load_dotenv()

con = mariadb.connect(host="localhost",
                      port=3306,
                      password=os.getenv('password'),
                      user="root",
                      database="aicybot")

cursor = con.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS `april` (`guild` BIGINT(20) NOT NULL,`channel` BIGINT(20) NULL DEFAULT NULL,UNIQUE INDEX `guild` (`guild`));")
cursor.execute("CREATE TABLE IF NOT EXISTS `bot` (`guild` BIGINT(20) NOT NULL,`role` BIGINT(20) NULL DEFAULT NULL,UNIQUE INDEX `guild` (`guild`) USING BTREE)")
cursor.execute("CREATE TABLE IF NOT EXISTS `spotify` (`guild` BIGINT(20) NULL DEFAULT NULL,`channel` BIGINT(20) NULL DEFAULT NULL)")
con.commit()

sys.exit(0)