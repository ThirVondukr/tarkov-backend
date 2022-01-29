import sys

import uvicorn

if __name__ == "__main__":
    sys.path.append("src")
    uvicorn.run("app:create_app", factory=True, use_colors=False)
