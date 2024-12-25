// pages/profile/profile.js
Page({
  data: {
    username: '--', // User ID 
    userEmail: '--', // User email
    gold: '--', // Fake money each user has
    tasksCompleted: '--', // Example value
    tasksPosted: '--', // Example value
  },

  onLoad: function () {
    // Fetch user details when the page loads
    wx.request({
      url: 'http://123.56.18.162:8000/accounts/profile',
      method: 'GET',
      header: {
        'Authorization': "Token " + wx.getStorageSync('token')
      },
      success: res => {
        if (res.statusCode === 200) {
          this.setData({
            username: res.data.username,
            userEmail: res.data.email,
            gold: res.data.gold,
            tasksPosted: res.data.published_tasks.length,
            tasksCompleted: res.data.accepted_finished_tasks.length
          })
          console.log(res.data)
        } else {
          wx.showModal({
            title: '用户信息获取失败',
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

  // Other navigation methods 
  onMessages: function () {
    console.log("on click message")
    wx.navigateTo({
      url: '/pages/messages/messages'
    });
  },
  onReviews: function () {
    wx.navigateTo({
      url: '/pages/finishedTasks/finishedTasks'
    });
  },
  onAccepted: function () {
    wx.navigateTo({
      url: '/pages/acceptedTasks/acceptedTasks'
    });
  },
  onSettings: function () {
    wx.navigateTo({
      url: '/pages/settings/settings'
    });
  },
  onPosts: function () {
    wx.navigateTo({
      url: '/pages/postedTasks/postedTasks'
    });
  },
  
  // Show "About Us" modal
  showAboutUs: function () {
    wx.showModal({
      title: '关于我们',
      content: 'PKUExpress 是一个便捷的校园任务发布平台blablabla。',
      showCancel: false, 
      confirmText: '关闭',
      confirmColor: '#3CC51F', 
      success(res) {
        if (res.confirm) {
          console.log('User closed the modal');
        }
      }
    });
  },

  onLogout: function () {
    wx.request({
      url: 'http://123.56.18.162:8000/accounts/auth/logout',
      method: 'POST',
      header: {
        'Authorization': "Token " + wx.getStorageSync('token')
      },
      success: res => {
        if (res.statusCode === 200) {
          wx.redirectTo({
            'url': '/pages/index/index'
          });
        } else {
          wx.showModal({
            title: '登出失败',
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
  }

});

