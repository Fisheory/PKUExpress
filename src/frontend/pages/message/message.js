Page({
  data: {
    receiver: "好友昵称", // 显示的好友昵称
    messages: [], // 聊天消息列表
    inputValue: "", // 输入框内容
    lastMessageId: "",
    socket: null,
    self: ""
  },

  // 页面加载时模拟初始化
  onLoad: function (options) {
    const receiver = options.receiver;
    const self = wx.getStorageSync('profile')['username'];
    this.setData({
      receiver: receiver,
      self: self
    });

    wx.request({
      url: 'http://123.56.18.162:8000/messages/msglist?receiver=' + receiver,
      method: 'GET',
      header: {
        'Authorization': "Token " + wx.getStorageSync('token')
      },

      success: res => {
        if (res.statusCode === 200) {
          this.setData({
            messages: res.data,
            lastMessageId: `message-${res.data[res.data.length - 1].id}`,
          });
          console.log(res.data);
          console.log(this.data.lastMessageId)
        }
        else {
          wx.showModal({
            title: '列表拉取失败',
            showCancel: false,
            confirmText: '确认',
            confirmColor: '#3CC51F',
          });
        }
      },
      fail: () => { 
        wx.showModal({
          title: '连接服务器失败',
          showCancel: false,
          confirmText: '确认',
          confirmColor: '#3CC51F',
        });
      }
    });

    this.createSocketConnection();
  },

  // 输入事件
  onInput: function (e) {
    this.setData({ inputValue: e.detail.value });
  },

  // 发送消息
  sendMessage: function () {
    if (!this.data.inputValue.trim()) return;

    // 添加自己的消息
    const msg = {
      // id: this.data.messages.length + 1,
      receiver: this.data.receiver,
      text: this.data.inputValue.trim(),
      content_type: "text",
    };
    console.log(msg)

    if (this.data.socket && this.data.socket.readyState === 1) {
      this.data.socket.send({
        data: JSON.stringify(msg),
        success: () => {
          console.log('消息发送成功');
        },
        fail: () => {
          console.error('消息发送失败');
        },
      });
    } else {
      console.error('WebSocket 尚未连接');
    }

    this.setData({
      inputValue: "", // 清空输入框
    });
  },

  // 创建 WebSocket 连接
  createSocketConnection() {
    if (this.data.socket) {
      console.log("Socket 已经建立");
      return;
    }

    const socket = wx.connectSocket({
      url: `ws://123.56.18.162:8000/ws/chat/${this.data.receiver}`,  // 服务器 WebSocket URL
      header: {
        'Authorization': "Token " + wx.getStorageSync('token')
      },
      success: () => {
        console.log('Socket 连接成功');
      },
    });

    // 监听 WebSocket 连接打开
    socket.onOpen(() => {
      console.log('WebSocket 连接已打开');
      // 你可以在这里发送一些登录信息或者初始化操作
    });

    // 监听 WebSocket 错误
    socket.onError((err) => {
      console.error('WebSocket 连接失败:', err);
    });

    // 监听 WebSocket 消息
    socket.onMessage((msg) => {
      console.log('收到消息:', msg);
      this.setData({
        messages: [...this.data.messages, JSON.parse(msg.data)["message"]],
        lastMessageId: `message-${this.data.messages[this.data.messages.length - 1].id}`,
      });
      console.log(this.data.messages);
      // 处理消息
    });

    // 监听 WebSocket 关闭
    socket.onClose(() => {
      console.log('WebSocket 连接关闭');
      this.globalData.socket = null;  // 关闭连接后清空
    });

    // 将 socket 对象保存在全局数据中
    this.setData({
      socket: socket
    })
  },

  // 选择表情
  chooseEmoji: function () {
    wx.showToast({ title: "表情选择功能未实现", icon: "none" });
  },

  // 选择图片
  chooseImage: function () {
    wx.showToast({ title: "图片选择功能未实现", icon: "none" });
  },

  onUnload: function () {
    if (this.data.socket) {
      console.log('关闭 WebSocket 连接');
      this.data.socket.close();  // 关闭 WebSocket 连接
    }
  },
});
