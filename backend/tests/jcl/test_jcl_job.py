import requests
import base64
from dataclasses import dataclass
import json
from enum import Enum, auto
import unittest
import os
import sys
src_path = os.path.curdir + "/backend/src"
print(src_path)
sys.path.insert(0, src_path)
from config.settings import Settings

JOB_NAME = "GLDFIREP"
TEST_SET_EXPECTED_OUTPUT_PATH ="backend/tests/test_data/test_set_1_expected_job_output.json" 

class TestJCLJobOutput(unittest.TestCase):
    """Tests to ensure the existing report at JOB_NAME under the current user contains the expected tables
    - Prior to running the job, the database is expected to be reset to a default state and repopulated using the insert_test_data script
    - The job output must exist prior to running this test, so the test should not be run as part of the normal suite
    - Run this test using `python -m unittest discover -s ./backend/tests/jcl -p "test_*.py" -v`
    """
    @staticmethod
    def test_jcl_job_output():
        creds: dict = json.load(open(Settings.db_config_file()))

        ZOSMF_URL = f"https://{creds["host"]}:11443"

        class ZosmfRoutes():
            AUTHENTICATE = "/zosmf/services/authenticate"
            SDSF_JOBS = "/zosmf/restjobs/jobs"


        def get_zosmf_authed_sesion(user_name: str, password: str, zosmf_url: str) -> requests.Session:
            auth_b64 = base64.urlsafe_b64encode(f"{user_name}:{password}".encode("utf-8")).decode("utf-8")

            auth_headers = {
                "Authorization" : f"Basic {auth_b64}",
                "Accept": "application/json",
                "Content-Type": "application/json",
            }

            session = requests.session()
            session.verify = False # SSL Doesn't work with zosmf
            print(f"{zosmf_url}{ZosmfRoutes.AUTHENTICATE}")
            auth_request = session.post(f"{zosmf_url}{ZosmfRoutes.AUTHENTICATE}", headers=auth_headers)
            
            if not auth_request:
                raise Exception(f"Mainframe API Authentication failed.\n\tresponse: {auth_request}\n\tcontent: {auth_request.content.decode()}")

            return session


        def get_job_lines_by_job_name(zosmf_authed_session: requests.Session, job_name: str) -> list[str]:

            query_params = f"?owner={creds['username']}&prefix={job_name}&max-jobs=1&exec-data=N"

            request = zosmf_authed_session.get(f"{ZOSMF_URL}{ZosmfRoutes.SDSF_JOBS}{query_params}")

            if not request.content:
                raise Exception(f"Failed to find job when searching for {job_name}")
            
            results = request.json()

            if not results:
                raise Exception(f"Unexpected resultes from {job_name}, got {results}")


            single_result = request.json()[-1]

            files = zosmf_authed_session.get(single_result["files-url"]).json()

            sysprint_file: str = ""

            for file in files:
                print(file["ddname"])
                if file["ddname"] == "SYSPRINT":
                    sysprint_file = zosmf_authed_session.get(file["records-url"]).text
                    break

            if not sysprint_file:
                raise Exception(f"SYSPRINT file not found in job")
            
            # Strip all lines for easier processing
            print(sysprint_file)
            return sysprint_file.splitlines() 
        # Tables are formatted like the following:
        #      +---------------------------------------------------------------+
        #      | ORDER_DATE |   PRODUCT_ID   |   DESIGN_ID    | TOTAL_QUANTITY |
        #      +---------------------------------------------------------------+
        #    1_| 03/10/2026 |              5 |              4 |              1 |
        #    2_| 03/01/2026 |              5 |              3 |              1 |
        #    3_| 02/15/2026 |              3 |              4 |              2 |
        #    4_| 02/10/2026 |              1 |              1 |              2 |
        #    5_| 02/01/2026 |              4 |              2 |              5 |
        #    6_| 01/20/2026 |              2 |              3 |              3 |
        #    7_| 01/15/2026 |              1 |              1 |              3 |
        #      +---------------------------------------------------------------+
        @dataclass
        class Table:
            column_names: list[str]
            rows: list[list[str]]

        class ParseState(Enum):
            # Using auto because we don't care about the enum values
            SEARCHING = auto(),
            EXTRACTING = auto()

        TABLE_BOUNDARY_MARKER = "+-"
        COLUMN_DELIMITER = "|"

        def parse_table_row(line: str) -> list[str]:
            """Returns a table row, removes whitespace"""
            return [col.strip() for col in line.split(COLUMN_DELIMITER)[1:-1]]

        def parse_tables_from_job(job_lines: list[str]) -> list[Table]:
            """ Extracts all tables from the lines of a job output

                Args: 
                    job_lines: List of lines from the job output

                Returns:
                    List of tables extracted from the job output
            """
            processed_job_lines = [line.strip() for line in job_lines]
            tables: list[Table] = [] # There should be 1 table per required report
            current_parse_state: ParseState = ParseState.SEARCHING
            lines_iterator = iter(processed_job_lines)
            for current_line in lines_iterator:
                if current_parse_state == ParseState.EXTRACTING:
                    if current_line.startswith(TABLE_BOUNDARY_MARKER):
                        current_parse_state = ParseState.SEARCHING
                    else:
                        # Always append to the rows in the last table
                        tables[-1].rows.append(parse_table_row(current_line))
                elif current_parse_state == ParseState.SEARCHING and current_line.startswith(TABLE_BOUNDARY_MARKER):
                    # Get the next 2 lines of the table header
                    # - Calling next(lines_iterator) will effectively advance the for loop 
                    table_header_columns_line = next(lines_iterator)
                    table_header_closing_line = next(lines_iterator)
                    if table_header_closing_line.startswith(TABLE_BOUNDARY_MARKER):
                        tables.append(Table(parse_table_row(table_header_columns_line), []))
                        current_parse_state = ParseState.EXTRACTING
            return tables

        def parse_tables_from_test_data(test_data_path: str) -> list[Table]:
            expected_output = json.load(open(test_data_path, "r"))
            expected_tables: list[Table] = []
            for table_data in expected_output:
                # Must convert each value in the rows to strings to compare to job output
                processed_rows: list[list[str]] = [[str(col) for col in row] for row in table_data["ROWS"]]
                expected_tables.append(Table(table_data["COLUMN_NAMES"], processed_rows))
            return expected_tables

        expected_tables = parse_tables_from_test_data(TEST_SET_EXPECTED_OUTPUT_PATH)
        authed_session = get_zosmf_authed_sesion(creds["username"], creds["password"], ZOSMF_URL)
        job_tables = parse_tables_from_job(get_job_lines_by_job_name(authed_session, JOB_NAME))

        print(f"expected_tables: {expected_tables}")
        print("\n\n\n")
        print(f"tables from job: {job_tables}")
        if (expected_tables == job_tables):
            print("Job tables are equal to expected tables, test passed")
        else:
            raise Exception("Job tables are not equal to expected tables, test failed")


