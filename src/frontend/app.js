App({
  globalData: {
    socket: null,  // 用于存储 Socket 连接
    userInfo: null,  // 存储用户信息
  },

  onLaunch() {
    // 用户登录或其他初始化操作
  },

  // 创建 WebSocket 连接
  createSocketConnection() {
    if (this.globalData.socket) {
      console.log("Socket 已经建立");
      return;
    }

    const socket = wx.connectSocket({
      url: 'ws://123.56.18.162:8000/ws/user',  // 服务器 WebSocket URL
      header: {
        'Authentication': "Token " + wx.getStorageSync('token')
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
      // 处理消息
    });

    // 监听 WebSocket 关闭
    socket.onClose(() => {
      console.log('WebSocket 连接关闭');
      this.globalData.socket = null;  // 关闭连接后清空
    });

    // 将 socket 对象保存在全局数据中
    this.globalData.socket = socket;
  },

  // 发送消息
  sendMessage(msg) {
    if (this.globalData.socket && this.globalData.socket.readyState === WebSocket.OPEN) {
      this.globalData.socket.send({
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
  },
});
