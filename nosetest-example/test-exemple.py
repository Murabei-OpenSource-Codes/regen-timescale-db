"""Sets an example for nosetests using regen postgres image."""
import unittest
import requests
import pandas as pd
from sqlalchemy import create_engine


class TestExample(unittest.TestCase):
    """Unittest class that helps building pumpwood based systems test."""
    con_str = "postgresql://murabei:is_very_nice!@localhost/murabei"

    def test__1(self):
        """Check if database has regen after call."""
        engine = create_engine(self.con_str)
        counts_start = pd.read_sql("""
            SELECT var, COUNT(*) AS count_start
            FROM data
            GROUP BY var
        """, con=engine)

        # Removing some rows...
        engine.execute("DELETE FROM data WHERE var='murabei'")
        counts_delete = pd.read_sql("""
            SELECT var, COUNT(*)
            FROM data
            GROUP BY var
        """, con=engine)
        self.assertNotIn('murabei', counts_delete["var"])

        # Regenerate database
        response = requests.get(
            "http://0.0.0.0:5000/reload-db/regen-test/")
        response.raise_for_status()

        # Check if database has regenerate
        counts_final = pd.read_sql("""
            SELECT var, COUNT(*) AS count_final
            FROM data
            GROUP BY var
        """, con=engine)
        pd_check_data = counts_final.merge(counts_start)
        check = (
            pd_check_data["count_final"] == pd_check_data[
                "count_start"]).all()
        self.assertTrue(check)
