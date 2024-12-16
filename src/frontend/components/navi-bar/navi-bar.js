// components/navi-bar.js
Component({

  /**
   * 组件的属性列表
   */
  properties: {
    title: {
      type: String,
      value: ''
    },
    showBack: {
      type: Boolean,
      value: true
    },
    url: {
      type: String,
      value: ''
    },
  },

  /**
   * 组件的初始数据
   */
  data: {
    paddingTop: 0,
    gap: 0,
    naviHeight: 0,
    platform: ''
  },
  lifetimes: {
    attached() {
      // 设置导航栏的高度
      let statusBarHeight = wx.getWindowInfo().statusBarHeight
      let capsule = wx.getMenuButtonBoundingClientRect()
      this.setData({
        paddingTop: statusBarHeight,
        gap: capsule.top - statusBarHeight
      });
      this.setData({
        platform: wx.getDeviceInfo().platform
      });
      console.log(this.data.platform);
      let height = capsule.height + 2 * this.data.gap;
      this.setData({
        naviHeight: height
      });
      console.log(this.data.gap);
      console.log(this.data.paddingTop);
      console.log(this.data.naviHeight);
    }
  },
  /**
   * 组件的方法列表
   */
  methods: {
    onBack() {
      const targetPagePath = this.properties.url;
      console.log(targetPagePath)
      if (targetPagePath) {
        // 如果指定了目标页面路径，则跳转
        wx.navigateTo({
          url: targetPagePath,
        });
      } else {
        // 否则返回上一页
        wx.navigateBack({
          delta: 1
        });
      }
    },
    getNaviInfo() {
      return {
        paddingTop: this.data.paddingTop,
        naviHeight: this.data.naviHeight,
      };
    },
  }
})