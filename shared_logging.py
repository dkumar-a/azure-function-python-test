import logging
import os
from logging import getLogger
from opencensus.ext.azure.log_exporter import AzureLogHandler


class CustomDimensionsFilter(logging.Filter):
    """Add application-wide properties to AzureLogHandler records"""

    def __init__(self, custom_dimensions=None):
        self.custom_dimensions = custom_dimensions or {}

    def filter(self, record):
        """Adds the default custom_dimensions into the current log record"""
        cdim = self.custom_dimensions.copy()
        cdim.update(getattr(record, 'custom_dimensions', {}))
        record.custom_dimensions = cdim

        return True


def build_azure_handler():
    """"""
    instrumentation_key = os.environ.get(
        "INSTRUMENTATION_KEY", "59b13c2d-c0ad-469f-87da-70039cbceec0;IngestionEndpoint=https://centralus-2.in.applicationinsights.azure.com/;LiveEndpoint=https://centralus.livediagnostics.monitor.azure.com/"
    )

    log_dfmt = '%Y-%m-%d %H:%M:%S'
    log_fmt = '%(asctime)s - %(levelname)-8s - %(name)s.%(funcName)s: %(message)s'
    formatter = logging.Formatter(log_fmt, log_dfmt)

    default_properties = {'app_name': 'First_Azure_Function_Python'}
    # or supply the default_properties as environment variables and add them here

    handler = AzureLogHandler(
        connection_string=f'InstrumentationKey={instrumentation_key}')
    handler.addFilter(CustomDimensionsFilter(default_properties))
    handler.setFormatter(formatter)
    return handler


def init():
    handler = build_azure_handler()
    logging.basicConfig(handlers=[handler])


init()
