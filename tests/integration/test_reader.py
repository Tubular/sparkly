import unittest

import pytest

from sparkle.test import (
    SparkleGlobalContextTest,
    BaseCassandraTest,
    BaseElasticTest,
    BaseMysqlTest,
)
from sparkle.utils import absolute_path
from tests.integration.base import _TestContext


@pytest.mark.branch_1_0
class SparkleReaderCassandraTest(BaseCassandraTest, SparkleGlobalContextTest):
    context = _TestContext

    cql_setup_files = [
        absolute_path(__file__, 'resources', 'test_read', 'cassandra_setup.cql'),
    ]
    cql_teardown_files = [
        absolute_path(__file__, 'resources', 'test_read', 'cassandra_teardown.cql'),
    ]

    def test_cassandra(self):
        df = self.hc.read_ext.cassandra(
            host=self.c_host,
            keyspace='sparkle_test',
            table='test',
            consistency='ONE',
        )

        self.assertCountEqual(
            [row.asDict() for row in df.take(3)],
            [
                {
                    'countries': {'DZ': 1, 'EG': 206, 'BE': 1, 'CA': 1, 'AE': 13, 'BH': 3},
                    'uid': '6',
                    'created': '1234567894',
                },
                {
                    'countries': {'DZ': 1, 'EG': 206, 'BE': 1, 'CA': 1, 'AE': 13, 'BH': 3},
                    'uid': '7',
                    'created': '1234567893',
                },
                {
                    'countries': {'DZ': 1, 'EG': 206, 'BE': 1, 'CA': 1, 'AE': 13, 'BH': 3},
                    'uid': '9',
                    'created': '1234567891',
                }]
        )


@pytest.mark.branch_1_0
class SparkleReaderCSVTest(SparkleGlobalContextTest):
    context = _TestContext

    def test_csv(self):
        df = self.hc.read_ext.csv(
            path=absolute_path(__file__, 'resources', 'test_read', 'test.csv'),
        )

        self.assertCountEqual(
            [row.asDict() for row in df.take(2)],
            [
                {
                    'county': 'CLAY COUNTY',
                    'statecode': 'FL',
                    'point_granularity': 1,
                    'point_latitude': 30.102261,
                    'fr_site_limit': 498960.0,
                    'point_longitude': -81.711777,
                    'tiv_2012': 792148.9,
                    'fl_site_deductible': 0,
                    'fr_site_deductible': 0,
                    'construction': 'Masonry',
                    'tiv_2011': 498960.0,
                    'line': 'Residential',
                    'eq_site_deductible': 0,
                    'policyID': 119736,
                    'eq_site_limit': 498960.0,
                    'hu_site_limit': 498960.0,
                    'hu_site_deductible': 9979.2,
                    'fl_site_limit': 498960.0,
                },
                {
                    'county': 'CLAY COUNTY',
                    'statecode': 'FL',
                    'point_granularity': 3,
                    'point_latitude': 30.063936,
                    'fr_site_limit': 1322376.3,
                    'point_longitude': -81.707664,
                    'tiv_2012': 1438163.57,
                    'fl_site_deductible': 0,
                    'fr_site_deductible': 0,
                    'construction': 'Masonry',
                    'tiv_2011': 1322376.3,
                    'line': 'Residential',
                    'eq_site_deductible': 0,
                    'policyID': 448094,
                    'eq_site_limit': 1322376.3,
                    'hu_site_limit': 1322376.3,
                    'hu_site_deductible': 0.0,
                    'fl_site_limit': 1322376.3,
                },
            ]
        )


@pytest.mark.branch_1_0
class SparkleReaderElasticTest(BaseElasticTest, SparkleGlobalContextTest):
    context = _TestContext

    elastic_setup_files = [
        absolute_path(__file__, 'resources', 'test_read', 'elastic_setup.json'),
    ]
    elastic_teardown_indexes = ['sparkle_test']

    def test_elastic(self):
        df = self.hc.read_ext.elastic(
            host=self.elastic_host,
            es_index='sparkle_test',
            es_type='test',
            query='?q=name:*Smith*',
            options={'es.read.field.as.array.include': 'topics'},
        )

        rows = [row.asDict() for row in df.take(3)]
        for row in rows:
            row['demo'] = row['demo'].asDict()

        self.assertCountEqual(
            rows,
            [
                {
                    '_metadata': {
                        '_index': 'sparkle_test',
                        '_id': '2',
                        '_type': 'test',
                        '_score': '0.0',
                    },
                    'age': 31,
                    'topics': [1, 4, 5],
                    'demo': {'age_10': 50, 'age_30': 110},
                    'name': 'Smith3',
                },
                {
                    '_metadata': {
                        '_index': 'sparkle_test',
                        '_id': '3',
                        '_type': 'test',
                        '_score': '0.0',
                    },
                    'age': 12,
                    'topics': [4, 5],
                    'demo': {'age_10': 1, 'age_30': 20},
                    'name': 'Smith4',
                }
            ]
        )


@pytest.mark.branch_1_0
class SparkleReaderMySQLTest(BaseMysqlTest, SparkleGlobalContextTest):
    context = _TestContext

    sql_setup_files = [
        absolute_path(__file__, 'resources', 'test_read', 'mysql_setup.sql'),
    ]
    sql_teardown_files = [
        absolute_path(__file__, 'resources', 'test_read', 'mysql_teardown.sql'),
    ]

    def test_read_mysql(self):
        df = self.hc.read_ext.mysql(
            host=self.mysql_host,
            database='sparkle_test',
            table='test',
            options={
                'user': 'root',
                'passowrd': '',
            }
        )

        self.assertCountEqual(
            [row.asDict() for row in df.take(3)],
            [
                {'id': 1, 'name': 'john', 'surname': 'sk', 'age': 111},
                {'id': 2, 'name': 'john', 'surname': 'po', 'age': 222},
                {'id': 3, 'name': 'john', 'surname': 'ku', 'age': 333},
            ]
        )
