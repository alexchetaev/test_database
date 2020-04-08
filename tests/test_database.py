# -*- coding: utf-8 -*-

"""
Tests examples for test tables exists and structure
"""

import pytest
import sqlalchemy.dialects

from sqlalchemy import create_engine, MetaData

test_db_conn = create_engine('mysql://test_user:test_password@localhost/test_db')

meta_data = MetaData(bind=test_db_conn, reflect=True)

test_db_tables: dict = meta_data.tables


################
"""
Structure storage should be in separate file but now here if for example
"""
tables_structures = {
    "internal_users": {
        "id": sqlalchemy.dialects.mysql.types.INTEGER,
        "name": {
            "type": sqlalchemy.dialects.mysql.types.VARCHAR,
            "length": 50,
        }
    },
    "external_users": {
        "id": sqlalchemy.dialects.mysql.types.INTEGER,
        "name": {
            "type": sqlalchemy.dialects.mysql.types.VARCHAR,
            "length": 50,
        }
    },
}
################


@pytest.mark.skip(reason="Abstract function")
def test_table_exist(table_name, tables_list):
    assert (table_name in tables_list), f"Error {table_name} did not found in database"


@pytest.mark.skip(reason="Abstract function")
def test_table_structure(table, structure, check_string_length=False):
    for k, v in structure.items():
        assert (k in table._columns), f"Column {k} did not found in table {table.name}"

        column = table._columns.get(k)

        _type = v if not isinstance(v, dict) else v.get('type')

        assert isinstance(column.type, _type), (f"Bad type for column f{k} in table {table.name}. "
                                                f"Should be {str(v)}, but now {str(column.type)}")
        if _type == sqlalchemy.dialects.mysql.types.VARCHAR and check_string_length:
            assert (v.get('length') == column.type.length), (f"Bad varchar column length. Should be {v.get('length')} "
                                                             f"but now {column.type.length}")

        """
        In general may be we need to add something another specific check as we added for string length for another 
        column types that we use in our database. 
        """


@pytest.mark.skip(reason="Abstract function")
def test_data_matching(source_cursor, target_cursor: sqlalchemy.engine.result.ResultProxy, id_column_name, columns=None):
    """
    This can be optimized without for in for and id. This code is only for example

    :param source_cursor: reference data
    :param target_cursor: test data
    """
    source_cursor = list(source_cursor)

    target_cursor = list(target_cursor)

    for source_row in source_cursor:
        found = False

        checked = True

        problem_colums = []

        for target_row in target_cursor:
            if source_row[id_column_name] == target_row[id_column_name]:
                found = True

                for k in source_row._keymap:
                    if source_row[k] == target_row[k]:
                        continue
                    else:
                        problem_colums.append(k)

                        checked = False

                break

        assert found, f"Row with id {source_row[id_column_name]} did not found in target tables"

        assert checked, f"Data do not mach for columns {problem_colums} in row with id {source_row[id_column_name]}"


def test_tables_structure():
    for k, v in tables_structures.items():
        test_table_exist(k, test_db_tables)

        table = test_db_tables.get(k)

        test_table_structure(table, v, check_string_length=True)


def test_tables_data():
    target_cursor = test_db_conn.execute("select * from internal_users")

    source_cursor = test_db_conn.execute("select * from external_users")

    test_data_matching(source_cursor, target_cursor, "id")












