Page({
  data: {
    containerHeight: 0,
    messageList: [
      {
        id: 1,
        avatar: '/path/to/avatar1.png',
        nickname: '张三',
        lastMessage: '你好，最近怎么样？',
        unreadCount: 2
      },
      {
        id: 2,
        avatar: '/path/to/avatar2.png',
        nickname: '李四',
        lastMessage: '收到文件了吗？',
        unreadCount: 0
      },
      {
        id: 1,
        avatar: '/path/to/avatar1.png',
        nickname: '张三',
        lastMessage: '你好，最近怎么样？',
        unreadCount: 2
      },
      {
        id: 1,
        avatar: '/path/to/avatar1.png',
        nickname: '张三',
        lastMessage: '你好，最近怎么样？',
        unreadCount: 2
      },
      {
        id: 1,
        avatar: '/path/to/avatar1.png',
        nickname: '张三',
        lastMessage: '你好，最近怎么样？',
        unreadCount: 2
      },
      {
        id: 1,
        avatar: '/path/to/avatar1.png',
        nickname: '张三',
        lastMessage: '你好，最近怎么样？',
        unreadCount: 2
      },
      {
        id: 1,
        avatar: '/path/to/avatar1.png',
        nickname: '张三',
        lastMessage: '你好，最近怎么样？',
        unreadCount: 2
      },
      {
        id: 1,
        avatar: '/path/to/avatar1.png',
        nickname: '张三',
        lastMessage: '你好，最近怎么样？',
        unreadCount: 2
      },
      {
        id: 1,
        avatar: '/path/to/avatar1.png',
        nickname: '张三',
        lastMessage: '你好，最近怎么样？',
        unreadCount: 2
      },
      {
        id: 1,
        avatar: '/path/to/avatar1.png',
        nickname: '张三',
        lastMessage: '你好，最近怎么样？',
        unreadCount: 2
      },
      {
        id: 3,
        avatar: '/path/to/avatar3.png',
        nickname: '王五',
        lastMessage: '晚餐时间定了',
        unreadCount: 5
      }
    ]
  },

  onLoad() {
    const navibar = this.selectComponent('#navi-bar'); // 选择导航栏组件
    const { paddingTop, naviHeight } = navibar.getNaviInfo();
    const windowHeightPx = wx.getWindowInfo().windowHeight;
    this.setData({
      containerHeight: windowHeightPx - paddingTop - naviHeight - 20,
    });
  },

  onMessage(e) {
    const receiver = e.currentTarget.dataset.nickname;
    console.log("打开聊天室，receiver: ", receiver);
    wx.navigateTo({
      url: `/pages/message/message?receiver=${receiver}`,
    })
  }
});
