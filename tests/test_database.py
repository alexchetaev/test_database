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
    "some_objects": {
        "id": sqlalchemy.dialects.mysql.types.INTEGER,
        "name": {
            "type": sqlalchemy.dialects.mysql.types.VARCHAR,
            "length": 50,
        }
    }
}
################


@pytest.mark.skip(reason="abstract function")
def test_table_exist(table_name, tables_list):
    assert (table_name in tables_list), f"Error {table_name} did not found in database"


@pytest.mark.skip(reason="abstract function")
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


def test_tables_structure():
    for k, v in tables_structures.items():
        test_table_exist(k, test_db_tables)

        table = test_db_tables.get(k)

        test_table_structure(table, v)












