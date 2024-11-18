// pages/post/post.js
Page({
    data: {
      taskName: '',
      campus: '',
      address: '',
      payment: '',
      details: '',
      message: '',
      uploadedImages: [],
      message_color: '#000'
    },

    // Get task name input
    onTaskNameInput: function (e) {
      this.setData({
        taskName: e.detail.value
      });
    },
  
    // Get address input
    onAddressInput: function (e) {
      this.setData({
        address: e.detail.value
      });
    },
  
    // Get payment input
    onPaymentInput: function (e) {
      this.setData({
        payment: e.detail.value
      });
    },

    // Get details input
    onDetailsInput: function (e) {
      this.setData({
        details: e.detail.value
      })
    },

    // Get details input
    uploadImage: function () {
      wx.chooseMedia({
        count: 1, // 限制选择1张图片
        mediaType: ['image'],
        sourceType: ['album', 'camera'],
        success: (res) => {
          if (Array.isArray(res.tempFiles) && res.tempFiles.length > 0) {
            const newImage = res.tempFiles[0].tempFilePath;
            this.setData({
              uploadedImages: [newImage] // 覆盖之前的图片
            });
          }
        },
        fail: (err) => {
          console.error('选择图片失败:', err);
          wx.showToast({
            title: '选择图片失败',
            icon: 'none'
          });
        }
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
      if (!this.data.address) {
        wx.showModal({
            title: '提示',
            content: '请填写途径点',
            showCancel: false,
            confirmText: '确认'
          });
          return;
      }
      if (!this.data.payment) {
        wx.showModal({
            title: '提示',
            content: '请填写金额',
            showCancel: false,
            confirmText: '确认'
          });
        return;
      }
      if (!this.data.details) {
        wx.showModal({
            title: '提示',
            content: '请填写任务详情',
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