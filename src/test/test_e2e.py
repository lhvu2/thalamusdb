import sys
import argparse
import sys
import time
import traceback

from prompt_toolkit import prompt
from prompt_toolkit.history import InMemoryHistory
from rich.console import Console
from rich.rule import Rule
from tdb.data.relational import Database
from tdb.execution.constraints import Constraints
from tdb.execution.engine import ExecutionEngine
from tdb.queries.query import Query
from tdb.ui.util import print_df

from tdb.console import run_console
from tdb.console import _process_query

if __name__ == '__main__':
    
    dbpath = "/home/lhvu/projects/thalamusdb/data/cars/cars.db"
    #modelconfigpath = "/home/lhvu/projects/thalamusdb/config/rits_models.json"
    modelconfigpath = "/home/lhvu/projects/thalamusdb/config/ibm_litellm_models.json"

    db = Database(dbpath)
    dop = 1
    model_config_path = modelconfigpath
    engine = ExecutionEngine(db, dop, model_config_path)
    constraints = Constraints()
    history = InMemoryHistory()
    cmd = "select count(*) from cars where nlfilter(pic, 'the car in the picture is black or white');"

    _process_query(
        db, engine, constraints, cmd)
    
    pass