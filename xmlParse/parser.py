from xml.sax.handler import ContentHandler
from xml.sax import parse
from model.Job import Job, JobDataSource, Prop
from model.Worker import Worker

current_jobs = []
current_job = Job()
current_name = ""

current_workers = []


# my handler class
class MyHandler(ContentHandler):
    def startElement(self, name, attrs):
        global current_job
        global current_job
        global current_name
        global current_workers
        current_name = name
        if name == "job":
            current_job = Job()
            current_job.set_type(attrs["type"])
        if name == "datasource":
            ds = JobDataSource()
            ds.set_props([])
            ds.set_type(attrs["type"])
            current_job.set_ds(ds)
        if name == "property":
            prop = Prop()
            prop.set_name(attrs["name"])
            prop.set_value(attrs["value"])
            prop.set_type(attrs["type"])
            current_job.ds.props.append(prop)
        if name == "worker":
            worker = Worker()
            worker.set_address(attrs["address"])
            worker.set_port(attrs["port"])
            current_workers.append(worker)

    def endElement(self, name):
        global current_name
        if name == "job":
            current_jobs.append(current_job)
        if name == "sql":
            current_name = ""

    def characters(self, content):
        global current_job
        if current_name == "sql":
            current_job.set_sql(content)


# parse all workers from the configuration file workers.xml
def parse_worker(source_file):
    try:
        parse(source_file, MyHandler())
    except IOError as e:
        print e.strerror
    return current_workers


# parse all job from the configuration file jobs.xml
def parse_job(source_file):
    try:
        parse(source_file, MyHandler())
    except IOError as e:
        print e.strerror
    return current_jobs

