import sqlite3
import csv
import os

def exportTablesToCsv(oldDbPath, exportDir):
    """
    Exports all tables from the old SQLite database to CSV files.
    io: reads oldDbPath, writes CSV files to exportDir
    working: fetches list of tables, dumps all rows into CSVs
    """
    try:
        if not os.path.exists(exportDir):
            os.makedirs(exportDir)

        conn = sqlite3.connect(oldDbPath)
        cursor = conn.cursor()

        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()

        for tableNameTuple in tables:
            tableName = tableNameTuple[0]
            csvFilePath = os.path.join(exportDir, f"{tableName}.csv")

            cursor.execute(f"SELECT * FROM {tableName}")
            rows = cursor.fetchall()

            colNames = [description[0] for description in cursor.description]

            with open(csvFilePath, mode="w", newline="", encoding="utf-8") as file:
                writer = csv.writer(file)
                writer.writerow(colNames)
                writer.writerows(rows)

            print(f"Exported: {tableName} -> {csvFilePath}")

        conn.close()
        print("\nExport complete.")

    except Exception as error:
        print(f"Error exporting tables: {error}")


def importCsvToNewDb(newDbPath, importDir):
    """
    Imports CSV files into the new SQLite database.
    io: reads CSVs from importDir, writes data into newDbPath
    working: creates tables if needed then inserts all rows
    """
    try:
        conn = sqlite3.connect(newDbPath)
        cursor = conn.cursor()

        for fileName in os.listdir(importDir):
            if fileName.endswith(".csv"):
                tableName = fileName.replace(".csv", "")
                csvFilePath = os.path.join(importDir, fileName)

                with open(csvFilePath, mode="r", encoding="utf-8") as file:
                    reader = csv.reader(file)
                    columns = next(reader)

                    placeholder = ",".join(["?"] * len(columns))
                    createColumns = ",".join([f"{col} TEXT" for col in columns])

                    cursor.execute(f"CREATE TABLE IF NOT EXISTS {tableName} ({createColumns});")

                    cursor.execute(f"DELETE FROM {tableName};")

                    for row in reader:
                        cursor.execute(
                            f"INSERT INTO {tableName} VALUES ({placeholder})",
                            row
                        )

                print(f"Imported: {tableName}")

        conn.commit()
        conn.close()
        print("\nImport complete.")

    except Exception as error:
        print(f"Error importing tables: {error}")


def main():
    """
    Drives the full migration: export old DB -> CSV -> import into new DB.
    """
    oldDbPath = "db_migrate/dbMain.sqlite3"
    newDbPath = "db.sqlite3"
    exportDir = "exported_tables"

    exportTablesToCsv(oldDbPath, exportDir)
    importCsvToNewDb(newDbPath, exportDir)


if __name__ == "__main__":
    main()




dont inport all the tables