// pages/post/post.js
Page({
    data: {
      taskName: '',
      campus: '',
      receivingAddress: '',
      taskAddress: '',
      details: '',
      message: '',
      message_color: '#000'
    },
  
    // Get task name input
    onTaskNameInput: function (e) {
      this.setData({
        taskName: e.detail.value
      });
    },
  
    // Get campus input
    onCampusInput: function (e) {
      this.setData({
        campus: e.detail.value
      });
    },
  
    // Get receiving address input
    onReceivingAddressInput: function (e) {
      this.setData({
        receivingAddress: e.detail.value
      });
    },
  
    // Get task address input
    onTaskAddressInput: function (e) {
      this.setData({
        taskAddress: e.detail.value
      });
    },
  
    // Get details input
    onDetailsInput: function (e) {
      this.setData({
        details: e.detail.value
      });
    },
  
    // Submit button click event
    submitTask: function () {
        // console.log('Submit button clicked');
      // Check for required fields
      if (!this.data.taskName) {
        wx.showModal({
            title: '提示',
            content: '请填写任务名称',  
            showCancel: false,
            confirmText: '确认'
          });
          return;
      }
      if (!this.data.campus) {
        wx.showModal({
            title: '提示',
            content: '请填写校区',
            showCancel: false,
            confirmText: '确认'
          });
          return;
      }
      if (!this.data.receivingAddress) {
        wx.showModal({
            title: '提示',
            content: '请填写收货地址',
            showCancel: false,
            confirmText: '确认'
          });
        return;
      }
      if (!this.data.taskAddress) {
        wx.showModal({
            title: '提示',
            content: '请填写任务地址',
            showCancel: false,
            confirmText: '确认'
          });
        return;
      }
      if (!this.data.details) {
        wx.showModal({
            title: '提示',
            content: '请填写详情',
            showCancel: false,
            confirmText: '确认'
          });
        return;
      }
  
      // Simulate submission success
      wx.showModal({
        title: '提交成功',
        content: '您的任务已成功提交！',
        showCancel: false,
        confirmText: '确认',
        confirmColor: '#3CC51F',
        success: (res) => {
          if (res.confirm) {
            wx.navigateTo({
              url: '/pages/success/success'
            });
          }
        }
      });
    },
  
    // Cancel button click event
    cancelTask: function () {
      wx.navigateBack();
    },
  
    // Show message function
    showMessage: function (text, color) {
      this.setData({
        message: text,
        message_color: color
      });
    }
  });