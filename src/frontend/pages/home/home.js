Page({
  data: {
    containerHeight: 0,
    list: [],
    isListEmpty: true,
  },

  // 点击查看详情
  viewDetail(e) {
    const id = e.currentTarget.dataset.id;
    console.log("查看详情，ID:", id);
    // 跳转到详情页面
    wx.setStorageSync('lasturl1', '/pages/home/home');
    wx.redirectTo({
      url: `/pages/detail/detail?id=${id}`
    });
  },

  onLoad(options) {
    const navibar = this.selectComponent('#navi-bar'); // 选择导航栏组件
    const { paddingTop, naviHeight } = navibar.getNaviInfo();
    const windowHeightPx = wx.getWindowInfo().windowHeight;
    const bottomHeightPx = 140 * wx.getWindowInfo().windowWidth / 750;
    let searchUrl = `http://123.56.18.162:8000/tasks/tasklist`
    if (options.search) {
      searchUrl += `?search=${options.search}`
      const navibar = this.selectComponent('#navi-bar');
      if (options.search) {
        navibar.setData({
          searchQuery: options.search
        });
      }
    }
    console.log(searchUrl)
    wx.request({
      url: searchUrl,
      method: 'GET',
      header: {
        'Authorization': "Token " + wx.getStorageSync('token')
      },
      success: res => {
        if (res.statusCode === 200) {
          this.setData({
            list: res.data,
          });
          if (this.data.list.length != 0) {
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
    this.setData({
      containerHeight: windowHeightPx - paddingTop - naviHeight - bottomHeightPx - 10,
    });
  },
  search(e) {
    console.log(e.detail);
    wx.redirectTo({
      url: `/pages/home/home?search=${e.detail}`,
    })
  }
});