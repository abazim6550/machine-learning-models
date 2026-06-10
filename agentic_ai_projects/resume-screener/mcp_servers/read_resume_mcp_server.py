from pypdf import PdfReader
from pathlib import Path
from mcp.server.fastmcp import FastMCP

mcp = FastMCP('read_resume_mcp_server')

@mcp.tool()
def read_resume():

    resumes_path = Path('docs/resume')

    extracted_resume = {}
    
    for resume in resumes_path.glob('*.pdf'):
    
        resume_file = PdfReader(resume)

        resume_text = "".join(
            page.extract_text() or ""
            for page in resume_file.pages
        )
        extracted_resume[resume.name] = resume_text

    return extracted_resume

if __name__ == '__main__':
    print('read resume server started')
    mcp.run()    