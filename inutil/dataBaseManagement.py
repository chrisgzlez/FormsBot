# AUTHOR: CHRISTIAN NOVOA GONZALEZ


# FUTURE CHANGES:
#   TERMINAL BASED:
#       add option to use several commands at once in terminal ("monitor chrome")
#           (Will be Done with Python 3.10 and match case function)
#       add more database functions for removing and adding data
#       add some more programs to the database
#       create a special class for Chrome
#           new and more functions to control websites/save websites...
#   CREATE WEBSITE
#   AUTORUN PROGRAM

import sqlite3
import re
from beautifultable import BeautifulTable
from dataclasses import dataclass, field
import datetime as dt

# NOTES:
  # SQLITE3:
    # cannot create table without columns
    # cannot change name or delete column in sqlite3
    # cannot use ? to include table names or table columns, just Values
    # can use (and will use) string formatting to do such tasks


  # BEAUTIFULTABLE:
    # table = BeautifulTable()
    # table.rows.append(["value1", value2,])     adding values to it
    # table.rows.header([1, 2, 3,])      indexing the table
    # table.columns.header(["column1", "column2", ])     adding column names


@dataclass
class _ProgramBase:
    name: str


@dataclass
# frozen means read-only, so no modifying the data
class Program(_ProgramBase):
    time_array = {}

    @staticmethod
    def get_time() -> re.Match:
        timestamp = str(dt.datetime.now())
        timestamp_pattern = r"(?P<Date>((-)*([0-9]{2,4})){3}) (?P<Time>((:)*([0-9]{2})){3})"
        match = re.match(timestamp_pattern, timestamp)
        # in case of an update changing the format of the dates
        if not match:
            print("""ERROR
                    It has not been matched
                    CHECK main.py, timestamp_pattern""")
        return match

    def start_monitoring(self) -> None:
        match = self.get_time()
        date = match.group("Date")
        time = match.group("Time")
        self.time_array[date] = time
        print(f"Program: {self.name} Initialized at {time} on {date}")

    def stop_monitoring(self) -> tuple[str, str, str]:
        for date, time in self.time_array.items():
            print(f"""Program: {self.name}
            Program Was Initialized at {time} on {date}
            Finished Running at {self.get_time().group("Time")}
            The Data has been added to the database
            """)
            return date, time, self.get_time().group("Time")


@dataclass
class _DataBase:
    db: str = field(init=False)
    con: sqlite3.Connection = field(init=False)
    cur: sqlite3.Cursor = field(init=False)

    def __post_init__(self) -> None:
        self.db = "Programming_Stats.db"
        self.con = sqlite3.connect(self.db)
        self.cur = self.con.cursor()


@dataclass
class DataBase(_DataBase, Program):

    def create_table(self) -> None:
        self.cur.execute(f"CREATE TABLE {self.name} (DATE, START_TIME, END_TIME)")
        # for column in columns:
        #   self.cur.execute(f"CREATE TABLE {self.name} ({column})") if column == columns[0] \
        #        else self.cur.execute(f"ALTER TABLE {self.name} ADD {column}")

    # add the monitored data to the database
    def add_data(self, timestamps: tuple) -> None:
        date, init_time, end_time = timestamps
        self.cur.execute(f"""INSERT INTO {self.name} (DATE, START_TIME, END_TIME)
            VALUES (?, ?, ?)""", (date, init_time, end_time))

    # executes several monitor functions
    def monitor(self, status: bool) -> None:
        if status:
            self.start_monitoring()
        else:
            self.add_data(self.stop_monitoring())
            self.time_array = {}

    def show_table(self) -> None:
        table = BeautifulTable()
        self.cur.execute(f"SELECT * FROM {self.name};")
        result = self.cur.fetchall()
        table.columns.header = ["Date", "Start_Time", "End_Time"]
        # adding rows to BeautifulTable
        for row in result:
            temp = []
            for value in row:
                temp.append(value)
            table.rows.append(temp)
        print(table)
