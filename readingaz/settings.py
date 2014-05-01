# Scrapy settings for readingaz project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#

BOT_NAME = 'readingaz'
BOT_VERSION = '1.0'

SPIDER_MODULES = ['readingaz.spiders']
NEWSPIDER_MODULE = 'readingaz.spiders'
USER_AGENT = '%s/%s' % (BOT_NAME, BOT_VERSION)

# ITEM_PIPELINES = ['readingaz.pipelines.ReadingazPipeline']
