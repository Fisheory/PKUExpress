Page({
  data: {
    id: "",
    detail: {
      status: '无',
      deadline: '无',
      create_time: '无',
      update_time: '无',
      finish_time: '无',
      worker: '无',
      imagebase64: '',
      publisher: ''
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
    image_path: '',
    isToBeAccepted: false,
    isAckFinished: false,
    isAccepted: false,
    isFinished: false,
    isExpired: false,
    isToEdit: false,
    isPoster: false,
    selfemail: '',
    lasturl1: ''
  },

  formatTime(time, deta) {
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
        return `${year}年${month}月${day}日 ${hours}:${minutes}:${seconds}`;
      } catch (error) {
        return 'failed';
      }
    } else {
      return deta;
    }
  },

  onLoad: function (options) {
    // 从本地获取item
    const id = options.id;
    this.setData({id})
    this.setData({
      lasturl1: wx.getStorageSync('lasturl1')
    });
    wx.request({
      url: `http://123.56.18.162:8000/tasks/tasklist/${id}`, // 替换为后端实际接口
      method: 'GET',
      success: (res) => {
        if (res.statusCode === 200) {
          console.log(res.data.image);
          this.setData({ detail: res.data }); // 设置数据到页面
          if(this.data.detail.image)
          {
            this.setData({
              image_path:  'http://123.56.18.162:8000' + this.data.detail.image
            });
          }
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
            isAckFinished: status === 'ack_finished',
            isFinished: status === 'finished',
            isExpired: !['to_be_accepted', 'accepted', 'finished', 'ack_finished'].includes(status),
          });
        } else {
          wx.showToast({
            title: '加载失败',
            icon: 'none',
          });
        }

        console.log("!!!!!!!!!!!!!!!!!!!!!");
         wx.request({
          url: 'http://123.56.18.162:8000/accounts/profile',
          method: 'GET',
          header: {
            'Authorization': "Token " + wx.getStorageSync('token')
          },
          success: res => {
            if (res.statusCode === 200) {
              this.setData({
                selfemail: res.data.email,
              });
              console.log(this.data.selfemail);
              console.log(this.data.detail.publisher);
              const username = wx.getStorageSync('profile')['username'];
              if(username === this.data.detail.publisher)
              {
                this.setData({
                  isPoster: true
                });
              }
            } else {
              wx.showModal({
                title: '用户信息获取失败',
                showCancel: false,
                confirmText: '确认',
                confirmColor: '#3CC51F',
              });
            }
          },
          fail: () => {
            wx.showModal({
              title: '连接服务器失败',
              showCancel: false,
              confirmText: '确认',
              confirmColor: '#3CC51F',
            });
          }
        });
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
            wx.showToast({
              title: '接取成功！',
              icon: 'none',
            });
            // 延时1秒跳转
            setTimeout(() => {
              wx.redirectTo({
                url: '/pages/home/home'
              });
            }, 1000);
          } else if (res.statusCode === 400) {
            // 任务已被接取
            wx.showToast({
              title: '任务已被接取！',
              icon: 'none',
            });
            setTimeout(() => {
              wx.redirectTo({
                url: '/pages/home/home'
              });
            }, 1000);
          }
          else {
            wx.showToast({
              title: '未知错误',
              icon: 'none',
            });
          }
        },
        fail: () => {
          // 显示连接失败消息
          wx.showToast({
            title: '连接服务器失败',
            icon: 'none',
          });
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
            wx.showToast({
              title: '任务完成！等待对方确认...',
              icon: 'none',
            });
            // 延时1秒跳转
            setTimeout(() => {
              wx.redirectTo({
                url: '/pages/home/home'
              });
            }, 1000);
          } else if (res.statusCode === 400) {
            // 任务已被接取
            wx.showToast({
              title: res.data.msg,
              icon: 'none',
            });
            setTimeout(() => {
              wx.redirectTo({
                url: '/pages/home/home'
              });
            }, 1000);
          }
          else {
            wx.showToast({
              title: '未知错误',
              icon: 'none',
            });
          }
        },
        fail: () => {
          // 显示连接失败消息
          wx.showToast({
            title: '连接服务器失败',
            icon: 'none',
          });
        }
      });
    }
  },

  cancelTask(){
    wx.redirectTo({
      url: "/pages/home/home"
    })
  },

  editTask(){
    const taskData = {
      id: this.data.id,
      taskName: this.data.detail.name,
      details: this.data.detail.description,
      payment: this.data.detail.reward,
      address: this.data.detail.end_location,
      ddl: this.data.detail.deadline,
      uploadedImages: this.data.image_path
    };
    
    const url = `/pages/edittask/edittask?id=${encodeURIComponent(taskData.id)}&taskName=${encodeURIComponent(taskData.taskName)}&details=${encodeURIComponent(taskData.details)}&payment=${encodeURIComponent(taskData.payment)}&address=${encodeURIComponent(taskData.address)}&ddl=${encodeURIComponent(taskData.ddl)}&uploadedImages=${encodeURIComponent(taskData.uploadedImages)}`;
    
    wx.navigateTo({
      url: url
    });
  },

  confirmTask(){
    const id = this.data.id;
    wx.request({
      url: `http://123.56.18.162:8000/tasks/tasklist/${id}`,
      method: 'PATCH',
      data: {
        'status': 'ack_finished'
      },
      header: {
        'Authorization': "Token " + wx.getStorageSync('token')
      },
      success: res => {
        if (res.statusCode === 200) {
          this.setData({message_color : 'green'});
          this.setData({message_text : '确认完成！即将回到主页...'});
          // 延时1秒跳转
          setTimeout(() => {
            wx.redirectTo({
              url: '/pages/home/home'
            });
          }, 1000);
        }
        else{
          wx.showToast({
            title: '未知错误',
            icon: 'none',
          });
        }
      },
      fail: () => {
        wx.showToast({
          title: '连接服务器失败',
          icon: 'none',
        });
      }
    })
  },

  base64ToArrayBuffer: function(params){
    const binaryString = wx.base64ToBinary(base64);
    const length = binaryString.length;
    const arrayBuffer = new ArrayBuffer(length);
    const view = new Uint8Array(arrayBuffer);
    for (let i = 0; i < length; i++) {
      view[i] = binaryString.charCodeAt(i);
    }
    return arrayBuffer;
  },

  onUnload() {
    wx.removeStorageSync("detailItem");
  },

  chat(){
    wx.setStorageSync('lasturl2', '/pages/detail/detail'); 
    wx.setStorageSync('id', this.data.id);
    wx.redirectTo({
      url: `/pages/message/message?receiver=${this.data.detail.publisher}&id=${this.data.id}`
    });
  }
});
