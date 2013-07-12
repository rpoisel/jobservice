import sys
import os
import traceback
import subprocess
import json
from time import sleep
from Queue import Queue, Empty
from threading import Thread
import string

import requests

ON_POSIX = 'posix' in sys.builtin_module_names


# taken from here
#   http://stackoverflow.com/questions/375427/non-blocking-read-on-a-subprocess-pipe-in-python
def enqueue_output(pOut, pQueue):
    for lLine in iter(pOut.readline, b''):
        pQueue.put(lLine)
    pOut.close()


def main():
    try:
        HOST = "pc16.leela.lab"
        PORT = 5000
        MESSAGE = 'Password Not Found'
        FOUND_PASS = 'false'
        TRUECRACK_PATH = '/netexport/tmp/truecrack-3/bin/truecrack'
        HEADER_PATH = 'res/example.img'
        DICT_PATH = 'res/small.txt'
        REFETCH_PERIOD = 2
        WORD_SIZE = 0

        lFileSize = os.stat(DICT_PATH).st_size

        # job loop
        while True:
            lRange = {}
            # request loop
            while True:
                lResponse = requests.get(
                    "http://" + HOST + ":" + str(PORT) + "/fetch"
                )
                lRange = json.loads(lResponse.text)
                if 'job' in lRange:
                    break
                sleep(REFETCH_PERIOD)

            lRangeId = lRange['job'][0]
            lNumRanges = lRange['job'][1]

            print "Execute the following job: " + str(lRangeId) + \
                " of " + str(lNumRanges)

            lFH = open(DICT_PATH, "rb")
            lOffsetBegin = float(lRangeId) / lNumRanges * lFileSize - WORD_SIZE
            lOffsetEnd = float(lRangeId + 1) / lNumRanges * lFileSize

            if lRangeId is not 0:
                lFH.seek(
                    lOffsetBegin,
                    os.SEEK_SET
                )

            # Start truecrack
            lTrueCrack = subprocess.Popen(
                [TRUECRACK_PATH, "-t", HEADER_PATH, "-w", "-"],
                bufsize=512,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE
            )

            lOutputQueue = Queue()
            lThread = Thread(
                target=enqueue_output,
                args=(
                    lTrueCrack.stdout,
                    lOutputQueue
                )
            )
            lThread.daemon = True
            lThread.start()

            # interact with truecrack
            while lFH.tell() < lOffsetEnd:
                # read password (line) from file
                lPass = lFH.readline()

                # forward password to process
                lTrueCrack.stdin.write(lPass + '\n')

            # stop the process
            try:
                lTrueCrack.communicate()
            except IOError:
                # ignore what they say :-)
                pass

            lOutput = ''
            while True:
                # get output
                try:
                    lLine = lOutputQueue.get_nowait()
                except Empty:
                    break
                lOutput += lLine

            # parse output and forward result to server
            print(lOutput)

            if 'Found password' in lOutput:
                MESSAGE = lOutput.split()[9]
                MESSAGE = MESSAGE.strip(string.punctuation)
                FOUND_PASS = 'true'

            lResponse = requests.get(
                "http://" + HOST + ":" + str(PORT) + "/report?" +
                "success=" + FOUND_PASS +
                "&rangeId=" + str(lRangeId) +
                "&message=" + MESSAGE
            )

            if FOUND_PASS is 'true':
                break

            # notify server

            # Print truecrack's output
            #print pass_check

            # Determine if the password has been found

    except Exception:
        traceback.print_exc()
    except KeyboardInterrupt:
        # clean up here
        pass


if __name__ == '__main__':
    main()
