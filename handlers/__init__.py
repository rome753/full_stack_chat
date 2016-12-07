handlers = []


import login
handlers += [
    (r"/verify_code", login.VerifyCodeHandler),
    (r"/register", login.RegisterHandler),
    (r"/login", login.LoginHandler),
    (r"/logout", login.LogoutHandler)
]


import chat
handlers += [
    (r"/chat", chat.ChatHandler),
]


import user
handlers += [
    (r"/user", user.UserHandler),
    (r"/avatar", user.AvatarHandler)
]
