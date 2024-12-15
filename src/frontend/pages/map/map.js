// pages/map/map.js
var amapFile = require('../../libs/amap-wx.130.js');

Page({
  data: {
    markers: [],
    latitude: '',
    longitude: '',
    textData: {},
    inputLocation: '',
    selectedLocation: null // To store confirmed location
  },

  onLoad: function () {
    var that = this;
    this.mapContext = new amapFile.AMapWX({ key: 'd351e5acebebe211388ac1efb1e18540' });
  
    // Get current location and display on map
    this.mapContext.getRegeo({
      success: function (data) {
        if (data && data.length > 0) {
          var location = data[0];
  
          // Set default marker for current location
          var marker = [{
            id: 0,
            latitude: location.latitude,
            longitude: location.longitude,
            width: 22,
            height: 32
          }];
  
          that.setData({
            markers: marker,
            latitude: location.latitude,
            longitude: location.longitude,
            textData: {
              name: location.name || '当前位置',
              desc: location.desc || '您当前的位置'
            },
            selectedLocation: {
              latitude: location.latitude,
              longitude: location.longitude,
              name: location.name || '当前位置'
            }
          });
        }
      },
      fail: function () {
        wx.showToast({ title: '无法获取当前位置', icon: 'none' });
      }
    });
  },
  

  // Update input value
  onInputChange: function (e) {
    this.setData({
      inputLocation: e.detail.value
    });
  },

  // Search for location
  searchLocation: function () {
    var that = this;
    var input = this.data.inputLocation;

    if (!input) {
      wx.showToast({ title: '请输入地点名称', icon: 'none' });
      return;
    }

    that.mapContext.getInputtips({
      keywords: input,
      success: function (data) {
        if (data && data.tips && data.tips.length > 0) {
          var location = data.tips[0].location.split(',');

          var latitude = parseFloat(location[1]);
          var longitude = parseFloat(location[0]);

          // Update markers and center map
          var marker = [{
            id: 0,
            latitude: latitude,
            longitude: longitude,
            iconPath: "../../img/marker.png",
            width: 22,
            height: 32
          }];

          that.setData({
            markers: marker,
            latitude: latitude,
            longitude: longitude,
            textData: {
              name: data.tips[0].name,
              desc: data.tips[0].district
            },
            selectedLocation: {
              latitude: latitude,
              longitude: longitude,
              name: data.tips[0].name
            }
          });
        } else {
          wx.showToast({ title: '未找到相关地点', icon: 'none' });
        }
      },
      fail: function () {
        wx.showToast({ title: '搜索失败', icon: 'none' });
      }
    });
  },

  // Confirm the selected location
  confirmLocation: function () {
    if (this.data.selectedLocation) {
      wx.showModal({
        title: '选择成功！',
        content: `您已选择： ${this.data.selectedLocation.name}`,
        showCancel: false
      });
      console.log('Confirmed location:', this.data.selectedLocation);
    } else {
      wx.showToast({ title: 'Please search and select a location first.', icon: 'none' });
    }
  }
});
