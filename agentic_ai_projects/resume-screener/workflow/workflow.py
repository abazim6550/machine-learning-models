from mcp_servers.jd_reader_mcp_server import read_file
from mcp_servers.read_resume_mcp_server import read_resume
from services.recommendation import generate_recommendation
from mcp_servers.generate_excel_mcp_server import generate_excel
import json

def trigger_workflow():

    jd_text = read_file()

    resume_text = read_resume()

    result = []
    for resume in resume_text.values():
        #print(resume)
        response = generate_recommendation(jd=jd_text, resume=resume)

        result.append(response)
    generate_excel(result)  
        

if __name__ == '__main__':
   print('read resume server started')
   trigger_workflow()    