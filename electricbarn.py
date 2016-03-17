#!/usr/bin/env python
"""
ElectricBarn builds on mitmproxy's base proxying infrastructure to
capture and stub network requests. Responses that are captured
will be stored in a folder hierarchy matching the path fo the
request.

Note: It is expected that this will need to be customized to match
your specific requirements.
"""
import os.path
from mitmproxy import controller, proxy
from mitmproxy.models import HTTPResponse
from mitmproxy.proxy.server import ProxyServer
from netlib.http import Headers
from re import sub


class StubMaster(controller.Master):
    def __init__(self, server):
        controller.Master.__init__(self, server)
        self.stickyhosts = {}

    def run(self):
        try:
            return controller.Master.run(self)
        except KeyboardInterrupt:
            self.shutdown()

    def handle_request(self, flow):
        hid = (flow.request.host, flow.request.port)
        
        host = flow.request.pretty_host
        path = flow.request.path[1:]
        
        if self.is_supported_api(host) and os.path.isfile(path):
            
            print "Stubbing: %s/%s"%(host, path)
            f = open(path, 'r')
            resp = HTTPResponse(
                "HTTP/1.1", 200, "OK",
                Headers(Content_Type="text/json"),
                f.read()
            )
            f.close()
            flow.reply(resp)
        elif self.is_supported_host(host):
            print "Should we capture ?: %s/%s"%(host, path)
            flow.reply()
        else:
            flow.reply()
        
    def handle_response(self, flow):
        
        host = flow.request.pretty_host
        path = flow.request.path[1:]
        
        if self.is_supported_api(host) and flow.request.method != "HEAD" and flow.response.status_code == 200 and not os.path.isfile(path):
            
            print "Capturing: %s/%s"%(host, path)
            
            content = flow.response.get_decoded_content()

            # Make sure that the appropriate directories are setup to store the files as needed
            # taken from http://stackoverflow.com/questions/12517451/python-automatically-creating-directories-with-file-output
            if not os.path.exists(os.path.dirname(path)):
                try:
                    
                    os.makedirs(os.path.dirname(path))
                except OSError as exc: # Guard against race condition
                    if exc.errno != errno.EEXIST:
                        raise
            with open(path, 'w') as f:
                f.write(content)
            ## should save this to file
        elif self.is_supported_host(host):
            print "Received a: %d for %s/%s"%(flow.response.status_code, host, path)
        
        flow.reply()
    
    def is_supported_api(self, host):
        """
        Used to limit the capture/stub to specific requests
        """
        return self.is_supported_host(host)
        
    def is_supported_host(self, host):
        """
        Used to limit the capture/stub to specific hosts
        """
        if host.endswith("example.com"):
            return True


config = proxy.ProxyConfig(port=8888)
server = ProxyServer(config)
m = StubMaster(server)
m.run()
