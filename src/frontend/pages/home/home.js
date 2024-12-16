Page({
  data: {
    containerHeight: 0,
<<<<<<< HEAD
    list: []
=======
    list: [],
    isListEmpty: true,
>>>>>>> ac4d57e3eaba250c9fdd3cb468a030d322ac2ae9
  },

  // 点击查看详情
  viewDetail(e) {
    const id = e.currentTarget.dataset.id;
    console.log("查看详情，ID:", id);
    // 跳转到详情页面
    wx.navigateTo({
      url: `/pages/detail/detail?id=${id}`
    });
  },

  onLoad() {
    const navibar = this.selectComponent('#navi-bar'); // 选择导航栏组件
    const { paddingTop, naviHeight } = navibar.getNaviInfo();
    const windowHeightPx = wx.getWindowInfo().windowHeight;
    const bottomHeightPx = 140 * wx.getWindowInfo().windowWidth / 750;
    wx.request({
<<<<<<< HEAD
      url: 'http://123.56.18.162:8000/tasks/',
=======
      url: 'http://123.56.18.162:8000/tasks/tasklist',
>>>>>>> ac4d57e3eaba250c9fdd3cb468a030d322ac2ae9
      method: 'GET',
      header: {
        'Authorization': "Token " + wx.getStorageSync('token')
      },
      success: res => {
        if (res.statusCode === 200) {
          this.setData({
            list: res.data,
          });
<<<<<<< HEAD
=======
          if(this.data.list.length!=0)
          {
            this.setData({
              isListEmpty: false,
            });
          }
>>>>>>> ac4d57e3eaba250c9fdd3cb468a030d322ac2ae9
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
    this.setData({
      containerHeight: windowHeightPx - paddingTop - naviHeight - bottomHeightPx - 10,
    });
  },
});
