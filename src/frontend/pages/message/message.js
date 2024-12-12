Page({
  data: {
    receiver: "好友昵称", // 显示的好友昵称
    messages: [], // 聊天消息列表
    inputValue: "", // 输入框内容
  },

  // 页面加载时模拟初始化
  onLoad: function (options) {
    const receiver = options.receiver;
    this.setData({
      messages: [
        { id: 1, sender: "other", avatar: "https://example.com/other-avatar.png", content: "你好！" },
        { id: 2, sender: "self", avatar: "https://example.com/self-avatar.png", content: "你好！有什么事吗？" },
      ],
      receiver: receiver
    });
  },

  // 输入事件
  onInput: function (e) {
    this.setData({ inputValue: e.detail.value });
  },

  // 发送消息
  sendMessage: function () {
    if (!this.data.inputValue.trim()) return;

    // 添加自己的消息
    const newMessage = {
      id: this.data.messages.length + 1,
      sender: "self",
      avatar: "https://example.com/self-avatar.png",
      content: this.data.inputValue,
    };

    this.setData({
      messages: [...this.data.messages, newMessage],
      inputValue: "", // 清空输入框
    });

    // 模拟对方回复（可用WebSocket代替）
    setTimeout(() => {
      const replyMessage = {
        id: this.data.messages.length + 1,
        sender: "other",
        avatar: "https://example.com/other-avatar.png",
        content: "收到你的消息了！",
      };
      this.setData({
        messages: [...this.data.messages, replyMessage],
      });
    }, 1000);
  },

  // 选择表情
  chooseEmoji: function () {
    wx.showToast({ title: "表情选择功能未实现", icon: "none" });
  },

  // 选择图片
  chooseImage: function () {
    wx.showToast({ title: "图片选择功能未实现", icon: "none" });
  },
});
