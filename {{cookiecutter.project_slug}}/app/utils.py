import tomlkit

from datetime import date, datetime, timedelta
from pathlib import Path

from sqlalchemy.orm import Query


def render_query(statement, db_session):
    """
    Ref: https://copdips.com/2020/06/compiling-sqlalchemy-query-to-nearly-real-raw-sql-query.html
    Generate an SQL expression string with bound parameters rendered inline
    for the given SQLAlchemy statement.
    WARNING: This method of escaping is insecure, incomplete, and for debugging
    purposes only. Executing SQL statements with inline-rendered user values is
    extremely insecure.
    Based on http://stackoverflow.com/questions/5631078/sqlalchemy-print-the-actual-query
    """
    if isinstance(statement, Query):
        statement = statement.statement
    dialect = db_session.bind.dialect

    class LiteralCompiler(dialect.statement_compiler):
        def visit_bindparam(
            self, bindparam, within_columns_clause=False, literal_binds=False, **kwargs
        ):
            return self.render_literal_value(bindparam.value, bindparam.type)

        def render_array_value(self, val, item_type):
            if isinstance(val, list):
                return "{}".format(
                    ",".join([self.render_array_value(x, item_type) for x in val])
                )
            return self.render_literal_value(val, item_type)

        def render_literal_value(self, value, type_):
            if isinstance(value, int):
                return str(value)
            elif isinstance(value, (str, date, datetime, timedelta)):
                return "'{}'".format(str(value).replace("'", "''"))
            elif isinstance(value, list):
                return "'{{{}}}'".format(
                    ",".join(
                        [self.render_array_value(x, type_.item_type) for x in value]
                    )
                )
            return super(LiteralCompiler, self).render_literal_value(value, type_)

    return LiteralCompiler(dialect, statement).process(statement)


def get_project_info():
    # Ref: https://github.com/rominf/poetry-version
    d = Path(__file__)
    result = None
    while d.parent != d and result is None:
        d = d.parent
        pyproject_toml_path = d / 'pyproject.toml'
        if pyproject_toml_path.exists():
            with open(file=str(pyproject_toml_path)) as f:
                pyproject_toml = tomlkit.parse(string=f.read())
                result = pyproject_toml['tool']['poetry']
    return result
