// page/zhandouli/index.js
Page({

  /**
   * 页面的初始数据
   */
  data: {
    level : 'F',
    p_count : 10,
    items: [{
      nickname: 'mike',level:'F'
    }, {
        nickname: 'sisi', level: 'A'
    }]
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
 
    var app = getApp() 
    var page = this
    // this.setData({ items: [{ nickname: 'aa', level: 'F' }, { nickname: 'bb', level: 'F' }, { nickname: 'cc', level: 'F'}]})
    wx.request({
      method:'POST',
      url: 'https://www.qiaohequan.com/wx/get_user_level_list',
      data: {
        nickname: app.globalData.userInfo.nickName        
      },
      header: {
        "Content-Type": "application/json"
      },
      success: function (res) {
        var data = res.data;
 
        console.log(data)// {items: Array[4], level: "F", p_count: 3 }
        page.setData({ p_count: data.p_count})
        page.setData({ level: data.level })
        page.setData({ items: data.items })
         
      }
    });


  },

  /**
   * 生命周期函数--监听页面初次渲染完成
   */
  onReady: function () {
  
  },

  /**
   * 生命周期函数--监听页面显示
   */
  onShow: function () {
  
  },

  /**
   * 生命周期函数--监听页面隐藏
   */
  onHide: function () {
  
  },

  /**
   * 生命周期函数--监听页面卸载
   */
  onUnload: function () {
  
  },

  /**
   * 页面相关事件处理函数--监听用户下拉动作
   */
  onPullDownRefresh: function () {
  
  },

  /**
   * 页面上拉触底事件的处理函数
   */
  onReachBottom: function () {
  
  },

  /**
   * 用户点击右上角分享
   */
  onShareAppMessage: function () {
  
  }
})