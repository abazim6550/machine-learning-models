from mcp.server.fastmcp import FastMCP

mcp = FastMCP("test")

@mcp.tool()
def hello() -> str:
    
    return "hello"

if __name__ == "__main__":
    print('hellow')
    mcp.run()