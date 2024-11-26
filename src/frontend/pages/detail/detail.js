Page({
  data: {
    id: "",
    notAccepted: true,
    detail: {
      status: '无',
      deadline: '无',
      create_time: '无',
      update_time: '无',
      finish_time: '无',
      worker: '无'
    },
    button_text: '接取任务',
    button_color: '#FFC107',
    task_status: '无',
    ddl: '无',
    pub_time: '无',
    edit_time: '无',
    com_time: '无',
    accepter: '无',
    st_point: '无',
    message_text: '',
    message_color: 'green',
    image_path: '/test.png',
    isToBeAccepted: false,
    isAccepted: false,
    isFinished: false,
    isExpired: false
  },

  formatTime(time, deta) {
    console.log("!");
    // 正则匹配时间格式
    console.log(time)
    const regex = /^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?\+08:00$/;
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
        return `${year}年${month}月${day}日 ${hours}:${minutes}:${seconds}`;
      } catch (error) {
        console.log("!2");
        return 'failed';
      }
    } else {
      console.log("!3");
      return deta;
    }
  },

  onLoad: function (options) {
    // 从本地获取item
    const id = options.id;
    this.setData({id})
    wx.request({
      url: `http://123.56.18.162:8000/tasks/tasklist/${id}`, // 替换为后端实际接口
      method: 'GET',
      success: (res) => {
        if (res.statusCode === 200) {
          this.setData({ detail: res.data }); // 设置数据到页面
          // 判断状态
          if (this.data.detail.status !== 'to_be_accepted') {

            if (this.data.detail.status === 'accepted') {
              this.setData({
                task_status: '已被接取',
              });
            } else if (this.data.detail.status === 'finished') {
              this.setData({
                task_status: '已完成',
              });
            } else {
              this.setData({
                task_status: '已过期',
              });
            }
          } else {
            this.setData({ task_status: '未被接取' });
          }

          // 转换时间格式
          this.setData({
            ddl: this.formatTime(this.data.detail.deadline, 'unmatch'),
            pub_time: this.formatTime(this.data.detail.create_time, 'unmatch'),
            edit_time: this.formatTime(this.data.detail.update_time, '无'),
            com_time: this.formatTime(this.data.detail.finish_time, '未完成'),
            accepter: this.data.detail.worker || '未被接取',
            st_point: this.data.detail.start_location || '无',
          });
          console.log(this.data.detail);
          const status = this.data.detail.status;
          console.log("status:", status);
          this.setData({
            isToBeAccepted: status === 'to_be_accepted',
            isAccepted: status === 'accepted',
            isFinished: status === 'finished',
            isExpired: !['to_be_accepted', 'accepted', 'finished'].includes(status),
          });
        } else {
          wx.showToast({
            title: '加载失败',
            icon: 'none',
          });
        }
      },
      fail: () => {
        wx.showToast({
          title: '网络错误',
          icon: 'none',
        });
      },
    });
  },

  submitTask(){
    if(this.data.detail.status == 'to_be_accepted')
    {
      const id = this.data.id;
      wx.request({
        url: `http://123.56.18.162:8000/tasks/tasklist/${id}`,
        method: 'PATCH',
        data: {
          'status': 'accepted'
        },
        header: {
          'Authorization': "Token " + wx.getStorageSync('token')
        },
        success: res => {
          if (res.statusCode === 200) {
            this.setData({message_color : 'green'});
            this.setData({message_text : '接取成功！即将回到主页...'});
            // 延时1秒跳转
            setTimeout(() => {
              wx.navigateTo({
                url: '/pages/home/home'
              });
            }, 1000);
          } else if (res.statusCode === 400) {
            // 任务已被接取
            this.setData({message_color : 'red'});
            this.setData({message_text : '任务已被接取！即将回到主页...'});
            console.log(res.data.msg)
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

  finishTask(){
    if(this.data.detail.status == 'accepted')
    {
      const id = this.data.id;
      wx.request({
        url: `http://123.56.18.162:8000/tasks/tasklist/${id}`,
        method: 'PATCH',
        data: {
          'status': 'finished'
        },
        header: {
          'Authorization': "Token " + wx.getStorageSync('token')
        },
        success: res => {
          if (res.statusCode === 200) {
            this.setData({message_color : 'green'});
            this.setData({message_text : '任务完成！即将回到主页...'});
            // 延时1秒跳转
            setTimeout(() => {
              wx.navigateTo({
                url: '/pages/home/home'
              });
            }, 1000);
          } else if (res.statusCode === 400) {
            // 任务已被接取
            this.setData({message_color : 'red'});
            this.setData({message_text : res.data.msg});
            console.log(res.data.msg)
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
