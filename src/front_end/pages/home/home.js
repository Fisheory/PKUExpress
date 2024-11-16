Page({
  data: {
    containerHeight: 0,
    list: [
      {
        id: 1,
        title: "标题1",
        content: "这是内容1的描述。",
        route: "途径点1, 途径点2, 途径点3"
      },
      {
        id: 2,
        title: "标题2",
        content: "这是内容2的描述。",
        route: "途径点A, 途径点B"
      },
      {
        id: 3,
        title: "标题3",
        content: "这是内容3的描述。",
        route: "途径点X, 途径点Y, 途径点Z"
      },
      {
        id: 4,
        title: "标题3",
        content: "这是内容3的描述。",
        route: "途径点X, 途径点Y, 途径点Z"
      },
      {
        id: 5,
        title: "标题3",
        content: "这是内容3的描述。",
        route: "途径点X, 途径点Y, 途径点Z"
      },
      {
        id: 6,
        title: "标题3",
        content: "这是内容3的描述。",
        route: "途径点X, 途径点Y, 途径点Z"
      }
      // 可以根据需要增加更多条目
    ]
  },

  // 点击查看详情
  viewDetail(e) {
    const id = e.currentTarget.dataset.id;
    console.log("查看详情，ID:", id);
    // 跳转到详情页面
    wx.navigateTo({
      url: `/pages/detail/detail?id=${id}`
    });
  },

  onLoad() {
    const navibar = this.selectComponent('#navi-bar'); // 选择导航栏组件
    const { paddingTop, naviHeight } = navibar.getNaviInfo();
    const windowHeightPx = wx.getWindowInfo().windowHeight;
    const bottomHeightPx = 140 * wx.getWindowInfo().windowWidth / 750;
    this.setData({
      containerHeight: windowHeightPx - paddingTop - naviHeight - bottomHeightPx - 10,
    });
  },
});
