const Crypto = require("crypto-js")

Page({
  data: {
    username: '',
    email: '',
    password: '',
    password_confirm: '',
<<<<<<< HEAD
    message: '',
    message_color: '#000',
    message_button: '@pku.edu.cn',
    full_email: ''
=======
    verification_code: '',
    message: '',
    message_color: '#000',
    message_button: '@pku.edu.cn',
    full_email: '',
    isVerificationSent: false
>>>>>>> ac4d57e3eaba250c9fdd3cb468a030d322ac2ae9
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

<<<<<<< HEAD
=======
  // 获取验证码输入
  onVerificationCodeInput: function (e) {
    this.setData({
      verification_code: e.detail.value
    })
  },

>>>>>>> ac4d57e3eaba250c9fdd3cb468a030d322ac2ae9
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
<<<<<<< HEAD
=======
    if(!this.data.verification_code){
      this.showMessage('请填写验证码', 'red');
      return;
    }
>>>>>>> ac4d57e3eaba250c9fdd3cb468a030d322ac2ae9

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
<<<<<<< HEAD
    wx.request({
      url: 'http://123.56.18.162:8000/accounts/register/',
=======
    const verification_code = this.data.verification_code
    wx.request({
      url: 'http://123.56.18.162:8000/accounts/auth/register',
>>>>>>> ac4d57e3eaba250c9fdd3cb468a030d322ac2ae9
      method: 'POST',
      data: {
        "username": username,
        "email": full_email,
<<<<<<< HEAD
        "password": encryptedPassword
      },
      success: res => {
        if (res.statusCode === 200) {
=======
        "password": encryptedPassword,
        "verification_code": verification_code
      },
      success: res => {
        if (res.statusCode === 201) {
>>>>>>> ac4d57e3eaba250c9fdd3cb468a030d322ac2ae9
          this.showMessage('注册成功，即将返回登录页面...', 'green');
          // 注册成功后延时1秒跳转
          setTimeout(() => {
            wx.navigateTo({
              url: '/pages/index/index'
            });
          }, 1000);
        } 
        else {
<<<<<<< HEAD
          this.showMessage(res.data.msg, 'red');
=======
          if(res.data.msg=="Email already exists")
          {
            this.showMessage("用户已存在", 'red');
          }
          else if(res.data.msg=="Email must be a pku email")
          {
            this.showMessage("必须输入北大邮箱", 'red');
          }
          if(res.data.msg=="Verification code not found")
          {
            this.showMessage("未输入验证码", 'red');
          }
          else if(res.data.msg=="Invalid verification code")
          {
            this.showMessage("验证码错误", 'red');
          }
          else this.showMessage(res.data.msg, 'red');
        }
      },
      fail: () => {
        this.showMessage('连接服务器失败', 'red');
      }
    });
  },
  
  onSendVerificationCode: function () {
    if (!this.data.email) {
      this.showMessage('请填写邮箱', 'red');
      return;
    }
    this.setData({
      full_email: this.data.email + this.data.message_button
    });
    const full_email = this.data.full_email;
    wx.request({
      url: 'http://123.56.18.162:8000/accounts/auth/verification-code',
      method: 'POST',
      data: {
        "email": full_email,
        "usage": "register"
      },
      success: res => {
        if (res.statusCode === 201) {
          this.showMessage('发送验证码成功', 'green');
          this.setData({
            isVerificationSent: true
          })
        } else {
          if(res.data.msg=="Email already exists")
          {
            this.showMessage("用户已存在", 'red');
          }
          else if(res.data.msg=="Email must be a pku email")
          {
            this.showMessage("必须输入北大邮箱", 'red');
          }
          else if(res.data.msg=="Email does not exist")
          {
            this.showMessage("用户不存在", 'red');
          }
          else if(res.data.msg=="Please wait for 1 minute before sending another token")
          {
            this.showMessage("发送频率过快，请等待1分钟后再次发送", 'red');
          }
          else if(res.data.msg=="Failed to send email")
          {
            this.showMessage("发送邮件失败", 'red');
          }
          else this.showMessage(res.data.msg, 'red');
>>>>>>> ac4d57e3eaba250c9fdd3cb468a030d322ac2ae9
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
