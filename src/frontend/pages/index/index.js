// 引入加密库
const Crypto = require("crypto-js");

const defaultAvatarUrl = 'https://mmbiz.qpic.cn/mmbiz/icTdbqWNOwNRna42FI242Lcia07jQodd2FJGIYQfG0LAJGFxM4FbnQP6yfMxBgJ0F3YRqJCJ1aPAK2dQagdusBZg/0';

Page({
  data: {
    avatarUrl: defaultAvatarUrl,
    username: '',
    password: '',
    message: '',
    message_color: '#000',
    message_button: '@pku.edu.cn',
    full_username: '',
    userInfo: null
  },

  // 获取邮箱输入
  onUsernameInput: function (e) {
    this.setData({
      username: e.detail.value
    });
  },

  // 获取密码输入
  onPasswordInput: function (e) {
    this.setData({
      password: e.detail.value
    });
  },

  onSwitch: function () {
    if (this.data.message_button === '@pku.edu.cn') {
      this.setData({
        message_button: '@stu.pku.edu.cn'
      });
    } else if (this.data.message_button === '@stu.pku.edu.cn') {
      this.setData({
        message_button: '@alumni.pku.edu.cn'
      });
    } else {
      this.setData({
        message_button: '@pku.edu.cn'
      });
    }
  },

  // 登录按钮点击事件
  onLogin: function () {
    // 检查输入框内容
    if (!this.data.username) {
      this.showMessage('请填写邮箱', 'red');
      return;
    }
    if (!this.data.password) {
      this.showMessage('请填写密码', 'red');
      return;
    }
    this.setData({
      full_username: this.data.username + this.data.message_button
    });

    // 加密密码
    const encryptedPassword = this.encryptPassword(this.data.password);
    console.log("encrypted");
    console.log(encryptedPassword)

    // 发送登录请求
    const full_username = this.data.full_username;
    wx.request({
      url: 'http://123.56.18.162:8000/accounts/auth/login', // 修改为正确的接口地址
      method: 'POST',
      data: {
        "email": full_username,
        "password": encryptedPassword
      },
      success: res => {
        if (res.statusCode === 200) {
          // 提取 token 并保存到本地存储
          const token = res.data.token; // 假设服务端返回的 JSON 中有一个 "token" 字段
          if (token) {
            wx.setStorageSync('token', token); // 保存 token 到本地
          }
          wx.setStorageSync(
            'profile', {
              "email": full_username,
              "username": res.data.username,
            }
          );
          console.log(wx.getStorageSync('profile'));
          console.log(token);
          // 显示登录成功消息
          this.showMessage('登录成功', 'green');
          // 登录成功后延时1秒跳转
          setTimeout(() => {
            wx.navigateTo({
              url: '/pages/home/home'
            });
          }, 1000);
        } else {
          // 显示错误消息
          this.showMessage(res.data.msg, 'red');
        }
      },
      fail: () => {
        // 显示连接失败消息
        this.showMessage('连接服务器失败', 'red');
      }
    });
  },
  
  // 注册跳转
  goToRegister: function () {
    wx.navigateTo({
      url: '/pages/register/register'
    });
  },

  // 找回密码跳转
  goToFindPassword: function () {
    wx.navigateTo({
      url: '/pages/reset/reset'
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
