'''
==============
3D scatterplot
==============

Demonstration of a basic scatterplot in 3D.
'''

# This import registers the 3D projection, but is otherwise unused.
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 unused import

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import mysql.connector

mydb = mysql.connector.connect(
        host="192.168.1.29",
        port="3306",
        user="utilisateur",
        password="root",
        database="elite",
        auth_plugin='mysql_native_password'
        )

fig = plt.figure()

# For each set of style and range settings, plot n random points in the box
# defined by x in [23, 32], y in [0, 100], z in [zlow, zhigh].

df_mysql = pd.read_sql('select * from elite.System;', con=mydb)  
df2_mysql = pd.DataFrame(df_mysql)  
print ('loaded dataframe from MySQL. records:', len(df2_mysql))
mydb.close()

print(df2_mysql.sample())

ax = fig.add_subplot(111, projection='3d')

ax.scatter(df2_mysql["Longitude"],df2_mysql[["Latitude"]],df2_mysql[["Altitude"]])

ax.set_xlabel('X Label')
ax.set_ylabel('Y Label')
ax.set_zlabel('Z Label')

plt.show()
