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
    message_color: '#000',
    selectedDate: '',
    selectedTime: '',
    rawDate: '',
    rawTime: '',
    imagebase64: ''
  },

  onLoad: function(){
    wx.removeStorageSync('position');
    console.log(wx.getStorageSync('position'))
    const currentDate = new Date();
    const year = currentDate.getFullYear();
    const month = String(currentDate.getMonth() + 1).padStart(2, '0');
    const day = String(currentDate.getDate()).padStart(2, '0');
    const formattedDate = `${year}年${month}月${day}日`;
    const hours = String(currentDate.getHours()).padStart(2, '0');
    const minutes = String(currentDate.getMinutes()).padStart(2, '0');
    const formattedTime = `${hours}:${minutes}`;
    const rDate = `${year}-${month}-${day}`;

    this.setData({
      selectedDate: formattedDate,
      selectedTime: formattedTime,
      rawDate: rDate,
      rawTime: formattedTime,
      address: ""
    });
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
      console.log(this.data.address)
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
    if (!this.isValidTime())
    {
      wx.showModal({
        title: '截止时间错误！',
        content: '任务的截止时间必须为：当前时间 至 一个月以后',
        showCancel: false,
        confirmText: '确认'
      });
      return;
    }

    const fs = wx.getFileSystemManager();
    fs.readFile({
      filePath: this.data.uploadedImages[0],
      encoding: 'base64',
      success: (res) => {
        this.setData({
          imagebase64: res.data
        });
        console.log(this.data.imagebase64);
      }
    });

    wx.request({
      url: 'http://123.56.18.162:8000/tasks/tasklist',
      method: 'POST',
      header: {
        "Authorization": "Token " + wx.getStorageSync('token')
      },
      data: {
        "name": this.data.taskName,
        "description": this.data.details,
        "reward": this.data.payment,
        "end_location": this.data.address,
        "deadline": `${this.data.rawDate}T${this.data.rawTime}:00`,
        "image": this.data.imagebase64
      },
      success: res => {
        console.log(`${this.data.rawDate}T${this.data.rawTime}:00`);
        // Simulate submission success
        if (res.statusCode === 201) {
          wx.showModal({
            title: '提交成功',
            content: '您的任务已成功提交！',
            showCancel: false,
            confirmText: '确认',
            confirmColor: '#3CC51F',
            success: (res) => {
              if (res.confirm) {
                wx.redirectTo({
                  url: '/pages/success/success'
                });
              }
            }
          });
        }
        else {
          const regex = /string='([^']+)'/;
          const match = res.data.msg.match(regex);
          if (match) {
            if(match[1]=="Insufficient gold")
            {
              wx.showModal({
                title: '提交失败',
                content: '余额不足！',
                showCancel: false,
                confirmText: '确认',
                confirmColor: '#3CC51F',
              });
            }
            else if(match[1]=="Reward must be a positive integer")
            {
              wx.showModal({
                title: '提交失败',
                content: '报酬必须为正整数！',
                showCancel: false,
                confirmText: '确认',
                confirmColor: '#3CC51F',
              });
            }
            else if(match[1]=="Deadline must be later than current time")
            {
              wx.showModal({
                title: '提交失败',
                content: '截止时间必须在当前时间以后！',
                showCancel: false,
                confirmText: '确认',
                confirmColor: '#3CC51F',
              });
            }
          }
          else 
          {
            wx.showModal({
              title: '提交失败',
              content: res.data.msg,
              showCancel: false,
              confirmText: '确认',
              confirmColor: '#3CC51F',
            });
          }
        }
      },
      fail: () => {
        wx.showModal({
          title: '连接服务器失败',
          content: res.data.msg,
          showCancel: false,
          confirmText: '确认',
          confirmColor: '#3CC51F',
        });
      }
    });
  },

  // Cancel button click event
  cancelTask: function () {
    wx.redirectTo({
      url: '/pages/home/home',
    })
  },

  // Show message function
  showMessage: function (text, color) {
    this.setData({
      message: text,
      message_color: color
    });
  },

  dateChange: function (e) {
    const date = e.detail.value;
    const [year, month, day] = date.split('-'); // 按"-"分割日期
    const formattedDate = `${year}年${month}月${day}日`;
    this.setData({
      selectedDate: formattedDate,
      rawDate: date
    });
  },

  timeChange: function(e) {
    const time = e.detail.value;
    const [hour, minute] = time.split(':');
    const formattedTime = `${hour}:${minute}`;
    this.setData({
      selectedTime: formattedTime,
      rawTime: time
    });
  },

  isValidTime: function() { 
    const currentDate = new Date();
    const [year, month, day] = this.data.rawDate.split('-').map(Number);
    const [hours, minutes] = this.data.rawTime.split(':').map(Number);
    const rawDateTime = new Date(year, month - 1, day, hours, minutes);
    const oneMonthLater = new Date(currentDate);
    oneMonthLater.setMonth(currentDate.getMonth() + 1);
    return rawDateTime > currentDate && rawDateTime <= oneMonthLater;
  },

  // Navigate to the map page
  navigateToMap: function () {
    wx.navigateTo({
      url: '/pages/map/map' 
    });
  },
  
  onShow: function () {
    const position = wx.getStorageSync('position');
    console.log(position);
    if (position) {
      this.setData({
        address: this.data.address + position['name'] + ','
      });
    }
  },

  onUnload() {
    console.log(this.data.address);
    wx.removeStorageSync('position');
    this.setData({address: ""});
    console.log(this.data.address);
  }
});