from pypdf import PdfReader
from mcp.server.fastmcp import FastMCP

mcp = FastMCP('jd_reader_mcp_server')

@mcp.tool()
def read_file():

    jd = PdfReader('docs\jd\Java_JD.pdf')
    jd_text = ''

    for page in jd.pages:
        jd_text += page.extract_text() or ''

    #print('jd_text',jd_text)
    
    return jd_text
    
if __name__ == '__main__':
    print('read jd server started')
    mcp.run()