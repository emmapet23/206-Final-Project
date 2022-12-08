import unittest
import sqlite3
import json
import os
import csv

import last_fm_api
import spotify_api
#import emily's


def main():
    spotify_api.main()
    last_fm_api.main()

main()