from routes.index import index
from routes.login import login, auth, login_failed, logout


ROOT = [
    {
        "path": "/",
        "func": index,
        "methods": ["GET"]
    },
    {
        "path": "/login",
        "func": login,
        "methods": ["GET"]
    },
    {
        "path": "/login/auth",
        "func": auth,
        "methods": ["GET"]
    },
    {
        "path": "/login/failed",
        "func": login_failed,
        "methods": ["GET"]
    },
    {
        "path": "/logout",
        "func": logout,
        "methods": ["GET"]
    }
]
