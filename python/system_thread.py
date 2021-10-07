import zlib
import zmq
import simplejson
import sys, os, datetime, time
import mysql.connector
import datetime
import threading
import signal

"""
 "  Configuration
"""
__relayEDDN             = 'tcp://eddn.edcd.io:9500'
__timeoutEDDN           = 600000

# Set False to listen to production stream
__debugEDDN             = False

# Set to False if you do not want verbose logging
__logVerboseFile        = os.path.dirname(__file__) + '/Logs_Verbose_EDDN_%DATE%.htm'
#__logVerboseFile        = False

# Set to False if you do not want JSON logging
__logJSONFile           = os.path.dirname(__file__) + '/Logs_JSON_EDDN_%DATE%.log'
#__logJSONFile           = False

# A sample list of authorised softwares
__authorisedSoftwares   = [
    "E:D Market Connector",
    "EDDiscovery",
    "EDDI",
    "EDCE",
    "ED-TD.SPACE",
    "EliteOCR",
    "Maddavo's Market Share",
    "RegulatedNoise",
    "RegulatedNoise__DJ",
    "E:D Market Connector [Windows]",
    "EDSM"
]

# Used this to excludes yourself for example has you don't want to handle your own messages ^^
__excludedSoftwares     = [
    'Helicorp'
]

"""
 "  Start
"""
def date(__format):
    d = datetime.datetime.utcnow()
    return d.strftime(__format)


__oldTime = False
def echoLog(__str):
    global __oldTime, __logVerboseFile

    if __logVerboseFile != False:
        __logVerboseFileParsed = __logVerboseFile.replace('%DATE%', str(date('%Y-%m-%d')))

    if __logVerboseFile != False and not os.path.exists(__logVerboseFileParsed):
        f = open(__logVerboseFileParsed, 'w')
        f.write('<style type="text/css">html { white-space: pre; font-family: Courier New,Courier,Lucida Sans Typewriter,Lucida Typewriter,monospace; }</style>')
        f.close()

    if (__oldTime == False) or (__oldTime != date('%H:%M:%S')):
        __oldTime = date('%H:%M:%S')
        __str = str(__oldTime)  + ' | ' + str(__str)
    else:
        __str = '        '  + ' | ' + str(__str)

    #print (__str)
    sys.stdout.flush()

    if __logVerboseFile != False:
        f = open('./__logVerboseFileParsed', 'a')
        f.write(__str + '\n')
        f.close()

def FSDJump(__json, mydb):
    mycursor = mydb.cursor(buffered=True)

    date = datetime.datetime.strptime(__json['message']['timestamp'], '%Y-%m-%dT%H:%M:%SZ')
    __json['message']['SystemGovernment'] = __json['message']['SystemGovernment'].replace('$government_', '')
    __json['message']['SystemGovernment'] = __json['message']['SystemGovernment'].replace(';', '')
    __json['message']['SystemEconomy'] = __json['message']['SystemEconomy'].replace('$economy_', '')
    __json['message']['SystemEconomy'] = __json['message']['SystemEconomy'].replace(';', '')
    __json['message']['SystemSecurity'] = __json['message']['SystemSecurity'].replace('$SYSTEM_SECURITY_', '')
    __json['message']['SystemSecurity'] = __json['message']['SystemSecurity'].replace(';', '')
    __json['message']['SystemSecurity'] = __json['message']['SystemSecurity'].replace('$GAlAXY_MAP_INFO_state_anarchy', 'anarchy')
    __json['message']['SystemSecurity'] = __json['message']['SystemSecurity'].replace(';', '')
    __json['message']['SystemSecondEconomy'] = __json['message']['SystemSecondEconomy'].replace('$economy_', '')
    __json['message']['SystemSecondEconomy'] = __json['message']['SystemSecondEconomy'].replace(';', '')
    __json['message']['StarSystem'] = __json['message']['StarSystem'].replace("'", "\\'")

    sql = "SELECT count(*), MAX(debut), StarSystem, SystemAllegiance, SystemEconomy, SystemGovernment FROM System WHERE SystemAdress = '" + str(__json['message']['SystemAddress']) + "' AND fin >= NOW()"
    mycursor.execute(sql)
    myresult = mycursor.fetchone()
    if int(myresult[0]) == 0:
        sql = "INSERT INTO System (StarSystem, SystemAllegiance, SystemEconomy, SystemGovernment, SystemSecurity, SystemFaction, SystemSecondEconomy, longitude, latitude, altitude, debut, SystemAdress) VALUES (LOWER(%s), LOWER(%s), LOWER(%s), LOWER(%s), LOWER(%s), LOWER(%s), LOWER(%s), %s, %s, %s, %s, %s)"
        if "SystemFaction" not in __json['message'].keys() :
            val = (__json['message']['StarSystem'], __json['message']['SystemAllegiance'], __json['message']['SystemEconomy'], __json['message']['SystemGovernment'], __json['message']['SystemSecurity'], "Empty",__json['message']['SystemSecondEconomy'], __json['message']['StarPos'][0], __json['message']['StarPos'][1], __json['message']['StarPos'][2], date, __json['message']['SystemAddress'])
            mycursor.execute(sql, val)
            mydb.commit()
        else :
            __json['message']['SystemFaction']['Name'] = __json['message']['SystemFaction']['Name'].replace("'", "\\'")
            val = (__json['message']['StarSystem'], __json['message']['SystemAllegiance'], __json['message']['SystemEconomy'], __json['message']['SystemGovernment'], __json['message']['SystemSecurity'], __json['message']['SystemFaction']['Name'], __json['message']['SystemSecondEconomy'], __json['message']['StarPos'][0], __json['message']['StarPos'][1], __json['message']['StarPos'][2], date, __json['message']['SystemAddress'])
            mycursor.execute(sql, val)
            mydb.commit()

    elif int(myresult[0]) != 0:
                        
        sql = "SELECT `System`.`StarSystem`,`System`.`SystemAllegiance`,`System`.`SystemEconomy`,`System`.`SystemGovernment`,`System`.`SystemSecurity`, `System`.`SystemFaction`, `System`.idSystem FROM `elite`.`System` WHERE SystemAdress = '" + str(__json['message']['SystemAddress']) + "' AND Fin >= NOW()"
        mycursor.execute(sql)
        dernierEnregistrement = mycursor.fetchone()

        if "SystemFaction" not in __json['message'].keys() :
            if dernierEnregistrement[0] != __json['message']['StarSystem'].lower() or dernierEnregistrement[1] != __json['message']['SystemAllegiance'].lower() or dernierEnregistrement[2] != __json['message']['SystemEconomy'].lower() or dernierEnregistrement[3] != __json['message']['SystemGovernment'].lower() or dernierEnregistrement[4] != __json['message']['SystemSecurity'].lower():
                sql = 'UPDATE `elite`.`System` SET FIN = NOW() WHERE `idSystem` = ' + str(dernierEnregistrement[6])
                mycursor.execute(sql)
                mydb.commit()

                sql = "INSERT INTO System (StarSystem, SystemAllegiance, SystemEconomy, SystemGovernment, SystemSecurity, SystemFaction, SystemSecondEconomy, longitude, latitude, altitude, debut, SystemAdress) VALUES (LOWER(%s), LOWER(%s), LOWER(%s), LOWER(%s), LOWER(%s), LOWER(%s), LOWER(%s), %s, %s, %s, %s, %s)"
                val = (__json['message']['StarSystem'], __json['message']['SystemAllegiance'], __json['message']['SystemEconomy'], __json['message']['SystemGovernment'], __json['message']['SystemSecurity'], "Empty",__json['message']['SystemSecondEconomy'], __json['message']['StarPos'][0], __json['message']['StarPos'][1], __json['message']['StarPos'][2], date, __json['message']['SystemAddress'])
                mycursor.execute(sql, val)
                mydb.commit()

        else :
            if dernierEnregistrement[0] != __json['message']['StarSystem'].lower() or dernierEnregistrement[1] != __json['message']['SystemAllegiance'].lower() or dernierEnregistrement[2] != __json['message']['SystemEconomy'].lower() or dernierEnregistrement[3] != __json['message']['SystemGovernment'].lower() or dernierEnregistrement[4] != __json['message']['SystemSecurity'].lower() or dernierEnregistrement[5] != __json['message']['SystemFaction']['Name'].lower():
                sql = 'UPDATE `elite`.`System` SET FIN = NOW() WHERE `idSystem` = ' + str(dernierEnregistrement[6])
                # print(sql)
                mycursor.execute(sql)
                mydb.commit()

                sql = "INSERT INTO System (StarSystem, SystemAllegiance, SystemEconomy, SystemGovernment, SystemSecurity, SystemFaction, SystemSecondEconomy, longitude, latitude, altitude, debut, SystemAdress) VALUES (LOWER(%s), LOWER(%s), LOWER(%s), LOWER(%s), LOWER(%s), LOWER(%s), LOWER(%s), %s, %s, %s, %s, %s)"
                __json['message']['SystemFaction']['Name'] = __json['message']['SystemFaction']['Name'].replace("'", "\\'")
                val = (__json['message']['StarSystem'], __json['message']['SystemAllegiance'], __json['message']['SystemEconomy'], __json['message']['SystemGovernment'], __json['message']['SystemSecurity'], __json['message']['SystemFaction']['Name'], __json['message']['SystemSecondEconomy'], __json['message']['StarPos'][0], __json['message']['StarPos'][1], __json['message']['StarPos'][2], date, __json['message']['SystemAddress'])
                mycursor.execute(sql, val)
                mydb.commit()

    sql = "SELECT count(*) FROM User WHERE UploaderID = '" + str(__json['header']['uploaderID']) +"'"
    mycursor.execute(sql)
    myresult = mycursor.fetchone()

    if int(myresult[0]) == 0:
        sql = "INSERT INTO User (UploaderID) VALUES ('" + str(__json['header']['uploaderID']) + "')" 
        mycursor.execute(sql)
        mydb.commit()
        sql = "SELECT distinct last_insert_id() FROM User"
        mycursor.execute(sql)
        lastUserInsert = mycursor.fetchone()
        sql = "INSERT INTO User_system (IdUser, SystemAddress, Date) VALUES (%s, %s, %s)"
        val = (lastUserInsert[0], __json['message']['SystemAddress'], date)
        mycursor.execute(sql, val)
        mydb.commit()
    else :
        sql = "SELECT distinct idUser FROM User WHERE UploaderID = '" + str(__json['header']['uploaderID']) + "'"
        mycursor.execute(sql)
        UserId = mycursor.fetchone()
        sql = "INSERT INTO User_system (IdUser, SystemAddress, Date) VALUES (%s, %s, %s)"
        val = (UserId[0], __json['message']['SystemAddress'], date)
        mycursor.execute(sql, val)
        mydb.commit()
    mydb.close()
    
def SAASignalsFound(__json,mydb):

    __json['message']['StarSystem'] = __json['message']['StarSystem'].replace("'", "\\'")
    __json['message']['BodyName'] = __json['message']['BodyName'].replace("'", "\\'")
    mycursor = mydb.cursor(buffered=True)
    # print("Location recu")
    # print(__json)
    for i in range(len(__json['message']['Signals'])):
        # print(__json['message']['Signals'][i]['Type'])
        if '$' not in str(__json['message']['Signals'][i]['Type']):
            sql = "SELECT count(*) FROM Signals_mine WHERE Type <> '" + str(__json['message']['Signals'][i]['Type']) + "' AND '" + str(__json['message']['SystemAddress']) + "' AND '" + __json['message']['BodyName'] + "'"
            mycursor.execute(sql)
            myresult = mycursor.fetchone()

            if int(myresult[0]) == 0:
                sql = "INSERT INTO Signals_mine (Type, SystemAddress, Body, nombre) VALUES ('" + __json['message']['Signals'][i]['Type'] + "', '" + str(__json['message']['SystemAddress']) + "', '" + __json['message']['BodyName'] + "', '" + str(__json['message']['Signals'][i]['Count']) + "')"
                # print(sql)
                mycursor.execute(sql)
                mydb.commit()

        if '$' in str(__json['message']['Signals'][i]['Type']):
            sql = "SELECT count(*) FROM Signals_other WHERE Type <> '" + str(__json['message']['Signals'][i]['Type']) + "' AND '" + str(__json['message']['SystemAddress']) + "' AND '" + __json['message']['BodyName'] + "'"
            mycursor.execute(sql)
            myresult = mycursor.fetchone()

            if int(myresult[0]) == 0:
                sql = "INSERT INTO Signals_other (Type, SystemAddress, Body, nombre) VALUES ('" + __json['message']['Signals'][i]['Type'] + "', '" + str(__json['message']['SystemAddress']) + "', '" + __json['message']['BodyName'] + "', '" + str(__json['message']['Signals'][i]['Count']) + "')"
                # print(sql)
                mycursor.execute(sql)
                mydb.commit()


def inject(__message):
        __message   = zlib.decompress(__message)
        __json      = simplejson.loads(__message)
        __converted = False
        if __json['$schemaRef'] == 'https://eddn.edcd.io/schemas/journal/1' + ('/test' if (__debugEDDN == True) else ''):
            mydb = mysql.connector.connect(
            host="192.168.1.29",
            port="3306",
            user="utilisateur",
            password="root",
            database="elite"
            )
            __authorised = False
            __excluded   = False
            if __json['header']['softwareName'] in __authorisedSoftwares:
                __authorised = True
            if __json['header']['softwareName'] in __excludedSoftwares:
                __excluded = True
            if __authorised == True and __excluded == False:
            # Do what you want with the data...
            # Have fun !
                if __json['message']['event'] == "FSDJump":
                    FSDJump(__json, mydb)
                    del __converted
                
                elif __json['message']['event'] == "SAASignalsFound":
                    SAASignalsFound(__json, mydb)
                    del __converted

                """elif __json['message']['event'] == "Location":
                    print(__json)
                    del __converted"""

def keyboardInterruptHandler(signal, frame):
    print("KeyboardInterrupt (ID: {}) has been caught. Cleaning up...".format(signal))
    exit(0)

def main():
    context     = zmq.Context()
    subscriber  = context.socket(zmq.SUB)

    subscriber.setsockopt(zmq.SUBSCRIBE, b"")
    subscriber.setsockopt(zmq.RCVTIMEO, __timeoutEDDN)

    while True:
        try:
            subscriber.connect(__relayEDDN)

            while True:
                __message   = subscriber.recv()
                thread = threading.Thread(target = inject, args = (__message, ))
                thread.start()
                signal.signal(signal.SIGINT, keyboardInterruptHandler)
                if __message == False:
                    subscriber.disconnect(__relayEDDN)
                    break
        except zmq.ZMQError:
            subscriber.disconnect(__relayEDDN)
            time.sleep(5)



if __name__ == '__main__':
    main()
