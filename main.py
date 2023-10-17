import os
import re
import asyncio
import configparser
from datetime import date

from utils import Logger

class NoFilesFoundInDirError(Exception):
    """Files not found in directory"""
    def __init__(self, message: str, *args: object) -> None:
        super().__init__(message, *args)

logger = Logger()

config = configparser.ConfigParser()

with open("./settings/settings.ini", "r") as file:
    config.read_file(file)

DIR = config.get("directory", "dir")

today = date.today()

FORMATTED_DATE = f"{today.month}.{today.day}.{str(today.year)[2:]}"

def read_directory() -> list[str]:
    logger.info("Reading files in %s" % DIR)

    excel_files = []

    [excel_files.append(f"{DIR}{file}") for file in os.listdir(DIR) 
     if file.endswith(".csv") or file.endswith(".xlsx")]
    
    if not len(excel_files):
        raise NoFilesFoundInDirError("Files not found in directory")

    logger.info("%s files found" % len(excel_files))
    
    return excel_files

async def get_extension(filename: str) -> str:
    return filename.split(".")[-1]

async def get_new_name(file_name: str, extension: str) -> str:
    return file_name.replace(f".{extension}", f"_{FORMATTED_DATE}.{extension}")

def rename(file_name: str, new_name: str) -> None:
    os.rename(file_name, new_name)

    logger.info("File '{}' renamed to '{}'".format(file_name.split("/")[-1],
                                                   new_name.split("/")[-1]))

async def rename_file(file_name: str) -> None:
    if not re.search(r"\d+\.{1,1}\d+\.{1,1}\d+\.{1,1}", file_name):
        extension = asyncio.create_task(get_extension(file_name))

        await extension

        new_name = asyncio.create_task(get_new_name(file_name, extension.result()))

        await new_name

        await asyncio.to_thread(rename, file_name, new_name.result())

async def run() -> None:
    for file in read_directory():
        task = asyncio.create_task(rename_file(file))

        await task

if __name__ == "__main__":
    asyncio.run(run())