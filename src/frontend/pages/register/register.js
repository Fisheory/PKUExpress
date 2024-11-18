const Crypto = require("crypto-js")

Page({
  data: {
    username: '',
    email: '',
    password: '',
    password_confirm: '',
    message: '',
    message_color: '#000',
    message_button: '@pku.edu.cn',
    full_email: ''
  },

  // 获取用户名输入
  onUsernameInput: function (e) {
    this.setData({
      username: e.detail.value
    });
  },

  // 获取邮箱输入
  onEmailInput: function (e) {
    this.setData({
      email: e.detail.value
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

  // 获取密码输入
  onPasswordInput: function (e) {
    this.setData({
      password: e.detail.value
    });
  },

  // 获取确认密码输入
  onPasswordConfirmInput: function (e) {
    this.setData({
      password_confirm: e.detail.value
    });
  },

  // 注册按钮点击事件
  onRegister: function () {
    // 检查输入框内容
    if (!this.data.username) {
      this.showMessage('请填写用户名', 'red');
      return;
    }
    if (!this.data.email) {
      this.showMessage('请填写邮箱', 'red');
      return;
    }
    if (!this.data.password) {
      this.showMessage('请填写密码', 'red');
      return;
    }
    console.info(111);
    if (!this.data.password_confirm)
    {
      this.showMessage('请确认密码', 'red');
      return;
    }
    if (this.data.password_confirm != this.data.password)
    {
      this.showMessage('密码与确认密码不匹配', 'red');
      return;
    }

    this.setData({
      full_email: this.data.email + this.data.message_button
    });

    // 加密密码
    const encryptedPassword = this.encryptPassword(this.data.password);
    console.log("encrypted");
    console.log(encryptedPassword)

    // 发送注册请求
    const full_email = this.data.full_email;
    const username = this.data.username;
    wx.request({
      url: 'http://123.56.18.162:8000/accounts/register/',
      method: 'POST',
      data: {
        "username": username,
        "email": full_email,
        "password": encryptedPassword
      },
      success: res => {
        if (res.statusCode === 200) {
          this.showMessage('注册成功，即将返回登录页面...', 'green');
          // 注册成功后延时1秒跳转
          setTimeout(() => {
            wx.navigateTo({
              url: '/pages/index/index'
            });
          }, 1000);
        } 
        else {
          this.showMessage(res.data.msg, 'red');
        }
      },
      fail: () => {
        this.showMessage('连接服务器失败', 'red');
      }
    });
  },

  // 返回登录
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
  },

  // 加密密码函数
  encryptPassword: function (password) {
    return Crypto.SHA256(password).toString(Crypto.enc.Hex); // 使用 SHA256 加密并转换为十六进制
  }
});