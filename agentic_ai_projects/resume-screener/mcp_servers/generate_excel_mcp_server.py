import pandas as pd
from mcp.server.fastmcp import FastMCP

app = FastMCP('generate excel mcp')

@app.tool()

def generate_excel(message):

    data = pd.DataFrame(message)
    data.to_csv("docs/screened_resume.csv", index= False)

if __name__ == "__main__":
    print('generate excel server started')
    app.run()