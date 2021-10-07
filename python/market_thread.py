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

def inject(__message):
        mydb = mysql.connector.connect(
        host="192.168.1.29",
        port="3306",
        user="utilisateur",
        password="root",
        database="elite"
        )
        # # echoLog('Got a message')
        __message   = zlib.decompress(__message)
        #if __message == False:
            # echoLog('Failed to decompress message')
        __json      = simplejson.loads(__message)
        #if __json == False:
            # echoLog('Failed to parse message as json')
        __converted = False
        if __json['$schemaRef'] == 'https://eddn.edcd.io/schemas/journal/1' + ('/test' if (__debugEDDN == True) else ''):
            # # echoLogJSON(__message)
            # echoLog('Receiving commodity-v1 message...')
            # echoLog('    - Converting to v3...')
            #print('journal recu')
            __authorised = False
            __excluded   = False
            if __json['header']['softwareName'] in __authorisedSoftwares:
                __authorised = True
            if __json['header']['softwareName'] in __excludedSoftwares:
                __excluded = True
            if __authorised == True and __excluded == False:
            # Do what you want with the data...
            # Have fun !
                if __json['message']['event'] == "Docked":
                    # inject(__json)
                    #print(__json)
                    mycursor = mydb.cursor()
                    date = datetime.datetime.strptime(__json['message']['timestamp'], '%Y-%m-%dT%H:%M:%SZ')
                    #print("message docked")
                    __json['message']['StationGovernment'] = __json['message']['StationGovernment'].replace('$government_', '')
                    __json['message']['StationGovernment'] = __json['message']['StationGovernment'].replace(';', '')
                    sql = "SELECT count(*), MAX(debut), StationAllegiance, StationGovernement, StationSystem FROM Market WHERE idMarket = " + str(__json['message']['MarketID']) + " AND fin >= NOW()"
                    # #print(sql)
                    mycursor.execute(sql)
                    # #print(sql,val)
                    myresult = mycursor.fetchone()
                    if int(myresult[0]) == 0:
                        sql = "INSERT INTO Market (idMarket, StationName, StationType, StationSystem, StationAllegiance, StationGovernement, debut) VALUES (%s, LOWER(%s), LOWER(%s), LOWER(%s), LOWER(%s), LOWER(%s), %s)"
                        val = (__json['message']['MarketID'], __json['message']['StationName'], __json['message']['StationType'], __json['message']['StarSystem'], __json['message']['StationFaction']['Name'],__json['message']['StationGovernment'], date)
                        mycursor.execute(sql, val)
                        mydb.commit()
                        #print(mycursor.rowcount, "record inserted.")
                    elif int(myresult[0]) != 0:
                        #print('donnee doublons recu')
                        if myresult[1] < date:
                            if myresult[2] != __json['message']['StationFaction']['Name'].lower() or myresult[3] != __json['message']['StationGovernment'].lower() or myresult[4] != __json['message']['StarSystem'].lower():
                                #print('Changement detecter')
                                sql = "UPDATE Market SET Fin = Now() WHERE idMarket = " + str(__json['message']['MarketID']) + " AND Fin = '9999-12-31'"
                                #print(sql)
                                mycursor.execute(sql)
                                mydb.commit()
                                #print(mycursor.rowcount, "record updated.")
                                sql = "INSERT INTO Market (idMarket, StationName, StationType, StationSystem, StationAllegiance, StationGovernement, debut) VALUES (%s, LOWER(%s), LOWER(%s), LOWER(%s), LOWER(%s), LOWER(%s), %s)"
                                val = (__json['message']['MarketID'], __json['message']['StationName'], __json['message']['StationType'], __json['message']['StarSystem'], __json['message']['StationFaction']['Name'],__json['message']['StationGovernment'], date)
                                mycursor.execute(sql, val)
                                mydb.commit()
                                #print(mycursor.rowcount, "record inserted.")
                                # f = open("suivi.txt", "a")
                                # f.write(myresult[2] + ' ' + __json['message']['StationFaction']['Name'].lower()  + ' ' +  myresult[3]  + ' ' +  __json['message']['StationGovernment'].lower()  + ' ' +  myresult[4]  + ' ' +  __json['message']['StarSystem'].lower())
                                # f.close()
        del __converted
        mydb.close()

def keyboardInterruptHandler(signal, frame):
    print("KeyboardInterrupt (ID: {}) has been caught. Cleaning up...".format(signal))
    exit(0)

def main():
    # echoLog('Starting EDDN Subscriber')
    # echoLog('')

    context     = zmq.Context()
    subscriber  = context.socket(zmq.SUB)

    subscriber.setsockopt(zmq.SUBSCRIBE, b"")
    subscriber.setsockopt(zmq.RCVTIMEO, __timeoutEDDN)

    while True:
        try:
            subscriber.connect(__relayEDDN)

            while True:
                __message   = subscriber.recv()
                print('message recu')
                thread = threading.Thread(target = inject, args = (__message, ))
                thread.start()
                print(threading.active_count())
                signal.signal(signal.SIGINT, keyboardInterruptHandler)
                # thread.join()
                # print("thread finished...exiting")
                if __message == False:
                    subscriber.disconnect(__relayEDDN)
                    # echoLog('Disconnect from ' + __relayEDDN)
                    # echoLog('')
                    # echoLog('')
                    break
        except zmq.ZMQError:
            subscriber.disconnect(__relayEDDN)
            time.sleep(5)



if __name__ == '__main__':
    main()
