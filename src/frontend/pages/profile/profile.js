// pages/profile/profile.js
Page({
    data: {
<<<<<<< HEAD
      userId: '12345_test', // User ID 
      userEmail: '12345_test@pku.edu.cn', // User email
      gold: '100', // Fake money each user has
      tasksCompleted: 10, // Example value
      userRating: 4.0 // Example value
=======
      username: '--', // User ID 
      userEmail: '--', // User email
      gold: '--', // Fake money each user has
      tasksCompleted: '--', // Example value
      tasksPosted: '--', // Example value
>>>>>>> ac4d57e3eaba250c9fdd3cb468a030d322ac2ae9
    },
  
    onLoad: function () {
      // Fetch user details when the page loads
<<<<<<< HEAD
      this.fetchUserId();
      this.fetchUserEmail();
      this.fetchGold();
    },
  
    // Fetch User ID
    fetchUserId: function () {
    },

    // Fetch User email
    fetchUserEmail: function () {
    },

    fetchGold: function () {
    },
  
    // Other navigation methods 
    goToMessages: function () {
=======
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
>>>>>>> ac4d57e3eaba250c9fdd3cb468a030d322ac2ae9
      wx.navigateTo({
        url: '/pages/messages/messages'
      });
    },
<<<<<<< HEAD
    goToReviews: function () {
      wx.navigateTo({
        url: '/pages/reviews/reviews'
      });
    },
    goToOrders: function () {
      wx.navigateTo({
        url: '/pages/orders/orders'
      });
    },
    goToSettings: function () {
=======
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
>>>>>>> ac4d57e3eaba250c9fdd3cb468a030d322ac2ae9
      wx.navigateTo({
        url: '/pages/settings/settings'
      });
    },
<<<<<<< HEAD
    
    // Show "About Us" modal
    showAboutUs: function () {
        wx.showModal({
=======
    onPosts: function () {
      wx.navigateTo({
        url: '/pages/postedTasks/postedTasks'
      });
    },
    
    // Show "About Us" modal
    showAboutUs: function () {
      wx.showModal({
>>>>>>> ac4d57e3eaba250c9fdd3cb468a030d322ac2ae9
        title: '关于我们',
        content: 'PKUExpress 是一个便捷的校园任务发布平台blablabla。',
        showCancel: false, 
        confirmText: '关闭',
        confirmColor: '#3CC51F', 
        success(res) {
<<<<<<< HEAD
            if (res.confirm) {
            console.log('User closed the modal');
            }
        }
        });
=======
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
            wx.navigateTo({
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
>>>>>>> ac4d57e3eaba250c9fdd3cb468a030d322ac2ae9
    }

  });
  
  