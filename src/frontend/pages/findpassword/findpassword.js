const defaultAvatarUrl = 'https://mmbiz.qpic.cn/mmbiz/icTdbqWNOwNRna42FI242Lcia07jQodd2FJGIYQfG0LAJGFxM4FbnQP6yfMxBgJ0F3YRqJCJ1aPAK2dQagdusBZg/0'

Page({
  data: {
    username: '',
    message: '',
    message_color: '#000',
    message_button: '@pku.edu.cn',
    full_username: '',
    button_text: '发送',
    button_color: 'rgba(255, 142, 79, 1)',
    isButtonDisabled: false,
    countdown: 60  
  },

  // 获取用户名输入
  onUsernameInput: function (e) {
    this.setData({
      username: e.detail.value
    });
  },

  onSwitch: function () {
    if (this.data.message_button ===  '@pku.edu.cn') {
      this.setData({
        message_button: '@stu.pku.edu.cn'
      });
    }
    else if (this.data.message_button ===  '@stu.pku.edu.cn') {
      this.setData({
        message_button: '@alumni.pku.edu.cn'
      });
    }
    else {
      this.setData({
        message_button: '@pku.edu.cn'
      });
    }
  },

  // 发送按钮点击事件
  onSend: function () {
    if (this.data.isButtonDisabled){
      this.showMessage('请稍后再次发送！', 'red');
      return;
    }
    // 检查输入框内容
    if (!this.data.username) {
      this.showMessage('请填写用户名', 'red');
      return;
    }
    this.setData({
      full_username: this.data.username + this.data.message_button
    });

    // 发送找回密码邮件请求
    const { full_username } = this.data;
    wx.request({
      url: 'https://your-server-domain.com/findpassword',
      method: 'POST',
      data: {
        full_username,
      },
      success: res => {
        if (res.data.code === 200) {
          this.showMessage('发送邮件成功，请查看您的邮箱', 'green');
          this.setData({
            isButtonDisabled: true,
            button_color: '#f5b273',
            button_text: `重新发送（${this.data.countdown}s）`
          });
          let countdown = this.data.countdown;
          const timer = setInterval(() => {
            countdown--;
            this.setData({
              button_text: `重新发送（${countdown}s）`
            });
            if (countdown === 0) {
              clearInterval(timer);
              this.setData({
                button_text: '发送',
                button_color: '#f87e0b',
                isButtonDisabled: false
              });
            }
          }, 1000);
        }
      },
      fail: () => {
        this.showMessage('连接服务器失败', 'red');
      }
    });
    
  },

  // 返回主页
  onReturn: function () {
    wx.navigateTo({
      url: '/pages/index/index'
    });
  },

  // 显示消息
  showMessage: function (text, color) {
    this.setData({
      message: text,
      message_color: color
    });
  }
});
