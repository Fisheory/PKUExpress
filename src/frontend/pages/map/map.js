// pages/map/map.js
Page({

  /**
   * 页面的初始数据
   */
  data: {
    subKey: 'FGNBZ-FZKLV-NTKPS-5Y3AK-YQCB3-LOFL3',
    enable3d: false,
    showLocation: true,
    showCompass: false,
    enableOverlooking: false,
    enableZoom: true,
    enableScroll: true,
    enableRotate: false,
    drawPolygon: false,
    enableSatellite: false,
    enableTraffic: false,
    latitude: '39.9976',
    longitude: '116.3102',
    markers: [],
    circles: [],
    polylines: [],
    polygons: [],
    showDialog: false,
    currentMarker: null,
    features: [
      {"name":"地点1","geometry":{"type":"Point","coordinates":[116.3102,39.9976]}},
    ]
  },

  onReady: function () {
    const map = wx.createMapContext("map");
    map.moveToLocation();
  },

  onShow: function () {
    const markers = this.data.features.map((feature,index) => {
      return {
        id: index,
        latitude: feature.geometry.coordinates[1],
        longitude: feature.geometry.coordinates[0],
        properties: {
          name: feature.name,
          code: feature.code
        },
      }
    });
    
    this.setData({
      markers: markers
    });
  },


  handleMarkerTap(e) {
    console.log(e);
    const marker = this.data.markers.find(item => item.id == e.markerId);
    marker && this.setData({
      currentMarker: marker,
      showDialog: true
    });
    //this.data.showDialog = true;
  },

})