// pages/profile/profile.js
Page({
    data: {
      userId: '12345_test', // User ID 
      userEmail: '12345_test@pku.edu.cn', // User email
      gold: '100', // Fake money each user has
      tasksCompleted: 10, // Example value
      userRating: 4.0 // Example value
    },
  
    onLoad: function () {
      // Fetch user details when the page loads
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
      wx.navigateTo({
        url: '/pages/messages/messages'
      });
    },
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
      wx.navigateTo({
        url: '/pages/settings/settings'
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
    }

  });
  
  