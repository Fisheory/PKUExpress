Page({
  data: {
    detail: {
      status: 'error',
      deadline: 'error',
      create_time: 'error',
      update_time: 'error',
      finish_time: 'error',
      worker: 'error'
    },
    button_text: '接取任务',
    button_color: '#FFC107',
    task_status: 'error',
    ddl: 'error',
    pub_time: 'error',
    edit_time: 'error',
    com_time: 'error',
    accepter: 'error',
    st_point: 'error',
    message_text: '',
    message_color: 'green',
    image_path: '/test.png' // ***需修改*** 仅用于测试！写好了就改掉！
  },

  formatTime(time, deta) {
    console.log("!");
    // 正则匹配时间格式
    const regex = /^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\+08:00$/;
    if (regex.test(time)) {
      try {
        const date = new Date(time);
        const year = date.getFullYear();
        const month = String(date.getMonth() + 1).padStart(2, '0'); 
        const day = String(date.getDate()).padStart(2, '0');
        const hours = String(date.getHours()).padStart(2, '0');
        const minutes = String(date.getMinutes()).padStart(2, '0');
        const seconds = String(date.getSeconds()).padStart(2, '0');
        console.log("!1");
        return `${year}年${month}月${day}日 ${hours} : ${minutes} : ${seconds}`;
      } catch (error) {
        console.log("!2");
        return 'failed';
      }
    } else {
      console.log("!3");
      return deta;
    }
  },

  onLoad() {
    // 从本地获取item
    const detailItem = wx.getStorageSync("detailItem");
    if (detailItem) {
      this.setData({
        detail: detailItem
      });
    // 判断状态
    if(this.data.detail.status != 'to_be_accepted')
    {
      this.setData({
        button_color: '#888888',
      });
      if(this.data.detail.status == 'accepted')
      {
        this.setData({task_status : '已被接取'});
        this.setData({
          button_text: '已被接取',
        });
      }
      else if(this.data.detail.status == 'finished')
      {
        this.setData({task_status : '已完成'});
        this.setData({
          button_text: '已完成',
        });
      }
      else
      {
        this.setData({task_status : '已过期'});
        this.setData({
          button_text: '已过期',
        });
      }
    }
    else this.setData({task_status : '未被接取'});
    // 转换时间格式
    console.log(this.data.detail.deadline);
    this.setData({ddl: this.formatTime(this.data.detail.deadline, 'unmatch')});
    this.setData({pub_time : this.formatTime(this.data.detail.create_time, 'unmatch')});
    this.setData({edit_time : this.formatTime(this.data.detail.update_time, '无')});
    this.setData({com_time : this.formatTime(this.data.detail.finish_time, '未完成')});
    if (this.data.detail.worker == null)
    {
      this.setData({accepter : '未被接取'});
    }
    else this.setData({accepter : this.data.detail.worker});
    if (this.data.detail.start_location == null)
    {
      this.setData({st_point : '无'});
    }
    else this.setData({st_point : this.data.detail.start_location});
    } else {
      console.error("未找到item");
    }
  },

  submitTask(){
    if(this.data.detail.status == 'to_be_accepted')
    {
      wx.request({
        url: 'http://*************************', // ***需修改*** 修改为正确的接口地址
        method: 'POST',
        data: {
          
          "id": this.data.detail.id
        },
        success: res => {
          if (res.statusCode === 200) {
            this.setData({message_color : 'green'});
            this.setData({message_text : '接取成功！即将回到主页...'});
            // 登录成功后延时1秒跳转
            setTimeout(() => {
              wx.navigateTo({
                url: '/pages/home/home'
              });
            }, 1000);
          } else if (res.statusCode === 400) {
            // 任务已被接取
            this.setData({message_color : 'red'});
            this.setData({message_text : '任务已被接取！即将回到主页...'});
            setTimeout(() => {
              wx.navigateTo({
                url: '/pages/home/home'
              });
            }, 1000);
          }
          else {
            this.setData({message_color : 'red'});
            this.setData({message_text : '未知错误'});
          }
        },
        fail: () => {
          // 显示连接失败消息
          this.setData({message_color : 'red'});
          this.setData({message_text : '连接服务器失败'});
        }
      });
    }
  },

  cancelTask(){
    wx.redirectTo({
      url: "/pages/home/home"
    })
  },

  onUnload() {
    wx.removeStorageSync("detailItem");
  }
});
