Page({
  data: {
    containerHeight: 0,
    messageList: [],
    isListEmpty: true
  },

  onShow() {
    const navibar = this.selectComponent('#navi-bar'); // 选择导航栏组件
    const { paddingTop, naviHeight } = navibar.getNaviInfo();
    const windowHeightPx = wx.getWindowInfo().windowHeight;
    this.setData({
      containerHeight: windowHeightPx - paddingTop - naviHeight - 20,
    });
    const self = wx.getStorageSync('profile')['username'];
    console.log(self);
    wx.request({
      url: 'http://123.56.18.162:8000/messages/msglist?last_message',
      method: 'GET',
      header: {
        'Authorization': "Token " + wx.getStorageSync('token')
      },
      success: res => {
        if (res.statusCode === 200) {
          res.data.map(item => {
            if (item.timestamp) {
              const timestamps = item.timestamp.replace('T', ' ').split(':')
              item.timestamp = timestamps[0] + ':' + timestamps[1];
            }

            // 添加 show 属性
            if (item.sender !== self) {
              item.show = item.sender;  // 如果 sender 不是 self，则 show 为 sender
            } else {
              item.show = item.receiver;  // 否则 show 为 receiver
            }
          });
          this.setData({
            messageList: res.data,
          });
          console.log(res.data)
          if (this.data.messageList.length != 0) {
            this.setData({
              isListEmpty: false,
            });
          }
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
  },

  onMessage(e) {
    const receiver = e.currentTarget.dataset.username;
    console.log("打开聊天室，receiver: ", receiver);
    wx.setStorageSync('lasturl', '/pages/messages/messages');
    wx.redirectTo({
      url: `/pages/message/message?receiver=${receiver}`,
    })
  },

  onBack(e) {
    const url = e.dataset.url;
    console.log(url);
    this.selectComponent('#navi-bar').onBack(url);
  }
});
