# full_stack_chat
这是一个开发中的全栈式即时聊天工具，包括python后台、Android客户端和html网页聊天室，后台搭建在自己的个人服务器(http://rome753.cc)上。目前已实现基本的登录注册和聊天功能。
只要你会Android/ios/python/js/html中的一种，就可以参加这个项目（ios本人不熟，欢迎开发ios客户端），欢迎提交Pull Request，有bug或者功能上的建议可以创建Issue，也可以直接到聊天室吼一声~

* 网页聊天室地址 <http://rome753.cc/chatroom>
* Android客户端项目地址 <https://github.com/rome753/full_stack_chat_android>

## 架构
- 开发语言：python 2.7
- 网络框架：tornado 4.4.2
- 数据库：mongodb

## 功能（~~已实现标记~~）
- ~~注册~~
> 检测邮箱和用户名是否已存在

- ~~登录~~
> 验证用户名和密码，登录成功后设置cookie(fsid=xxx...xxx)

- ~~即时聊天~~ 
> 使用tornado中的websocket长连接实现。已连接上的用户自动保存到内存集合中，连接断开则移除。由于websocket是tcp层，不能直接使用http层的header发送cookie，连接上后客户端在message中主动发送一次cookie信息。聊天室通过遍历用户集合并发送消息实现，单对单聊天通过cookie中记录的用户信息实现。

- 邮箱验证码
- **聊天记录管理**
- **发送图片**
- 重复登录检测
- 第三方登录对接

## 接口
- [register](#register)
- [login](#login)
- [chat](#chat)

#### "register" <span id='register' />
```
post: {
	email,
	username,
	password
	}
```

#### "login" <span id='login' />
```
post: {
	username,
	password
}
```

#### "chat" <span id='chat' />
```js
ws: {} //websocket直接连接 
send: {// 发送的消息格式
	type, //int
	to,
	msg
}
receive: {// 接收的消息格式
	type, //int
	from,
	to,
	msg
}
```
