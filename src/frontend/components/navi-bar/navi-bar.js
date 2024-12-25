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
    showSearch: {
      type: Boolean,
      value: false
    },
    searchQuery: {
      type: String,
      value: ''
    }
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
      console.log("showSearch ", this.data.showSearch)
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
        // 返回上一页
        wx.navigateBack({
            delta: 1
        });
    },
    getNaviInfo() {
      return {
        paddingTop: this.data.paddingTop,
        naviHeight: this.data.naviHeight,
      };
    },
    onSearchInput(event) {
      const query = event.detail.value;
      this.setData({
        searchQuery: query
      });
      // this.triggerEvent('search', query); // 向父组件传递搜索内容
    },
    onSearch() {
      console.log(this.data.searchQuery);
      this.triggerEvent('search', this.data.searchQuery); // 向父组件传递搜索内容
    }

  }
})