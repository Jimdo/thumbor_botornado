import thumbor_botornado.s3_loader as S3Loader
import tornado.concurrent.return_future
import thumbor.loaders.http_loader as HttpLoader
import re
import librato
import os

HTTP_RE = re.compile(r'\Ahttps?:', re.IGNORECASE)
LIBRATO_API = librato.connect(os.environ.get('LIBRATO_USER'), os.environ.get('LIBRATO_TOKEN'))


@return_future
def load(context, url, callback):
    logger.debug("*** LOADER.load" )
    start = datetime.datetime.now()
    if HTTP_RE.match(url):
        method = 'http'
        HttpLoader.load(context, url, callback)
    else:
        method = 's3'
        logger.debug("*** s3")
        S3Loader.load(context, url, callback)
    finish = datetime.datetime.now()
    metric_name = "thumbor.loader.%s.request_time" % method
    logger.debug("*** librato submit")
    LIBRATO_API.submit(metric_name, (finish - start).total_seconds() * 1000, description="original file request time (ms)")

