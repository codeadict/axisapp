import logging
from django.db import connection


sql_log = logging.getLogger('sql_logger')
totals_log = logging.getLogger('sql_totals_logger')


class SqlTimingMiddleware(object):
    """
    Logs the total time taken to run sql queries and the number of sql queries
    per request.
    """
    def process_response(self, request, response):
        sqltime = 0  # Variable to store execution time
        for query in connection.queries:
            # Add the time that the query took to the total
            sqltime += float(query["time"])
            sql_log.debug(request.path_info, extra=query)

        totals_log.debug(request.path_info,
                         extra={'time': sqltime,
                                'num_queries': len(connection.queries)})

        return response