class ReadingazPipeline(object):
    def process_item(self, item, spider):
        for pdfUrl in item['pdfs']:
            path = self.get_path(pdfUrl)
            #print path
            with open(path, "wb") as f:
                f.write(item['body'])
        return item

    def get_path(self, path):
        return "http://www.readinga-z.com"+path;