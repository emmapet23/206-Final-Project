import unittest
import sqlite3
import json
import os
import csv

import spotify_api
import last_fm_api
import billboard_url


def main():
    spotify_api.main()
    last_fm_api.main()
    billboard_url.main()

main() 