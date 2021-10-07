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
        # Handle commodity v3
        __converted = False
        if __json['$schemaRef'] == 'https://eddn.edcd.io/schemas/commodity/3' + ('/test' if (__debugEDDN == True) else ''):
            # if __converted == False:
                # # echoLogJSON(__message)
                # echoLog('Receiving commodity-v3 message...')

            __authorised = False
            __excluded   = False

            if __json['header']['softwareName'] in __authorisedSoftwares:
                __authorised = True
            if __json['header']['softwareName'] in __excludedSoftwares:
                __excluded = True

            # echoLog('    - Software: ' + __json['header']['softwareName'] + ' / ' + __json['header']['softwareVersion'])
            # echoLog('        - ' + 'AUTHORISED' if (__authorised == True) else ('EXCLUDED' if (__excluded == True) else 'UNAUTHORISED'))

            if __authorised == True and __excluded == False:
                # Do what you want with the data...
                # Have fun !

                # For example
                # echoLog('    - Timestamp: ' + __json['message']['timestamp'])
                # echoLog('    - Uploader ID: ' + __json['header']['uploaderID'])
                # echoLog('        - System Name: ' + __json['message']['systemName'])
                # echoLog('        - Station Name: ' + __json['message']['stationName'])

                for __commodity in __json['message']['commodities']:
                    # print(__commodity['name'])
                    # # echoLog('            - Name: ' + __commodity['name'])
                    # # echoLog('                - Buy Price: ' + str(__commodity['buyPrice']))
                    # # echoLog('                - Supply: ' + str(__commodity['supply']) + ((' (' + __commodity['supplyLevel'] + ')') if 'supplyLevel' in __commodity else ''))
                    # # echoLog('                - Sell Price: ' + str(__commodity['sellPrice']))
                    # # echoLog('                - Demand: ' + str(__commodity['demand']) + ((' (' + __commodity['demandLevel'] + ')') if 'demandLevel' in __commodity else ''))
                    if __commodity['name'] == "opal":
                       # print(__json['message']['marketId'])
                       mycursor = mydb.cursor()
                       sql = "SELECT count(*) FROM vrai_market WHERE idMarket = " + str(__json['message']['marketId'])
                       mycursor.execute(sql)
                       print(sql)
                       myresult = mycursor.fetchone()
                       print(int(myresult[0]))
                       print("opal du vide detecter")
                       date = datetime.datetime.strptime(__json['message']['timestamp'], '%Y-%m-%dT%H:%M:%SZ')
                       if int(myresult[0]) != 0:
                          print('Station et systeme connu et non fleetshit')
                          sql = "SELECT count(*), Max(opal.Debut), Prix FROM opal JOIN vrai_market ON opal.idMarket = vrai_market.idMarket WHERE opal.idMarket = " + str(__json['message']['marketId']) + " AND opal.fin > NOW()"
                          mycursor.execute(sql)
                          myresult = mycursor.fetchone()
                          #print(__commodity)
                          if int(myresult[0]) == 0:
                            sql = "INSERT INTO opal (Prix, idMarket, debut, Demand) VALUES (%s, %s, %s, %s)"
                            val = (float(__commodity['sellPrice']), __json['message']['marketId'], date, __commodity['demand'])
                            mycursor.execute(sql, val)
                            mydb.commit()
                            print(mycursor.rowcount, "record inserted.")
                          elif int(myresult[0]) != 0 and myresult[1] < date and myresult[2] != float(__commodity['sellPrice']):
                              sql = "UPDATE opal SET fin = Now() WHERE idMarket = " + str(__json['message']['marketId']) + " AND Fin = '9999-12-31'"
                              #print(sql)
                              mycursor.execute(sql)
                              mydb.commit()
                              print(mycursor.rowcount, "record updated.")
                              sql = "INSERT INTO opal (Prix, idMarket, debut, Demand) VALUES (%s, %s, %s, %s)"
                              val = (float(__commodity['sellPrice']), __json['message']['marketId'], date, __commodity['demand'])
                              mycursor.execute(sql, val)
                              mydb.commit()
                              print(mycursor.rowcount, "record inserted.")
                              
                    if __commodity['name'] == "lowtemperaturediamond":
                       # print(__json['message']['marketId'])
                       mycursor = mydb.cursor()
                       sql = "SELECT count(*) FROM vrai_market WHERE idMarket = " + str(__json['message']['marketId'])
                       mycursor.execute(sql)
                       print(sql)
                       myresult = mycursor.fetchone()
                       print(int(myresult[0]))
                       print("lowtemperaturediamond detecter")
                       date = datetime.datetime.strptime(__json['message']['timestamp'], '%Y-%m-%dT%H:%M:%SZ')
                       if int(myresult[0]) != 0:
                          print('Station et systeme connu et non fleetshit')
                          sql = "SELECT count(*), Max(lowtemperaturediamond.Debut), Prix FROM lowtemperaturediamond JOIN vrai_market ON lowtemperaturediamond.idMarket = vrai_market.idMarket WHERE lowtemperaturediamond.idMarket = " + str(__json['message']['marketId']) + " AND lowtemperaturediamond.fin > NOW()"
                          mycursor.execute(sql)
                          myresult = mycursor.fetchone()
                          if int(myresult[0]) == 0:
                            sql = "INSERT INTO lowtemperaturediamond (Prix, idMarket, debut, demand) VALUES (%s, %s, %s, %s)"
                            val = (float(__commodity['sellPrice']), __json['message']['marketId'], date, __commodity['demand'])
                            mycursor.execute(sql, val)
                            mydb.commit()
                            print(mycursor.rowcount, "record inserted.")
                          elif int(myresult[0]) != 0 and myresult[1] < date and myresult[2] != float(__commodity['sellPrice']):
                              sql = "UPDATE lowtemperaturediamond SET fin = Now() WHERE idMarket = " + str(__json['message']['marketId']) + " AND Fin = '9999-12-31'"
                              #print(sql)
                              mycursor.execute(sql)
                              mydb.commit()
                              print(mycursor.rowcount, "record updated.")
                              sql = "INSERT INTO lowtemperaturediamond (Prix, idMarket, debut, demand) VALUES (%s, %s, %s, %s)"
                              val = (float(__commodity['sellPrice']), __json['message']['marketId'], date, __commodity['demand'])
                              mycursor.execute(sql, val)
                              mydb.commit()
                              print(mycursor.rowcount, "record inserted.")          

                # End example
            del __authorised, __excluded
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
